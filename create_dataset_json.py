import os
import csv
import json
from prompt import get_prompt_for_zero_shot, get_prompt_for_sft
from dataset_split import val_names

def save_json(name, data, output_dir):
    json_file_path = f"{output_dir}/{name}.json"
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved {output_dir}/{name}.json, containing {len(data)} entries.")

def create_dataset_json(prompt_base, output_dir, csv_file, images_dir, is_augment=False, is_zero_shot=False):

    os.makedirs(output_dir, exist_ok=True)

    val_data = []
    train_data = []

    all_image_files = []
    if is_augment:
        all_image_files = os.listdir(images_dir)

    images_dir = images_dir.replace('csdi/', '') 
    
    with open(csv_file, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for item in reader:
            original_id = item['id']
            score = item['score']
            thought = item["English_diagnosis"]

            base_data_dict = prompt_base(thought, score)

            if is_augment:
                base_name = os.path.splitext(original_id)[0]
                
                if original_id in val_names:
                    data_dict = base_data_dict.copy()
                    data_dict["images"] = [os.path.join(images_dir, original_id)]
                    val_data.append(data_dict)
                else:
                    related_files = [f for f in all_image_files if f.startswith(base_name)]
                    for filename in related_files:
                        data_dict = base_data_dict.copy()
                        data_dict["images"] = [os.path.join(images_dir, filename)]
                        train_data.append(data_dict)
            else:
                data_dict = base_data_dict.copy()
                data_dict["images"] = [os.path.join(images_dir, original_id)]
                if original_id in val_names:
                    val_data.append(data_dict)
                else:
                    train_data.append(data_dict)

    if not is_zero_shot:
        save_json('train', train_data, output_dir)
    save_json('val', val_data, output_dir)

if __name__ == "__main__":
    csv_file = "CSDI_annotations.csv"

    # zero-shot prompt generate
    create_dataset_json(
        prompt_base=get_prompt_for_zero_shot,
        output_dir="csdi/data/csdi_zero_shot_prompt",
        csv_file=csv_file,
        images_dir='csdi/processed_data/croped_images',
        is_zero_shot=True
    )

    # SFT discrete level to score prompt generate
    create_dataset_json(
        prompt_base=get_prompt_for_sft,
        output_dir="csdi/data/csdi_sft_prompt",
        csv_file=csv_file,
        images_dir='csdi/processed_data/croped_augmented_images',
        is_augment=True     # [optional]
    )