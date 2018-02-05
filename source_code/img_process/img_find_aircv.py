import cv2
import aircv as ac
import ImageGrab
import numpy


def draw_circle(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('objDetect', imsrc)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


bbox = (100, 100, 1820, 980)
im = ImageGrab.grab(bbox)
#imsrc = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)

imsrc = cv2.imread('x1.jpg')
imobj = cv2.imread('x2.jpg')

# find the match position
pos = ac.find_template(imsrc, imobj)
print pos
if not pos is None:
    circle_center_pos = pos['result']
    circle_radius = 60
    color = (20, 200, 20)
    line_width = 3

    # draw circle
    draw_circle(imsrc, circle_center_pos, circle_radius, color, line_width)
