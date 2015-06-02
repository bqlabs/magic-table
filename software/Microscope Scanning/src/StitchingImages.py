import cv2
import numpy as np

__author__ = 'def'

def main():
    # Load images:
    image1 = cv2.imread("../images/scan01.jpg")
    image2 = cv2.imread("../images/scan02.jpg")

    # Convert them to b/w:
    image1_bw = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_bw = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Feature extraction
    orb = cv2.ORB()
    kp = orb.detect(image1_bw)
    for point in [(int(x), int(y)) for x, y in [ i.pt for i in kp]]:
        print point
        cv2.circle(image1,point,2,(255, 0, 0),-1)
    cv2.imshow('img',image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Setting up samples and responses for kNN
    #samples = np.array(descriptors)
    responses = np.arange(len(kp), dtype=np.float32)

    # kNN training
    knn = cv2.KNearest()
    knn.train(samples, responses)

    # Now loading a template image and searching for similar keypoints
    keys,desc = orb.detect(image2)

    for h,des in enumerate(desc):
        des = np.array(des,np.float32).reshape((1,128))
        retval, results, neigh_resp, dists = knn.find_nearest(des,1)
        res,dist =  int(results[0][0]),dists[0][0]

        if dist<0.1: # draw matched keypoints in red color
            color = (0,0,255)
        else:  # draw unmatched in blue color
            print dist
            color = (255,0,0)

        #Draw matched key points on original image
        x,y = kp[res].pt
        center = (int(x),int(y))
        cv2.circle(image1,center,2,color,-1)

        #Draw matched key points on template image
        x,y = keys[h].pt
        center = (int(x),int(y))
        cv2.circle(image2,center,2,color,-1)

    cv2.imshow('img',image1)
    cv2.imshow('tm',image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
