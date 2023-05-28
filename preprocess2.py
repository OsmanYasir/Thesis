import numpy as np
import pytesseract
import argparse
import imutils
import cv2


def preprocess_image(image_path, output_path):

    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding to enhance the features
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Gaussian blur for noise reduction
    img = cv2.GaussianBlur(img, (5, 5), 0)


    # Normalize the image data to 0-1 range

    img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img = (img * 255).astype(np.uint8)

    # Save the processed image
    cv2.imwrite(output_path, img)

    return img



if __name__ == "__main__":
    path = "./Cropped/1edit.jpg"
    # test()
    processed_image = preprocess_image(path, './output_image.jpg')
