import cv2
import numpy as np
import os
import argparse

def transform(pos):
	pts = []
	n = len(pos)
	for i in range(n):
		pts.append(list(pos[i][0]))
	#print pts
	sums = {}
	diffs = {}
	tl = tr = bl = br = 0
	for i in pts:
		x = i[0]
		y = i[1]
		sum = x+y
		diff = y-x
		sums[sum] = i
		diffs[diff] = i
	sums = sorted(sums.items())
	diffs = sorted(diffs.items())
	n = len(sums)
	rect = [sums[0][1], diffs[0][1], diffs[n-1][1], sums[n-1][1]]
	#	   top-left   top-right   bottom-left   bottom-right

	h1 = np.sqrt((rect[0][0]-rect[2][0])**2 +
	             (rect[0][1]-rect[2][1])**2)  # height of left side
	h2 = np.sqrt((rect[1][0]-rect[3][0])**2 +
	             (rect[1][1]-rect[3][1])**2)  # height of right side
	h = max(h1, h2)

	w1 = np.sqrt((rect[0][0]-rect[1][0])**2 +
	             (rect[0][1]-rect[1][1])**2)  # width of upper side
	w2 = np.sqrt((rect[2][0]-rect[3][0])**2 +
	             (rect[2][1]-rect[3][1])**2)  # width of lower side
	w = max(w1, w2)

	#print '#',rect
	return int(w), int(h), rect


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# img = cv2.imread('C:\Users\Admin\Desktop\pic.jpg')
img = cv2.imread(args["image"])
r = 500.0 / img.shape[1]
dim = (500, int(img.shape[0] * r))
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
#img=cv2.resize(img,None,fx=.1,fy=.1,interpolation=cv2.INTER_CUBIC)
cv2.imshow('ORIGINAL', img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (11, 11), 0)
edge = cv2.Canny(gray, 100, 200)
# _, contours, _ = cv2.findContours(edge.copy(), 1, 1)
# _, contours = cv2.findContours(edge.copy(), 1, 1)
tmp = cv2.findContours(edge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = tmp[0] if len(tmp) == 2 else tmp[1]
n = len(contours)
max_area = 0
pos = 0
for i in contours:
	area = cv2.contourArea(i)
	if area > max_area:
		max_area = area
		pos = i
peri = cv2.arcLength(pos, True)
approx = cv2.approxPolyDP(pos, 0.02*peri, True)

size = img.shape
cv2.imshow('BILL', img)
w, h, arr = transform(approx)

pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
pts1 = np.float32(arr)
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (w, h))
#dst=dst.astype('uint8')*255
image = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
image = cv2.adaptiveThreshold(image, 255, 1, 0, 11, 2)
image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
cv2.imshow('IMAGE', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
