import pickle
import cv2
import math
import numpy as np
from PIL import Image

# Merges two or more images, according to the values in the mask dictionary. If the amount of images is not equal to
# the amount in the mask dictionary, it raises an error
def mergeImages(mask_dict, image_list):
    original_img = image_list[0]
    newimg = np.full(shape=(len(original_img), len(original_img[0]), 3), dtype=np.uint8,fill_value=255)
    no_mask_vals = mask_dict["noMask"]
    print(len(mask_dict.keys()))
    if len(image_list[1:])==len(mask_dict.keys())-1:
        c=1
        for pix in no_mask_vals:
            row=math.floor(pix/len(original_img[0]))
            pos = pix%len(original_img[0])
            newimg[row][pos] = original_img[row][pos]
        while c<len(mask_dict.keys()):
            mask_vals = mask_dict["Mask " + str(c)]
            for pix in mask_vals:
                row=math.floor(pix/len(original_img[0]))
                pos = pix%len(original_img[0])
                try:
                    newimg[row][pos] = image_list[c][row][pos]
                except:
                    pass
            c+=1
        img = Image.fromarray(newimg)
        img.show()
        cv2.waitKey(0)
        return newimg
    else:
        print("amount of input images not equal to mask amount")

# Creates a white image that is as big as the input, used for zero masking
def getWhiteImg(img):
    newimg = np.full(shape=(len(img), len(img[0]), 3), dtype=np.uint8, fill_value=255)
    img = Image.fromarray(newimg)
    cv2.imwrite("white_img.jpg", newimg)
    return img

# The path of the images has to be put in manually in the code
if __name__ == "__main__":
    mask_dict = pickle.load(open("mask_list.txt", "rb"))
    image_list = []
    image_list.append(cv2.imread("Images/pizza.jpg"))
    image_list.append(cv2.imread("Image_data\giraffe\giraffe.png"))
    white_img = getWhiteImg(image_list[0])
    white_img = cv2.imread("white_img.jpg")
    zero_mask = mergeImages(mask_dict, [image_list[0], white_img])
    cv2.imwrite("zero_mask.jpg", zero_mask)