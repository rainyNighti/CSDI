## Getting Started
Our code is built upon [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) with only minimal modifications. We strongly recommend that you familiarize yourself with that framework first.

**Key Modifications:**
The primary changes are located in `csdi/src/llamafactory/train/sft/trainer.py`, specifically the `QAlignSeq2SeqTrainer` class.

### Installation
Our code has been tested and verified on **CUDA 12.1**, though it supports newer CUDA versions.

```bash
conda create -n csdi python=3.10
conda activate csdi
cd csdi
pip install -e '.[torch,metrics]'
```

### Data Preparation
1. Crop Images. Run the following command to preprocess the dataset. This script crops individual fundus images to remove black borders and saves them to the specified path.
```bash
python crop_fundus_images.py
```

2. Augment Images. Run the command below to generate the augmented training set. Note: To minimize modifications to the LLaMA-Factory codebase, we pre-generate a batch of augmented images and save them locally for the training dataloader to read directly.
```bash
python augment_fundus_images.py
```

3. Generate JSON Files. Run the following command to create the JSON files required for training and testing. Note: The generated training and inference JSON files will be stored in csdi/data.
```bash
python create_dataset_json.py
```

### Train & Evaluation
You can use the LLaMA-Factory WebUI to generate specific training and inference commands. Please refer to the LLaMA-Factory tutorials for details.
```bash
llamafactory-cli webui
```
In the examples below, we use Qwen2.5-VL-7B-Instruct. Commands for other models can be generated similarly via the WebUI. 

Hardware Note: These tests were conducted on an H20 GPU (96GB VRAM). If your GPU has less memory, please reduce the batch size accordingly.

#### 1 Zero-shot Inference
```bash
cd csdi
llamafactory-cli train \
    --stage sft \
    --model_name_or_path Qwen/Qwen2-VL-7B-Instruct \
    --preprocessing_num_workers 16 \
    --finetuning_type lora \
    --quantization_method bnb \
    --template qwen2_vl \
    --flash_attn auto \
    --dataset_dir data \
    --eval_dataset csdi_zero_shot_prompt_val \
    --cutoff_len 4096 \
    --max_samples 37 \
    --per_device_eval_batch_size 37 \
    --predict_with_generate True \
    --report_to none \
    --max_new_tokens 512 \
    --top_p 0.7 \
    --temperature 0.95 \
    --output_dir saves/Qwen2-VL-7B-Instruct/zero-shot \
    --trust_remote_code True \
    --ddp_timeout 180000000 \
    --do_predict True 
```

#### 2 Zero-shot Result Evaluation

```bash
python csdi/eval_csdi_metric.py \
    --predict_json_path "csdi/saves/Qwen2-VL-7B-Instruct/zero-shot/generated_predictions.jsonl" \
    --use_g_eval \
    --gpt_api_key "you api key"
```

#### 3 SFT Training
```bash
cd csdi
llamafactory-cli train \
    --stage sft \
    --do_train True \
    --model_name_or_path Qwen/Qwen2-VL-7B-Instruct \
    --preprocessing_num_workers 16 \
    --finetuning_type lora \
    --template qwen2_vl \
    --flash_attn auto \
    --dataset_dir data \
    --dataset csdi_sft_prompt_train \
    --cutoff_len 4096 \
    --learning_rate 5e-05 \
    --num_train_epochs 6.0 \
    --max_samples 100000 \
    --per_device_train_batch_size 8 \
    --gradient_accumulation_steps 2 \
    --lr_scheduler_type cosine \
    --max_grad_norm 1.0 \
    --logging_steps 1 \
    --save_steps 10 \
    --warmup_steps 0 \
    --packing False \
    --enable_thinking True \
    --report_to none \
    --output_dir saves/Qwen2-VL-7B-Instruct/lora/train_CSDI \
    --bf16 True \
    --plot_loss True \
    --trust_remote_code True \
    --ddp_timeout 180000000 \
    --include_num_input_tokens_seen True \
    --optim adamw_torch \
    --lora_rank 8 \
    --lora_alpha 16 \
    --lora_dropout 0 \
    --lora_target all \
    --freeze_vision_tower True \
    --freeze_multi_modal_projector True \
    --image_max_pixels 589824 \
    --image_min_pixels 1024 \
    --video_max_pixels 65536 \
    --video_min_pixels 256 
```

#### 4 SFT Inference
```bash
cd csdi
llamafactory-cli train \
    --stage sft \
    --model_name_or_path Qwen/Qwen2-VL-7B-Instruct \
    --preprocessing_num_workers 16 \
    --finetuning_type lora \
    --quantization_method bnb \
    --template qwen2_vl \
    --flash_attn auto \
    --dataset_dir data \
    --eval_dataset csdi_sft_prompt_val \
    --cutoff_len 4096 \
    --max_samples 37 \
    --per_device_eval_batch_size 37 \
    --predict_with_generate True \
    --report_to none \
    --max_new_tokens 512 \
    --top_p 0.7 \
    --temperature 0.95 \
    --output_dir saves/Qwen2-VL-7B-Instruct/SFT/ \
    --trust_remote_code True \
    --ddp_timeout 180000000 \
    --do_predict True \
    --adapter_name_or_path saves/Qwen2-VL-7B-Instruct/lora/train_CSDI/checkpoint-396
```

#### 4 SFT Result Evaluation

```bash
python csdi/eval_csdi_metric.py \
    --predict_json_path "csdi/saves/Qwen2-VL-7B-Instruct/SFT/generated_predictions.jsonl" \
    --is_q_align \
    --use_g_eval \
    --gpt_api_key "you api key"
```


## Related Projects

Our work is inspired by these excellent open-sourced repos:
[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

## Citation

If you find this project helpful, please consider citing the following paper:
@misc{csdi2025cataract,
  title        = {CSDI: A Fine-Grained Fundus Image Dataset of Cataract Severity and Diagnostic Images},
  author       = {Xie, Zixun and Ao, Mingxin and Tang, Haiming and Li, Xuemin and Bai, Xiang and Zhang, Shanghang and Li, Dawei},
  year         = {2025},
  note         = {Under review at Scientific Data}
}