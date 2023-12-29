# camera.py

import cv2
import PIL.Image
from PIL import Image
import argparse
import shutil
class VideoCamera3(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        
        self.video = cv2.VideoCapture(0)
        self.k=1
        # initialize the cv2 QRCode detector
        self.detector = cv2.QRCodeDetector()
       
    
    def __del__(self):
        self.video.release()
        
    
    def get_frame(self):
        success, img = self.video.read()
        data, bbox, _ = self.detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if bbox is not None:
            # display the image with lines
            for i in range(len(bbox)):
                # draw all lines
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            if data:
                print("[+] QR Code detected, data:", data)

                ff=open("data.txt","w")
                ff.write(data)
                ff.close


        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
