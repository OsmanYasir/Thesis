import cv2
import numpy as np

def preprocess_image(image_path, outpath):
    # Step 1: Read the image
    img = cv2.imread(image_path)

    # Step 2: Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply thresholding
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Step 4: Remove noise using morphology operations
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)

    # Step 5: Apply dilation to connect the broken parts
    dilation = cv2.dilate(opening, kernel, iterations=1)

    # Step 7: Normalize the image
    normalized = cv2.resize(dilation, (1000, 1000), interpolation=cv2.INTER_LINEAR)

    cv2.imwrite(outpath, normalized)

    # Step 6: Return the processed image
    return normalized


if __name__ == "__main__":
    processed_image = preprocess_image('./imgs/1cropped.jpg')
    cv2.imwrite('./imgs/output_image.jpg', processed_image)