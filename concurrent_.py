from PIL import Image, ImageOps, ImageFilter
import os
import time
from concurrent.futures import ThreadPoolExecutor

def process_image(image_path, output_folder, new_size):
    start_time = time.time()
    
    img = Image.open(image_path)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_resized = img.resize(new_size)
    
    img_detail = img_resized.filter(ImageFilter.DETAIL)
    
    img_solarized = ImageOps.solarize(img_detail, threshold=128)
    
    img_sharpen = img_solarized.filter(ImageFilter.SHARPEN)
    
    base_name = os.path.basename(image_path)
    processed_image_path = os.path.join(output_folder, f"processed_{base_name}")
    
    img_sharpen.save(processed_image_path)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Imagem salva em: {processed_image_path} (Tempo de processamento: {elapsed_time:.2f} segundos)")

def process_images(input_folder, output_folder, new_size, num_threads):
    total_start_time = time.time()
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    image_paths = [os.path.join(input_folder, file_name) for file_name in os.listdir(input_folder) if file_name.endswith(('.png', '.jpg', '.jpeg', '.jfif'))]
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(lambda image_path: process_image(image_path, output_folder, new_size), image_paths)

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    
    print(f"Tempo total de processamento de todas as imagens: {total_elapsed_time:.2f} segundos")

input_folder = './images'
output_folder = './processed-images'

for num_threads in [2, 8, 32]:
    print(f"\nProcessando com {num_threads} threads:")
    process_images(input_folder, output_folder, (800, 600), num_threads)
