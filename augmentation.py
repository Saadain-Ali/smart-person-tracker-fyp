import cv2
from keras_preprocessing.image import image_data_generator, array_to_img, img_to_array, load_img
import os
import glob



path = "dataset/62645"


# Augmentation

def change_brightness(img, value=40):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  h, s, v = cv2.split(hsv)
  v = cv2.add(v,value)
  v[v > 255] = 255
  v[v < 0] = 0
  final_hsv = cv2.merge((h, s, v))
  img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
  return img

datagen = image_data_generator.ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.7,
    horizontal_flip=True,
    fill_mode='nearest',
    preprocessing_function = change_brightness
)

for file in glob.glob("*.jpg"):
    img = load_img(file)
    x = img_to_array(img)
    x = x.reshape((1,)+x.shape)

    i = 0
    for batch in datagen.flow(x, batch_size=1, save_to_dir=path, save_prefix='aug', save_format='jpg'):
        i += 1
        print(i)
        if i > 4:
            break


from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
import mxnet as mx  # used version '1.0.0' at time of writing
import numpy as np

mx.random.seed(42) # set seed for repeatability

def plot_mx_array(array):
    """
    Array expected to be height x width x 3 (channels), and values are floats between 0 and 255.
    """
    assert array.shape[2] == 3, "RGB Channel should be last"
    imshow((array.clip(0, 255)/255).asnumpy())

count = 0 


for file in glob.glob("*.jpg"):
    print(file)
    example_image = mx.image.imread(file)
    assert example_image.dtype == np.uint8
    example_image = example_image.astype("float32")    
    plot_mx_array(example_image)
    example_image_copy = example_image.copy()
    
    
    aug_list = [
        mx.image.ColorJitterAug(brightness=1, contrast=1, saturation=1),
        mx.image.HueJitterAug(hue=0.5),
        mx.image.RandomGrayAug(p=1),
        mx.image.ColorNormalizeAug(mean=mean, std=stdev)
    ]
    aug = mx.image.RandomOrderAug(aug_list)
    aug_image = aug(example_image_copy)
    # plot_mx_array(aug_image)
    v = aug_image.asnumpy()
    cv2.imwrite(f'augm_{count}.jpg',v)
    count= count+1

    example_image_copy = example_image.copy()
    mean = [0, 10, 20]
    stdev = [1, 2, 3] 
    aug = mx.image.ColorNormalizeAug(mean=mean, std=stdev)
    aug_image = aug(example_image_copy)
    # plot_mx_array(aug_image)

    v = aug_image.asnumpy()
    cv2.imwrite(f'augm_{count}.jpg',v)
    count= count+1
    
    if count == 1:
        break


