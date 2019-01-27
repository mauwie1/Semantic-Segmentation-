import sys
import os
import skimage
import cv2
curdir = os.getcwd()
sys.path.append(os.path.join(curdir, "Mask_RCNN-master"))
#File that handles most of the mask work.
import masks
import pickle
# This method evaluates an image and creates 'masks', which semantically segment the image. It returns a dictionary
# in which each pixel is assigned to the appropriate mask, or no mask.
def getPixelMaskDict(img, output):
    pixel_mask_dict = {"noMask":[]}
    count=0
    while count<len(output['masks'][0][0]): #Create an empty list of pixels per mask, which eventually will include the pixels.
        pixel_mask_dict["Mask " + str(count+1)]=[]
        count+=1
    c = 0
    while c < len(img): # It puts the pixels in the appropriate mask list, where its mask value is True
        row = img[c]
        maskrow = output['masks'][c]
        c2 = 0
        while c2 < len(row):
            rgbval = row[c2]
            maskval = maskrow[c2]
            c3 = 0
            appended=False
            while c3 < len(maskval):
                if maskval[c3] == True:
                    pixel_mask_dict["Mask " + str(c3+1)].append(c * len(row) + c2)
                    appended=True
                c3 += 1
            if appended==False:
                pixel_mask_dict["noMask"].append(c * len(row) + c2)
            c2 += 1
        c += 1
    return pixel_mask_dict

# This method returns cropped images according to the boxes of the masks.
def getBoxes(img, output):
    # The rois parameter of the output indicates a box per mask. It includes two coordinates per mask, the first being
    # the top left corner of the box, the second being the bottom right.
    boxes = output['rois']
    cropped_images = []
    for box in boxes:
        topx = box[0]
        botx = box[2]
        lefty = box[1]
        righty = box[3]
        cropped_images.append(img[topx:botx, lefty:righty])
    return(cropped_images)

def get_Masks_and_Boxes(image):
    mask_output = masks.createMasks(image)
    boxes = getBoxes(image, mask_output)
    mask_dict = getPixelMaskDict(image, mask_output)
    return([mask_dict, boxes])


# Creates masks from an image and saves it to a pickle file, in addition to the boxes.
def create_boxes_and_mask(image_path):
    curdir = os.getcwd()
    try:
        img_path = os.path.join(curdir, image_path)
        image = cv2.imread(img_path)
    except: # If full path is specified
        image = cv2.imread(img_path)
    sys.stdout = open(os.devnull, 'w') # Prevents a lot of print statements
    segmentation_info = get_Masks_and_Boxes(image)
    sys.stdout = sys.__stdout__
    boxes= segmentation_info[1]
    c=0
    while c<len(boxes):
        cv2.imwrite("box" +str(c) + ".jpg", boxes[c])
        c+=1
    with open("mask_list.txt", 'wb') as file:
        pickle.dump(segmentation_info[0], file)


if __name__ == "__main__":
    create_boxes_and_mask(sys.argv[1])