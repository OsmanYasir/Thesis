from PIL import Image
import pytesseract

custom_config = r'-l rus+kir out tsv'
print(pytesseract.image_to_string(Image.open('imgs/output_image.jpg'), config=custom_config))