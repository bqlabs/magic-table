import cv2
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'def'

def transform_image(src, new_width, new_height, new_depth):
    limits = np.arange(0, 256, 256/new_depth)
    if limits[-1] != 255:
        limits = np.concatenate((limits, np.array([255])))
    lut = np.zeros((256, 1))
    j = 0
    #print limits

    for i in range(256):
        if i > limits[j]:
            j += 1
        lut[i, 0] = limits[j]


    dst = cv2.resize(src, (new_width, new_height))

    for i, col in enumerate(dst):
        for j, px in enumerate(col):
            dst[i, j, :] = [ lut[px[0]], lut[px[1]], lut[px[2]]]

    return dst


if __name__ == '__main__':
    # Load image
    file_path = 'Landscape_55.jpg'
    #file_path = 'Granger_Chart.jpg'
    #file_path = '/home/def/Documents/CoreXY/doc/With Legs.png'
    test_image = cv2.imread(file_path)

    # Process image
    processed = transform_image(test_image, 50, 38, 3)

    cv2.imshow('Result', processed)
    cv2.waitKey(-1)
    cv2.destroyAllWindows()

    plt.imshow(processed)
    plt.show()