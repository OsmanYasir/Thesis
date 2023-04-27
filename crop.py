import cv2
import matplotlib
from matplotlib import pyplot as plt

image = cv2.imread("imgs/1.jpg")
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

color = ('b','g','r')
fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(1,2,1)
ax.imshow(image)
ax1 = fig.add_subplot(1,2,2)

for i,col in enumerate(color):
    histogram = cv2.calcHist([image],[i],None,[256],[0,256])
    ax1.plot(histogram,color = col)
    ax1.set_xlim([0,256])
    blurred_gray_image = cv2.blur(gray_image, (21, 21))


