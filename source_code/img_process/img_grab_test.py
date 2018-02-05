import cv2
import ImageGrab
import numpy

bbox = (100, 100, 100+800, 100+600)
im = ImageGrab.grab(bbox)

#convert the grab picture to cv2 format
cimg = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)
cv2.imshow('test', cimg)

cv2.waitKey(10000)