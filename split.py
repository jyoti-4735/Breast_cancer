import os
import shutil
import random

def split_data(src_dir, dst_dir, split_ratio=0.8):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for category in os.listdir(src_dir):
        category_path = os.path.join(src_dir, category)
        if not os.path.isdir(category_path):
            continue

        images = [f for f in os.listdir(category_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(images)

        train_size = int(len(images) * split_ratio)
        train_images = images[:train_size]
        test_images = images[train_size:]

        # Create train and test category folders
        train_cat_dir = os.path.join(dst_dir, 'train', category)
        test_cat_dir = os.path.join(dst_dir, 'test', category)
        os.makedirs(train_cat_dir, exist_ok=True)
        os.makedirs(test_cat_dir, exist_ok=True)

        # Copy files
        for img in train_images:
            shutil.copy2(os.path.join(category_path, img), os.path.join(train_cat_dir, img))

        for img in test_images:
            shutil.copy2(os.path.join(category_path, img), os.path.join(test_cat_dir, img))

        print(f"[✅] {category}: {len(train_images)} train, {len(test_images)} test")

# Set paths
source_path = r"D:\BCD\data_final"
target_path = r"D:\BCD\data_combined"

split_data(source_path, target_path)
print("\n✅ Dataset successfully split into train and test sets.")
