from pathlib import Path
import tesserocr
from mmcv import mkdir_or_exist
from PIL import Image
import json


base_folder = Path('input')
target_folder = 'sadam'
target_path = base_folder / target_folder

file_list = list(target_path.glob('*.jpg')) + list(target_path.glob('*.png')) + list(target_path.glob('*.jpeg'))

print(tesserocr.tesseract_version())  # print tesseract-ocr version
print(tesserocr.get_languages())  # prints tessdata path and list of available languages


def ocr_image(image_path):
    print(f"Performing OCR on: {image_path}")
    image = Image.open(image_path)
    text = tesserocr.image_to_text(image, lang="ell+eng")
    print(f"Extracted text: {text}")
    return  text

extracted_data = {}
for file_path in file_list:
    print(f"Processing file: {file_path}")
    text = ocr_image(file_path)
    extracted_data[file_path.name] = text

print("Extracted data from all images")

mkdir_or_exist(Path('data'))
save_file_name = Path('data') / f"{target_folder}.json"

with open(save_file_name, "w", encoding="utf-8") as file:
    json.dump(extracted_data, file, indent=4, ensure_ascii=False)




