# The validation set is divided by an 8:2 ratio. We used stratified sampling based on scores to select 37 cases as the validation set from the total 187 cases.
val_names = [
    'NL_060.png', 'NL_076.png',     # [0, 1) 2
    'NL_034.png', 'cataract_011.png', 'cataract_044.png', 'cataract_055.png', 'DJD1.jpg', 'MYZ2.jpg',    # [1, 3) 6
    'cataract_002.png', 'cataract_045.png', 'cataract_051.png', 'LXW2.jpg', 'cataract_001.png', 'cataract_003.png', 'SGZ-OS.jpg',   # [3, 5) 7
    'cataract_069.png', 'cataract_037.png', 'cataract_090.png', 'LL2.jpg', 'cataract_079.png', 'cataract_096.png', 'cataract_099.png', 'HZH1.jpg', 'cataract_081.png', 'left-eye-2.jpg',   # [5, 7) 10
    'SYY1.jpg', 'cataract_087.png', 'cataract_025.png', 'cataract_030.png', 'YZT1.jpg', 'cataract_093.png', 'cataract_063.png', 'HFM4.jpg', 'cataract_065.png', 'cataract_083.png', 'ZJC2.jpg', 'WC2.jpg'   # [7, 10] 12
]