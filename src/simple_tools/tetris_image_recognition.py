from matplotlib import pyplot as plt

import cv2 as cv

print(cv.__version__)


def nothing(x):
    pass


image = cv.imread('/home/anton/PycharmProjects/opencv-tools/src/picture_2.jpg')
(h, w, d) = image.shape
print("width = {}, height = {}, depth = {}".format(w, h, d))
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
plt.title("Input image")

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(gray, cv.COLOR_BGR2RGB))
plt.title('Grayscale image')
plt.show()

cv.namedWindow('gray')
cv.imshow('gray', gray)

cv.namedWindow('gray_canny')
cv.imshow('gray_canny', gray)

cv.namedWindow('gray_thresh')
cv.imshow('gray_thresh', gray)

while True:
    cv.createTrackbar('blurSize', 'gray', 5, 20, nothing)
    blurSize = cv.getTrackbarPos('blurSize', 'gray')
    gray_blur = gray.copy()
    if blurSize > 1 & blurSize % 2 == 1:
        gray_blur = cv.GaussianBlur(gray_blur, (blurSize, blurSize), 0)
    cv.imshow('gray', gray_blur)

    cv.createTrackbar('min_gray', 'gray_canny', 0, 255, nothing)
    cv.createTrackbar('max_gray', 'gray_canny', 65, 255, nothing)
    min_gray = cv.getTrackbarPos('min_gray', 'gray_canny')
    max_gray = cv.getTrackbarPos('max_gray', 'gray_canny')

    image_canny = cv.Canny(gray_blur, min_gray, max_gray)
    cv.imshow('gray_canny', image_canny)

    cv.createTrackbar('min_gray', 'gray_thresh', 240, 255, nothing)
    cv.createTrackbar('max_gray', 'gray_thresh', 255, 255, nothing)
    min_gray_thresh = cv.getTrackbarPos('min_gray', 'gray_thresh')
    max_gray_thresh = cv.getTrackbarPos('max_gray', 'gray_thresh')

    gray_thresh = cv.threshold(gray_blur, min_gray_thresh, max_gray_thresh, cv.THRESH_BINARY_INV)[1]
    gray_thresh = cv.erode(gray_thresh, None, iterations=5)
    cv.imshow("gray_thresh", gray_thresh)

    output_contours = image.copy()
    contours, hierarchy = cv.findContours(gray_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cv.drawContours(output_contours, [cnt], 0, (240, 20, 159), 5)

    cv.putText(output_contours, "I found {} objects".format(len(contours)), (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7,
               (240, 20, 159), 2)
    cv.imshow("output_contours", output_contours)

    key = cv.waitKey(50)
    if key == ord('q'):
        break
