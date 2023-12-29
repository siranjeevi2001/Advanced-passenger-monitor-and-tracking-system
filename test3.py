import cv2
from pyzbar.pyzbar import decode
import numpy as np

def decoder(image):
	# gray image
	gray_image = cv2.cvtColor(image,0)

	#Decoder
	barcode = decode(gray_image)

	for obj in barcode:
		points = obj.polygon
		(x,y,w,h) = obj.rect
		pts = np.array(points, np.int32)
		pts.reshape([-1,1,2])
		cv2.polylines(image,[pts],True,(0,255,0),3)

		barcodeData = obj.data.decode('utf-8')
		barcodeType = obj.type
		string = "Data : " + barcodeData + " Type : " + barcodeType

		cv2.putText(frame,string,(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0), 2)
		print("Barcode: "+barcodeData +" | Type: "+barcodeType)


cap = cv2.VideoCapture(0)
while True:
	ret,frame = cap.read()
	decoder(frame)
	cv2.imshow('image',frame)
	code = cv2.waitKey(10)
	if code == ord('q'):
		break
