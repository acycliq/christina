import skimage.io
import numpy as np
import pandas as pd
from PIL import Image, ImageOps, ImageDraw
from skimage.transform import rescale, resize, downscale_local_mean
import diplib as dip
import os
import logging

def normalize_img(img, normalize=[0,99.9]):
    perc1, perc2 = np.percentile(img, list(normalize))
    img = img - perc1
    img /= (perc2-perc1)
    img = img * 255.0
    img = np.clip(img, 0, 255)
    img = img.astype(np.uint8)
    return img


def stack_to_images(d):
    label = d[0]
    filename = d[1]
    dapi = skimage.io.imread(filename)
    n = dapi.shape[0]
    for i in range(n):
        page = normalize_img(dapi[i])
        img = Image.fromarray(page.astype(np.uint8))
        target_file = os.path.join(os.path.join('pages', label, 'page_%s.jpg' % str(i).zfill(3)))
        if not os.path.exists(os.path.dirname(target_file)):
            os.makedirs(os.path.dirname(target_file))
        img.save(target_file)
        print('page_%d.jpg saved at %s' % (i, target_file))

        scale = 0.5
        img_resized = img.resize([int(scale * s) for s in img.size], Image.ANTIALIAS)
        target_file = os.path.join(os.path.join('pages', label, 'resized_page_%s.jpg' % str(i).zfill(3)))
        img_resized.save(target_file)
        print('resized_page_%d.jpg saved at %s' % (i, target_file))


def app():
    print('hi')


if __name__ == "__main__":
    dic = {
        # 'dapi': r"F:\data\Christina\microglia\DAPI_retiled_image.tif",
        'microglia': r"F:\data\Christina\microglia\microglia_ WT997_icvAB_Iba1_retiled.tif"
    }
    for di in dic.items():
        # img_path = r"F:\data\Christina\microglia\DAPI_retiled_image.tif"
        stack_to_images(di)
    # img = skimage.io.imread(img_path)
    # nimg = normalize_img(img)
    # im = Image.fromarray(nimg)
    # im.save("your_file.jpeg")

    app()
