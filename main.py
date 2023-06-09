import datetime
import json
from os import listdir
from os.path import isfile, join
from PIL import Image
import pytesseract
import bill
import preprocess
import preprocess2
import cv2

from extUtils import *


def ocr(imgPath, imgName, output):
    custom_config = fr'-l rus+kir --psm 3 --oem 1'

    # img = Image.open(imgPath)
    img = preprocess2.preprocess_image(imgPath, "./out/" + get_time() + ".jpg")

    text = pytesseract.image_to_string(img, config=custom_config)
    print(text)

    my_bill = bill.Bill(imgName, extractamount(text), extractperiod(text), extractpaymentid(text),
                        extractorganization(text))

    with open(fr'./out/bill {output}', 'a', encoding='utf8') as f:
        json.dump(my_bill.__dict__, f, ensure_ascii=False, indent=0)
        f.write("\n\n")

    with open(fr'./out/textbill {output}', 'a', encoding='utf8') as f:
        f.write(text)
        f.write("\n\n")
        json.dump(my_bill.__dict__, f, ensure_ascii=False, indent=0)
        f.write("\n\n\n")

    print("\n", my_bill, "\n")


def get_time():
    now = datetime.datetime.now()
    now = now.__str__().replace(" ", "T").replace(":", "-")
    return now


def ocrDir(path):
    imgs = [f for f in listdir(path) if isfile(join(path, f))]
    print(imgs)
    now = get_time()
    for img in imgs:
        ocr(fr'{path}/{img}', img, fr"{now}.json")


if __name__ == "__main__":
    path = "./single2"
    ocrDir(path)
    # ocr(path,"name","out.json")
