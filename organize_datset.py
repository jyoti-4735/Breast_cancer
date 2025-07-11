import os
import shutil

def move_images(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_dir, file)
                shutil.copy2(src_file, dst_file)

# Define source directories
source_dirs = {
    "malignant": r"D:\BCD\data_organized\breast\BreaKHis 400X\train\malignant",
    "benign": r"D:\BCD\data_organized\breast\BreaKHis 400X\train\benign",
    "normal": r"D:\BCD\data_organized\breast\ICIAR2018_BACH_Challenge\ICIAR2018_BACH_Challenge\Photos\Normal",
    "other": r"D:\BCD\data_organized\non_breast\ImageNet-Mini"
}

# Target unified structure
target_base = r"D:\BCD\data_final"

for label, src in source_dirs.items():
    dst = os.path.join(target_base, label)
    print(f"🔄 Copying {label} images...")
    move_images(src, dst)

print("\n✅ All images organized successfully into 'data_final' folder.")
