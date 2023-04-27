import cv2
import numpy as np
import pytesseract
from PIL import Image
from scipy.ndimage import interpolation as inter


# Replace this with the path to your Tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(threshold, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    return inter.rotate(image, best_angle, reshape=False)


def skeletonize(image):
    size = np.size(image)
    skeleton = np.zeros(image.shape, np.uint8)

    ret, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    done = False
    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

    return skeleton


def preprocess_image(image_path, output_path):
    image = cv2.imread(image_path)

    # Correct skew
    corrected_skew = correct_skew(image)
    # cv2.imwrite(output_path.replace("T", "1"), corrected_skew)

    # Convert the image to grayscale
    gray = cv2.cvtColor(corrected_skew, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(output_path.replace("T", "2"), gray)

    # Apply adaptive thresholding
    threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # cv2.imwrite(output_path.replace("T", "3"), threshold)

    # Apply a slight Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(threshold, (5, 5), 0)
    # cv2.imwrite(output_path.replace("T", "4"), blurred)

    # Dilate the image to fill gaps
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(blurred, kernel, iterations=1)
    # cv2.imwrite(output_path.replace("T", "5"), dilated)

    # Skeletonize the image
    skeleton = skeletonize(dilated)

    # Save the preprocessed image
    cv2.imwrite(output_path, skeleton)

    return skeleton


def perform_ocr(preprocessed_image_path):
    image = Image.open(preprocessed_image_path)
    text = pytesseract.image_to_string(image)
    return text


def main():
    input_image_path = './imgs/1.jpg'
    output_image_path = 'preprocessed_image.jpg'

    preprocessed_image_path = preprocess_image(input_image_path, output_image_path)
    extracted_text = perform_ocr(preprocessed_image_path)

    print("Extracted Text:")
    print(extracted_text)


if __name__ == "__main__":
    main()
