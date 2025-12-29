import sys
from pathlib import Path
current_file = Path(__file__).resolve()
target_path = current_file.parent.parent
sys.path.append(str(target_path))

import json
import re
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import os
import torch
import pandas as pd
import math
import argparse
from openai import OpenAI, APIStatusError
from prompt import get_g_eval_prompt, convert_to_level

class MetricEvaluator:
    def __init__(self, filepath, output_dir, csv_path, is_q_align=False, use_g_eval=False, gpt_api_key=None):
        self.filepath = filepath
        self.is_q_align = is_q_align
        self.level_name = ['normal', 'acceptable', 'mild', 'moderate', 'severe']
        self.level_weights = torch.tensor([0.5, 2, 4, 6, 8.5])
        self.data_info = pd.read_csv(csv_path, encoding='utf-8')
        self.acc = []
        self.mse = []
        self.bleu_scores = {"bleu-1": [], "bleu-2": [], "bleu-3": [], "bleu-4": []}
        self.g_eval_scores = []
        self.error_messages = []
        self.output_dir = output_dir
        self.use_g_eval = use_g_eval
        if self.use_g_eval:
            assert gpt_api_key != "",  "必须传入 GPT API key"
            self.client = OpenAI(api_key=gpt_api_key)
        

    def extract_level_and_score(self, text):
        """
        提取`<score>`和`<level>`，格式为：**Diagnosis**: <score> <level>
        """
        pattern = r"\*\*Diagnosis\*\*: ([+-]?\d+\.\d+|[+-]?\d+)\s(\w+)"
        match = re.search(pattern, text)
        if not match:
              raise ValueError(f"Failed to extract score and level from text: {text}")
        return float(match.group(1)), match.group(2)

    def calculate_bleu(self, reference, prediction):
        """
        计算BLEU 1-4分数
        """
        smoothing_function = SmoothingFunction().method3
        for n in range(1, 5):
            bleu_score = sentence_bleu(
                [list(reference)], list(prediction),
                weights=[1/n] * n + [0] * (4-n),
                smoothing_function=smoothing_function
            )
            self.bleu_scores[f"bleu-{n}"].append(round(bleu_score * 100, 4))

    def metric_gpt4o(self, label, pred):
        """
        调用G-eval API计算评分
        """

        eval_prompt = get_g_eval_prompt(label, pred)

        try:
            # 调用 chat.completions.create 方法
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": "You are an AI assistant."}]
                    },
                    {"role": "user", "content": eval_prompt}
                ],
                temperature=0.7,
                top_p=0.95,
                max_tokens=800
            )
            
            # 从响应对象中获取内容
            content = response.choices[0].message.content.strip()
            rating_value = float(content)
        except APIStatusError as e: # 捕获 OpenAI 库特有的 API 错误
            print(f"Failed to make the request to OpenAI API. Status: {e.status_code}, Message: {e.response}")
            raise SystemExit(f"Failed to make the request. Error: {e}")
        except ValueError as e:
            rating_value = -1.0
            self.error_messages.append(f"Failed to parse rating: '{content}' (Error: {e})")
            print(f"Failed to parse rating: '{content}' (Error: {e})") # 打印错误信息以便调试
        except Exception as e: # 捕获其他未知错误
            print(f"An unexpected error occurred: {e}")
            raise SystemExit(f"An unexpected error occurred. Error: {e}")

        return rating_value


    def evaluate(self):
        """
        评估指标
        """
        with open(self.filepath, 'r') as f:
            for line in f:
                data = json.loads(line)
                pred, label = data["predict"], data["label"]
                if self.is_q_align:
                    score_logits = torch.tensor(data['logit'])
                    pred_score = (torch.softmax(score_logits, dim=0) @ self.level_weights).item()
                    pred_level = self.level_name[torch.argmax(score_logits).item()]
                    id = data['img_path'][0].split('/')[-1]
                    label_score = self.data_info[self.data_info['id'] == id]['score'].values[0]
                    label_level = convert_to_level(label_score)
                else:
                    try:
                        pred_score, pred_level = self.extract_level_and_score(pred)
                        label_score, label_level = self.extract_level_and_score(label)
                    except ValueError as e:
                        self.error_messages.append(str(e))
                        pred_score = 10
                        pred_level = 'error'
                        label_level = "true"
                        label_score = 0     # 对于格式错误无法匹配的case,设置为rmse=10
                        
                # ACC
                self.acc.append(pred_level == label_level)

                # MSE
                self.mse.append(math.sqrt((pred_score - label_score) ** 2))

                # BLEU
                self.calculate_bleu(label, pred)

                # G-eval
                if self.use_g_eval:
                    g_eval_score = self.metric_gpt4o(label, pred)
                    self.g_eval_scores.append(g_eval_score)

        # 输出最终结果
        acc_result = sum(self.acc) / len(self.acc) if len(self.acc) != 0 else 0
        mse_result = sum(self.mse) / len(self.mse) if len(self.mse) != 0 else 0
        bleu_result = {key: round(sum(values) / len(values), 2) if len(values) != 0 else 0 \
             for key, values in self.bleu_scores.items()}
        if self.use_g_eval:
            g_eval_result = sum(self.g_eval_scores) / len(self.g_eval_scores) if len(self.g_eval_scores) != 0 else 0

        # 保存结果到metric.txt
        with open(self.output_dir, 'w') as metrics_file:
            metrics_file.write(f"ACC: {round((acc_result * 100), 2)}\n")
            metrics_file.write(f"MSE: {round(mse_result, 2)}\n")
            metrics_file.write(f"BLEU Scores: {bleu_result}\n")
            if self.use_g_eval:
                metrics_file.write(f"G-eval: {round(g_eval_result, 2)}\n")

        # 保存错误信息到error.txt
        error_path = os.path.join(os.path.dirname(self.filepath), 'error.txt')
        with open(error_path, 'w') as error_file:
            for error in self.error_messages:
                error_file.write(error + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--predict_json_path')
    parser.add_argument('--output_dir', default="", help="The default directory is at the same level as predict json", )
    parser.add_argument('--is_q_align', action='store_true', help='need to convert level to score')
    parser.add_argument('--use_g_eval', action='store_true')
    parser.add_argument('--gpt_api_key', default="")
    parser.add_argument('--csv_path', default="CSDI_annotations.csv")
    
    args = parser.parse_args()

    if not args.output_dir:
        args.output_dir = os.path.join(os.path.dirname(args.predict_json_path), 'metric.txt')

    evaluator = MetricEvaluator(
        filepath=args.predict_json_path,
        output_dir=args.output_dir,
        is_q_align=args.is_q_align,
        use_g_eval=args.use_g_eval,
        gpt_api_key=args.gpt_api_key,
        csv_path=args.csv_path
    )
    evaluator.evaluate()
