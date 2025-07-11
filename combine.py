import os
import shutil

# Base directory where your datasets are stored
base_dir = "data"

# Datasets and their classification
breast_datasets = ["BreaKHis 400X", "Dataset_BUSI_with_GT", "ICIAR2018_BACH_Challenge", "idc", "tcga_brca"]
non_breast_datasets = ["ImageNet-Mini", "cifar-10-batches-py"]

# New organized directory
organized_dir = "data_organized"

# Function to move datasets
def move_dataset(dataset_list, category):
    for name in dataset_list:
        src = os.path.join(base_dir, name)
        dst = os.path.join(organized_dir, category, name)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            print(f"✅ Moved '{name}' to '{category}'")
        else:
            print(f"❌ Dataset '{name}' not found in '{base_dir}'")

# Organize datasets
move_dataset(breast_datasets, "breast")
move_dataset(non_breast_datasets, "non_breast")
