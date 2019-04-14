import cv2 as cv


def nothing(x):
    pass


def rotate_image(image, angle):
    (w, h) = image.shape
    center = (w // 2, h // 2)
    rotation_mat = cv.getRotationMatrix2D(center, angle, 1.0)

    angle_cos = abs(rotation_mat[0, 0])
    angle_sin = abs(rotation_mat[0, 1])

    # count width and height bounds
    w_rotated_not_cropped = int(w * angle_cos + h * angle_sin)
    h_rotated_not_cropped = int(w * angle_sin + h * angle_cos)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += w_rotated_not_cropped / 2 - center[0]
    rotation_mat[1, 2] += h_rotated_not_cropped / 2 - center[1]

    return cv.warpAffine(image, rotation_mat, (w_rotated_not_cropped, h_rotated_not_cropped))


def open_video():
    video = cv.VideoCapture(-1)

    if video.isOpened():
        while True:
            check, frame = video.read()
            if check:
                open_input_video_frame(frame)
                key = cv.waitKey(50)
                if key == ord('q'):
                    break
            else:
                print('Frame not available')
                print(video.isOpened())


def open_input_video_frame(frame):
    cv.namedWindow('result')

    cv.createTrackbar('minB', 'result', 0, 255, nothing)
    cv.createTrackbar('minG', 'result', 0, 255, nothing)
    cv.createTrackbar('minR', 'result', 0, 255, nothing)

    cv.createTrackbar('maxB', 'result', 0, 255, nothing)
    cv.createTrackbar('maxG', 'result', 0, 255, nothing)
    cv.createTrackbar('maxR', 'result', 0, 255, nothing)

    cv.createTrackbar('blurSize', 'result', 0, 20, nothing)

    minB = cv.getTrackbarPos('minB', 'result')
    minG = cv.getTrackbarPos('minG', 'result')
    minR = cv.getTrackbarPos('minR', 'result')
    maxB = cv.getTrackbarPos('maxB', 'result')
    maxG = cv.getTrackbarPos('maxG', 'result')
    maxR = cv.getTrackbarPos('maxR', 'result')

    result = frame.copy()
    blurSize = cv.getTrackbarPos('blurSize', 'result')

    if blurSize > 1 & blurSize % 2 == 1:
        result = cv.GaussianBlur(result, (blurSize, blurSize), 0)

    maskFrame = cv.inRange(result, (minB, minG, minR), (maxB, maxG, maxR))
    cv.imshow('mask', maskFrame)

    result = cv.bitwise_and(result, frame, mask=maskFrame)
    cv.imshow('result', result)


open_video()
cv.waitKey(0)
