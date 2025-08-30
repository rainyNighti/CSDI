# CSDI: A Fine-Grained Fundus Image Dataset of Cataract Severity and Diagnostic Images

The **CSDI Cataract Diagnosis Dataset** is a curated collection of 187 fundus images with expert annotations, including cataract severity scores and bilingual diagnostic descriptions (English and Chinese). This dataset supports research in automated cataract screening, grading, and fundus image interpretation using both image and text modalities.
This dataset is licensed under CC BY-NC 4.0. See [LICENSE.md](LICENSE.md) for details.

## 📁 Dataset Overview

- **Total images**: 187
- **Image formats**: `.png` and `.jpg`
- **Annotation file**: `CSDI_annotations.csv`
- **Labels**: Cataract severity score (0–10), expert-written diagnoses, optic disc localization, optic disc clarity

## 📂 File Structure
```
CSDI/
├── original_images/ # Folder containing 187 fundus images (.png and .jpg)
│ ├── cataract_001.png
│ ├── cataract_002.jpg
│ └── ...
├── CSDI_annotations.csv # Annotation CSV file (UTF-8 encoded)
├── README.md                  # Dataset description
└── LICENSE.md                 # Dataset license (CC BY-NC 4.0)
```


## 🗒️ CSV Annotation File (`CSDI_annotations.csv`)
- The CSV annotation file is encoded in **UTF-8** to ensure proper display of English and Chinese characters.
- 
| Column Name                | Description |
|-----------------------------|-------------|
| `id`                       | Image file name (e.g., `cataract_001.png`) |
| `score`                    | Cataract severity score (range 0–10) |
| `English_diagnosis`        | Diagnosis in English |
| `Chinese_diagnosis`        | Diagnosis in Chinese |
| `original_image_width`     | Original image width in pixels |
| `original_image_height`    | Original image height in pixels |
| `fundus_region_x1 / y1 / x2 / y2` | Coordinates of the annotated fundus region in pixels; `-1` if not visible |
| `optic_disc_clear`         | Optic disc visibility (`visible` / `not visible`) |
| `optic_disc_x1 / y1 / x2 / y2` | Coordinates of the optic disc bounding box in pixels; `-1` if not visible |


> The `score` field supports both **regression** (exact score prediction) and **classification** (e.g., mild/moderate/severe).

## 📊 Suggested Severity Levels

The cataract severity grading criteria are defined as follows, with decimal scores (to one decimal place) allowing for precise assessment within each range:

| Severity Level   | Score Range | Quantity | Percentage (%) |
|------------------|-------------|----------|----------------|
| Normal           | [0, 1)      | 9        | 4.81           |
| Acceptable       | [1, 3)      | 30       | 16.04          |
| Mild             | [3, 5)      | 39       | 20.86          |
| Moderate         | [5, 7)      | 48       | 25.67          |
| Severe           | [7, 10]     | 61       | 32.62          |

- **0–1 (Normal):** No cataract; fundus images are clear with no lens opacity affecting image quality.  
- **1–3 (Acceptable):** Acceptable cataract; images remain clear with subtle blurring, low likelihood of visual impairment.  
- **3–5 (Mild):** Mild cataract; image clarity decreases, regular visual monitoring recommended, surgery unlikely immediately necessary.  
- **5–7 (Moderate):** Moderate cataract; noticeable reduction in image clarity, higher probability of visual impairment, elective surgery may be considered.  
- **7–10 (Severe):** Severe cataract; marked reduction in image clarity, significant impact on visual function, prompt surgical intervention advised.  

---

## 🔍 Diagnostic Content

Each record contains detailed diagnostic descriptions in both Chinese and English, following a fixed sentence structure evaluating:

- **Overall Color:** Typical orange-red fundus background; deviation toward yellow-white indicates increased cataract severity.  
- **Optic Disc and Vessel Clarity:** Blurring of optic disc margins and reduced vessel clarity indicate lens opacity affecting image quality.  
- **Macular Area:** Accurate localization and assessment of the macula is crucial; inability to do so suggests advanced cataract.  
- **Retinal Vessel Clarity and Branching:** Severity increases as visualization decreases from fine branch vessels, to major vessels and second-order branches, to only major vessels visible, to complete inability to distinguish vascular structures.  

This standardized scoring system and diagnostic protocol were strictly adhered to by annotators to ensure high-quality, reliable annotations.

---

English and Chinese versions of the diagnostic descriptions are included to support multilingual and cross-lingual research applications.


## 🎯 Applications

- Automated cataract screening and grading
- Ophthalmic report generation (image-to-text)
- Fundus image quality analysis
- Cross-modal learning and medical vision-language modeling
- Optic disc detection and segmentation

## 👨‍🔬 Authors

Zixun Xie<sup>1,2,\*</sup>, Mingxin Ao<sup>3,\*</sup>, Haiming Tang<sup>1,4,\*</sup>, Xuemin Li<sup>3</sup>, Xiang Bai<sup>1,2</sup>, Shanghang Zhang<sup>1,†</sup>, Dawei Li<sup>5,†</sup>

<sup>1</sup>State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University, China  
<sup>2</sup>School of Software and Microelectronics, Peking University, China  
<sup>3</sup>Department of Ophthalmology, Peking University Third Hospital, China  
<sup>4</sup>School of Computing, National University of Singapore, Singapore  
<sup>5</sup>School of Future Technology, Peking University, China  

**\*** Equal contribution and co-first authors.
**†** Corresponding authors.  

## 📬 Contact

- Zixun Xie: `zixun.xie@stu.pku.edu.cn`  
- Mingxin Ao: `mingxin256@vip.sina.com`  
- Haiming Tang: `haiming@comp.nus.edu.sg`  
- Xuemin Li: `lxmlxm66@sina.com`  
- Xiang Bai: `x.bai@stu.pku.edu.cn`  
- Shanghang Zhang: `shanghang@pku.edu.cn`  
- Dawei Li: `lidawei@pku.edu.cn`

## 📜 Citation

```bibtex
@misc{csdi2025cataract,
  title        = {CSDI: A Fine-Grained Fundus Image Dataset of Cataract Severity and Diagnostic Images},
  author       = {Xie, Zixun and Ao, Mingxin and Tang, Haiming and Li, Xuemin and Bai, Xiang and Zhang, Shanghang and Li, Dawei},
  year         = {2025},
  note         = {Under review at Scientific Data}
}
