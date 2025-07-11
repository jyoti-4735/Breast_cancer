import os

def count_images(folder):
 image_extensions = ('.jpg', '.jpeg', '.png')
 count = 0
 for root, _, files in os.walk(folder):
  for file in files:
   if file.lower().endswith(image_extensions):
    count += 1
   return count

paths = {
"malignant": r"D:\BCD\data_organized\breast\BreaKHis 400X\train\malignant",
"benign": r"D:\BCD\data_organized\breast\BreaKHis 400X\train\benign",
"normal": r"D:\BCD\data_organized\breast\ICIAR2018_BACH_Challenge\ICIAR2018_BACH_Challenge\Photos\Normal",
"other": r"D:\BCD\data_organized\non_breast\ImageNet-Mini",
}

total_images = 0

print("\n🔍 Scanning dataset folders...\n")

for name, path in paths.items():
 if not os.path.exists(path):
  print(f"❌ Folder not found: {name} -> {path}")
 else:
  img_count = count_images(path)
total_images += img_count
print(f"✅ {name.capitalize():<10} contains {img_count} images at:\n 📁 {path}\n")

print(f"\n📊 Total images across all categories: {total_images}\n")
