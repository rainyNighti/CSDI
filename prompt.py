# use for zero-shot prompt
prompt_cataract_grading_with_score = """<image># Task Description
Simulate an experienced ophthalmologist analyzing fundus photographs to assess the severity of cataracts. Follow these steps to observe and evaluate the images, and provide a diagnosis based on the observations. The diagnosis should be categorized into one of the following five levels and their corresponding scores:  
**normal [0,1)**, **acceptable [1,3)**, **mild [3,5)**, **moderate [5,7)**, **severe [7,10]**.
## 1. Observe Overall Color of the Photograph
- The background color of the photograph is typically orange-red, representing a healthy retina. Evaluate any deviation from this color:
  - **Minimal deviation**: Suggests `normal` (e.g., 0.3) or `mild` (e.g., 3.7).
  - **Significant deviation towards yellow-white**: Indicates `moderate` (e.g., 5.8) or `severe` (e.g., 8.2).
  - **Pronounced deviation**: Suggests `severe` (e.g., 9.5).
## 2. Assess Overall Brightness
- A healthy fundus photograph should have moderate brightness, allowing clear visibility of the optic disc, blood vessels, and macula. Consider the following brightness changes:
  - **Normal brightness**: Indicates `normal` (e.g., 0.7).
  - **Slight decrease**: Suggests `acceptable` (e.g., 2.4) or `mild` (e.g., 3.9).
  - **Significant decrease and dullness**: Implies `moderate` (e.g., 6.3) or `severe` (e.g., 8.6).
  - **Extremely low brightness**: Typically indicates `severe` (e.g., 9.8).
## 3. Evaluate Optic Disc Clarity
- The optic disc should be clearly visible. Note the following conditions:
  - **Clear optic disc margins**: Suggests `normal` (e.g., 0.4).
  - **Slightly blurred margins**: Indicates `acceptable` (e.g., 2.1) or `mild` (e.g., 3.5).
  - **Noticeably blurred margins**: Suggests `moderate` (e.g., 6.0) or `severe` (e.g., 8.9).
  - **Completely obscured margins**: Typically indicates `severe` (e.g., 9.7).
## 4. Examine Macula Region
- The macula region is crucial for evaluating cataracts. Consider the following factors:
  - If the pupil is small or the photograph is taken in low light, the macula may appear darker; use optic disc and blood vessel clarity for comprehensive judgment.
  - **Clearly defined macula**: Suggests `normal` (e.g., 0.8).
  - **Blurred but identifiable macula**: Indicates `mild` (e.g., 4.2) or `moderate` (e.g., 5.9).
  - **Unidentifiable macula**: Typically indicates `severe` (e.g., 9.4).
## 5. Assess Retinal Blood Vessel Clarity
- The clarity of retinal blood vessels is vital for cataract assessment. Use the following criteria:
  - **No visible blood vessels**: Indicates `severe` (e.g., 9.9).
  - **Only major blood vessels visible, smaller branches obscured**: Suggests `severe` (e.g., 8.7).
  - **Visible second-level branches but blurred**: Indicates `moderate` (e.g., 6.4).
  - **Clear visibility of fine branches, slightly blurred edges**: Suggests `mild` (e.g., 4.1).
  - **Clear visibility of main and fine branches**: Suggests `normal` (e.g., 0.6) or `acceptable` (e.g., 2.2).
## 6. Comprehensive Judgment and Diagnosis
- Based on the observations above, analyze the overall color, brightness, optic disc clarity, macula region, and blood vessel visibility to select one of the following levels and scores to describe the severity of the cataract:
  1. **normal [0,1]**: No signs of cataract; retina color is normal, brightness is moderate, optic disc, blood vessels, and macula are clearly visible. Example: `0.8 normal`.
  2. **acceptable (1,3]**: Early-stage cataract; slight impact on vision but clinically insignificant. Photograph slightly blurred, brightness slightly decreased, optic disc and blood vessel edges slightly blurred, macula identifiable. Example: `acceptable 2.5`.
  3. **mild (3,5]**: Cataract affects visual quality; may cause slight blurring and brightness decrease. Optic disc edges and blood vessel branches are blurred, macula blurred but identifiable. Example: `3.8 mild`.
  4. **moderate (5,7]**: Cataract significantly affects visual quality; brightness noticeably decreased, photograph blurred, optic disc edges unclear, only major blood vessels visible, macula unidentifiable. Example: `6.5 moderate`.
  5. **severe (7,10]**: Cataract causes severe visual impairment; extremely low brightness, photograph severely blurred, optic disc edges and blood vessels completely unclear, macula unidentifiable. Example: `9.3 severe`.
## Please ensure that your output strictly follows the format below:
**Observation**: <your detailed observation and analysis>\n**Diagnosis**: <score> <category>
> **Important**: Do not add any additional characters (e.g., `\n`) after the `<category>` field. The output must end exactly at `<category>` without any trailing spaces or line breaks.
Examples:
1. **Observation**: The fundus appears orange-red, with vivid colors, slightly reduced brightness, clear and identifiable optic disc and vascular texture, discernible fine blood vessels, and accurate localization of the macular area.\n**Diagnosis**: 0.5 normal
2. **Observation**: The fundus exhibits an orange-red background with a light to moderate white haze, accompanied by decreased brightness. The optic disc margins are blurred, with the secondary branches of blood vessels still discernible but with blurred edges. The macular area appears slightly blurred but can still be located. Consideration is given to moderate cataracts.\n**Diagnosis**: 4.5 mild
3. **Observation**: The fundus presents a yellow-white haze, with the optic disc, vessels, and macular structure all invisible, indicating severe cataracts.\n**Diagnosis**: 10.0 severe
## Notes
- If the photograph quality is poor, such as blurred or underexposed, reasonably hypothesize possible reasons (e.g., small pupil or insufficient shooting conditions) and indicate the hypothesis in the diagnosis.
- If uncertain, refer to standardized normal and abnormal fundus photographs and strive to make a reasonable judgment."""

# use for SFT discrete level to score prompt
prompt_cataract_grading_categorical_only = """<image># Task Description
Simulate an experienced ophthalmologist analyzing fundus photographs to assess the severity of cataracts. Follow these steps to observe and evaluate the images, and provide a diagnosis based on the observations. The diagnosis should be categorized into one of the following five levels:  
**normal**, **acceptable**, **mild**, **moderate**, **severe**.
## 1. Observe Overall Color of the Photograph
- The background color of the photograph is typically orange-red, representing a healthy retina. Evaluate any deviation from this color:
  - **Minimal deviation**: Suggests `normal` or `mild`.
  - **Significant deviation towards yellow-white**: Indicates `moderate` or `severe`.
  - **Pronounced deviation**: Suggests `severe`.
## 2. Assess Overall Brightness
- A healthy fundus photograph should have moderate brightness, allowing clear visibility of the optic disc, blood vessels, and macula. Consider the following brightness changes:
  - **Normal brightness**: Indicates `normal`.
  - **Slight decrease**: Suggests `acceptable` or `mild`.
  - **Significant decrease and dullness**: Implies `moderate` or `severe`.
  - **Extremely low brightness**: Typically indicates `severe`.
## 3. Evaluate Optic Disc Clarity
- The optic disc should be clearly visible. Note the following conditions:
  - **Clear optic disc margins**: Suggests `normal`.
  - **Slightly blurred margins**: Indicates `acceptable` or `mild`.
  - **Noticeably blurred margins**: Suggests `moderate` or `severe`.
  - **Completely obscured margins**: Typically indicates `severe`.
## 4. Examine Macula Region
- The macula region is crucial for evaluating cataracts. Consider the following factors:
  - If the pupil is small or the photograph is taken in low light, the macula may appear darker; use optic disc and blood vessel clarity for comprehensive judgment.
  - **Clearly defined macula**: Suggests `normal`.
  - **Blurred but identifiable macula**: Indicates `mild` or `moderate`.
  - **Unidentifiable macula**: Typically indicates `severe`.
## 5. Assess Retinal Blood Vessel Clarity
- The clarity of retinal blood vessels is vital for cataract assessment. Use the following criteria:
  - **No visible blood vessels**: Indicates `severe`.
  - **Only major blood vessels visible, smaller branches obscured**: Suggests `severe`.
  - **Visible second-level branches but blurred**: Indicates `moderate`.
  - **Clear visibility of fine branches, slightly blurred edges**: Suggests `mild`.
  - **Clear visibility of main and fine branches**: Suggests `normal` or `acceptable`.
## 6. Comprehensive Judgment and Diagnosis
- Based on the observations above, analyze the overall color, brightness, optic disc clarity, macula region, and blood vessel visibility to select one of the following levels and scores to describe the severity of the cataract:
  1. **normal**: No signs of cataract; retina color is normal, brightness is moderate, optic disc, blood vessels, and macula are clearly visible.
  2. **acceptable**: Early-stage cataract; slight impact on vision but clinically insignificant. Photograph slightly blurred, brightness slightly decreased, optic disc and blood vessel edges slightly blurred, macula identifiable.
  3. **mild**: Cataract affects visual quality; may cause slight blurring and brightness decrease. Optic disc edges and blood vessel branches are blurred, macula blurred but identifiable.
  4. **moderate**: Cataract significantly affects visual quality; brightness noticeably decreased, photograph blurred, optic disc edges unclear, only major blood vessels visible, macula unidentifiable.
  5. **severe**: Cataract causes severe visual impairment; extremely low brightness, photograph severely blurred, optic disc edges and blood vessels completely unclear, macula unidentifiable.
## Please ensure that your output strictly follows the format below:
**Observation**: <your detailed observation and analysis>\n**Diagnosis**: <category>
Examples:
1. **Observation**: The fundus appears orange-red, with vivid colors, slightly reduced brightness, clear and identifiable optic disc and vascular texture, discernible fine blood vessels, and accurate localization of the macular area.\n**Diagnosis**: normal
2. **Observation**: The fundus exhibits an orange-red background with a light to moderate white haze, accompanied by decreased brightness. The optic disc margins are blurred, with the secondary branches of blood vessels still discernible but with blurred edges. The macular area appears slightly blurred but can still be located. Consideration is given to moderate cataracts.\n**Diagnosis**: mild
3. **Observation**: The fundus presents a yellow-white haze, with the optic disc, vessels, and macular structure all invisible, indicating severe cataracts.\n**Diagnosis**: severe
## Notes
- If the photograph quality is poor, such as blurred or underexposed, reasonably hypothesize possible reasons (e.g., small pupil or insufficient shooting conditions) and indicate the hypothesis in the diagnosis.
- If uncertain, refer to standardized normal and abnormal fundus photographs and strive to make a reasonable judgment."""

def convert_to_level(value):
    value = float(value)
    if 0 <= value < 1:
        return "normal"
    elif 1 <= value < 3:
        return "acceptable"
    elif 3 <= value < 5:
        return "mild"
    elif 5 <= value < 7:
        return "moderate"
    elif 7 <= value <= 10:
        return "severe"
    else:
        raise NotImplementedError("unknown level!")

# use for zero-shot prompt
def get_prompt_for_zero_shot(thought, score):
  return {
      "messages": [
          {"content": prompt_cataract_grading_with_score, "role": "user"},
          {"content": f"""**Observation**: {thought}\n**Diagnosis**: {score} {convert_to_level(score)}""", "role": "assistant"},
      ],
  }

# use for SFT discrete level to score prompt
def get_prompt_for_sft(thought, score):
  return {
      "messages": [
          {"content": prompt_cataract_grading_categorical_only, "role": "user"},
          {"content": f"""**Observation**: {thought}\n**Diagnosis**: {convert_to_level(score)}""", "role": "assistant"},
      ],
  }

# G-eval prompt
def get_g_eval_prompt(label, pred):
  return f"""You will be given one prediction (Pred) and the corresponding ground truth (GT) for a medical diagnosis.
  Your task is to evaluate the semantic similarity between the prediction and the ground truth.
  Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.
  Evaluation Criteria:
  Semantic Similarity (1-5): the degree to which the prediction (Pred) conveys the same meaning as the ground truth (GT).
  - 1: Poor. The prediction is completely different from the ground truth in meaning, with no overlap in key observations or diagnosis.
  - 2: Fair. The prediction has some overlap with the ground truth in meaning but misses or misrepresents key observations or diagnosis.
  - 3: Good. The prediction captures the main meaning of the ground truth but lacks detail or contains minor inaccuracies.
  - 4: Very Good. The prediction is almost identical to the ground truth in meaning, with only slight differences in phrasing or detail.
  - 5: Excellent. The prediction perfectly matches the ground truth in meaning, including all key observations and diagnosis.
  Evaluation Steps:
  1. Read the prediction (Pred) and the ground truth (GT) carefully.
  2. Compare the key observations, diagnosis, and overall meaning conveyed by the prediction and the ground truth.
  3. Assess how well the prediction aligns with the ground truth in terms of semantic meaning.
  4. Assign a semantic similarity score from 1 to 5.
  Example:
  Ground Truth (GT):
  {label}
  Prediction (Pred):
  {pred}
  ### Important: Return Format ###
  Your response must strictly follow this format:
  <score>

  Where <score> is a number between 1 and 5 (e.g., 1, 2.5, 4.0, etc.). Do not include any additional text or explanation."""