import os
import glob
import sys
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import rembg

def preprocess_image(path,rembg_model='u2net',size=256,border_ratio=0.2,recenter=True):
    session = rembg.new_session(model_name=rembg_model)

    if os.path.isdir(path):
        print(f'[INFO] processing directory {path}...')
        files = glob.glob(f'{path}/*')
        out_dir = path
    else: # isfile
        files = [path]
        out_dir = os.path.dirname(path)
    
    for file in files:

        out_base = os.path.basename(file).split('.')[0]
        out_rgba = os.path.join(out_dir, out_base + '_rgba.png')

        # load image
        print(f'[INFO] loading image {file}...')
        image = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        
        # carve background
        print(f'[INFO] background removal...')
        carved_image = rembg.remove(image, session=session) # [H, W, 4]
        mask = carved_image[..., -1] > 0

        # recenter
        if recenter:
            print(f'[INFO] recenter...')
            final_rgba = np.zeros((size, size, 4), dtype=np.uint8)
            
            coords = np.nonzero(mask)
            x_min, x_max = coords[0].min(), coords[0].max()
            y_min, y_max = coords[1].min(), coords[1].max()
            h = x_max - x_min
            w = y_max - y_min
            desired_size = int(size * (1 - border_ratio))
            scale = desired_size / max(h, w)
            h2 = int(h * scale)
            w2 = int(w * scale)
            x2_min = (size - h2) // 2
            x2_max = x2_min + h2
            y2_min = (size - w2) // 2
            y2_max = y2_min + w2
            final_rgba[x2_min:x2_max, y2_min:y2_max] = cv2.resize(carved_image[x_min:x_max, y_min:y_max], (w2, h2), interpolation=cv2.INTER_AREA)
            
        else:
            final_rgba = carved_image
        
        # write image
        cv2.imwrite(out_rgba, final_rgba)