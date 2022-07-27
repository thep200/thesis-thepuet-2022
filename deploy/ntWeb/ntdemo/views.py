import json
import os
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from ntdemo.forms import UserImage
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

thresh = 100
DPI = [300]
inch_to_mm = 25.4

root_path = 'C:/Users/Thep Ho/Desktop/Thesis/deploy/ntWeb/ntdemo/static/images/'

# Create your views here.
def index(request):
    form = UserImage()
    return render(request, 'index.html', {'form': form})

def image_request(request):
    path_img = ''
    if request.method == 'POST':
        form = UserImage(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            path_img = instance.image.path

    xCrop = int(request.POST.get('xCrop'))
    yCrop = int(request.POST.get('yCrop'))

    img = cropImage(path_img, xCrop-456, yCrop-128)
    # plt.imsave(root_path + 'nt-root-crop.png', img)
    single_img = prepareImage(root_path + 'nt-root-crop.png')

    premsk = unet_predict(single_img)
    plt.imsave(root_path + 'nt-root-pred.png', premsk)
    nt = ms_nt(root_path + 'nt-root-pred.png')

    return HttpResponse(nt, content_type="application/json")


def cropImage(image_path, xCrop, yCrop):
    image = plt.imread(image_path)
    height, width = image.shape[:2]

    if (xCrop + 256 > width):
        xCrop = xCrop + (width - (xCrop + 256))
    else:
        xCrop = 0 if xCrop - 30 < 0 else xCrop - 30

    if (yCrop + 256 > height):
        yCrop = yCrop + (height - (yCrop + 256))
    else:
        yCrop = 0 if yCrop - 30 < 0 else yCrop - 30
    return image[yCrop:yCrop+256, xCrop:xCrop+256, :]

def prepareImage(image_path):
    single_img = Image.open(image_path).convert('RGB')
    single_img = single_img.resize((256, 256))
    single_img = np.reshape(single_img, (256, 256, 3))
    single_img = single_img/256.
    return single_img

def unet_predict(image):
    # unet = keras.models.load_model('C:/Users/Thep Ho/Desktop/Thesis/exported-model/unet-7-256x256-25ep-94%.h5')
    unet = keras.models.load_model('C:/Users/Thep Ho/Desktop/Thesis/exported-model/unet-256x256-dataAug-50ep-99%.h5')
    img = image[np.newaxis, ...]
    pred_y = unet.predict(img)
    pred_mask = tf.argmax(pred_y[0], axis=-1)
    return pred_mask

def drawLine(img, Vx, Vy, Px, Py):
    _, cols = img.shape[:2]
    lefty = int((-Px*Vy/Vx) + Py)
    righty = int(((cols-Px)*Vy/Vx)+Py)
    cv2.line(img, (cols-1, righty), (0, lefty), (0, 255, 0), 1)

# standard
def mDistance(x1, y1, x2, y2):
    return ((((x1 - x2)/DPI[0])**2 + ((y1 - y2)/DPI[0])**2)**0.5)*inch_to_mm

def ms_nt(name_image):
    img = Image.open(name_image).convert('RGB')
    img = np.reshape(img, (256, 256, 3))
    #convert img to grey
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # set a thresh
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

    #find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # tìm vector và điểm của fitline
    [fit_line_vx, fit_line_vy, fit_line_x, fit_line_y] = cv2.fitLine(contours[0], cv2.DIST_L2, 0, 0.01, 0.01)

    # Kẻ đường vuông góc với fitline
    percentage_line_vx, percentage_line_vy = -fit_line_vy, fit_line_vx

    # contours mask
    img_contours_mask = np.zeros(img.shape, np.uint8)
    contour_img = np.zeros(img.shape, np.uint8)

    cv2.drawContours(img_contours_mask, contours, -1, (0, 255, 0), 1)
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 1)
    # region

    # centroid, area and max width, height
    centroid = []
    for c in contours:
        # find the center of the contour
        m = cv2.moments(c)
        centroid.append(int(m['m10']/m['m00']))
        centroid.append(int(m['m01']/m['m00']))

        # extract roi
        x, y, w, h = cv2.boundingRect(c)
        break

    cv2.circle(img_contours_mask, (centroid[0], centroid[1]), 2, (255, 0, 0), -1)

    line_mask = np.zeros(img.shape, np.uint8)
    drawLine(line_mask, percentage_line_vx, percentage_line_vy, centroid[0], centroid[1])
    img_contours_mask = np.array(img_contours_mask)
    line_mask = np.array(line_mask)

    rows, cols, _ = img.shape
    nt_points = []

    for i in range(0, rows):
        for j in range(0, cols):
            if img_contours_mask[i][j][1] == 255 and line_mask[i][j][1] == 255:
                nt_points.append([i, j])

    if (len(nt_points) == 1):
        nt_points.append([centroid[1], centroid[0]])

    (x1, y1, x2, y2) = (nt_points[0][0], nt_points[0][1], nt_points[1][0], nt_points[1][1])

    return round(mDistance(x1, y1, x2, y2), 3)
