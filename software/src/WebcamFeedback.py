import cv2
import numpy as np
import time as t

__author__ = 'def'


if __name__ == '__main__':
    webcam = cv2.VideoCapture()
    webcam.open(1)

    dummy, final_image = webcam.read()
    final_image = np.zeros( final_image.shape, dtype = np.float64)
    time = 0

    while True:
        dummy, new_image = webcam.read()
        dummy, mask = cv2.threshold(new_image, 125, 255, cv2.THRESH_BINARY)
        mask = mask[:, :, 0] | mask[:,:,1] | mask[:, :, 2]

        #cv2.accumulateWeighted(new_image, final_image, 0.5)
        cv2.accumulate(new_image, final_image, mask)

        cv2.imshow("Result", final_image.astype(np.uint8))
        k = cv2.waitKey(30) & 0xFF
        if k == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.imwrite("test.png", final_image)


