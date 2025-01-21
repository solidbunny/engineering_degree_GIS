import json
import numpy as np
import skimage
import os
import shutil
import matplotlib.pyplot as plt
from matplotlib import cm
import ntpath
from pycocotools.coco import COCO


#stworzenie listy katalogów w pliku po których porusza się program
dirs_path = 'your_directory_containing_directories'
dirs = os.listdir(dirs_path)

#znalezienie plików json w katalogach
#lista plików json po której będziemy się poruszaj w dalszej części skryptu
json_files = []
for x in dirs:
    obj = os.scandir(dirs_path + '/' + x)
    for entry in obj:
        if entry.is_file() and '.json' in entry.name:
            #dodanie pliku do listy
            json_files.append(dirs_path  + x + '/' + entry.name)

def create_mask(image_info, annotations, output_folder):
    #tworzy pustą macierz numpy
    mask_np = np.zeros((image_info['height'], image_info['width']), dtype=np.uint8)
    #numer obiektu/annotacji
    o_n = 1
    #petla porusza sie w zakresie ilosci annotacji
    for ann in annotations:
        if ann['image_id'] == image_info['id']:
            for seg in ann['segmentation']:
                rr, cc = skimage.draw.polygon(seg[1::2], seg[0::2], mask_np.shape)
                mask_np[rr,cc] = 1
                o_n += 1

    #zapisanie maski jako plik
    mask_path = os.path.join(output_folder, image_info['file_name'])
    plt.imsave(mask_path, ~mask_np, cmap='Greys')
    print(mask_path)

def main(json_file, mask_output_folder, original_image_dir):
    #wczytanie pliku json
    with open(json_file, 'r') as f:
        data = json.load(f)
    #listy obrazów i annotacji
    images = data['images']
    annotations = data['annotations']

    #kontrola istnienia folderu na maski i stworzenie go jeśli jej nie ma
    if not os.path.exists(mask_output_folder):
        os.makedirs(mask_output_folder)
    #pętla porusząjaca się po  
    for img in images:
        #tworzenie maski
        create_mask(img, annotations, mask_output_folder)

if __name__ == '__main__':
    i=0
    for x in dirs:
        original_image_dir = dirs_path + x + '/images'
        mask_output_folder = dirs_path + x + '/masks'
        json_file = json_files[i]
        i += 1
        main(json_file, mask_output_folder, original_image_dir)