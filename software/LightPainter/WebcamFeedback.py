import cv2
import numpy as np
import optparse

#########################################################
# WebcamFeedback                                        #
#########################################################
# Simple program to emulate a long-exposure camera shot #
#                                                       #
# Usage:                                                #
#   - Press Esc to exit without saving file             #
#   - Press q to save the current image and exit        #
#   - Press r to reset the current image                #
#########################################################

__author__ = 'def'


if __name__ == '__main__':
    # Parse command-line parameters
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-o", "--output", dest="output_file", default="test.png", type="string",help="Output file in which the shot will be saved")
    (options, args) = parser.parse_args()
    output_file = options.output_file

    # Start webcam
    webcam = cv2.VideoCapture()
    webcam.open(1)

    # Init image
    dummy, final_image = webcam.read()
    final_image = np.zeros( final_image.shape, dtype = np.float64)

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
        elif k == ord('r'):
            # Reset image:
            dummy, final_image = webcam.read()
            final_image = np.zeros( final_image.shape, dtype = np.float64)

    cv2.destroyAllWindows()
    cv2.imwrite(output_file, final_image)


