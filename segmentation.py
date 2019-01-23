import sys
import os
import skimage

curdir = os.getcwd()
sys.path.append(os.path.join(curdir, "Mask_RCNN-master"))
#File that handles most of the mask work.
import masks


# This method evaluates an image and creates 'masks', which semantically segment the image. It returns a dictionary
# in which each pixel is assigned to the appropriate mask, or no mask.
def getPixelMaskDict(img):
    output = masks.createMasks(image)
    pixel_mask_dict = {"noMask":[]}
    count=0
    while count<len(output['masks'][0][0]): #Create an empty list of pixels per mask, which eventually will include the pixels.
        pixel_mask_dict["Mask " + str(count+1)]=[]
        count+=1
    c = 0
    while c < len(image): # It puts the pixels in the appropriate mask list, where its mask value is True
        row = image[c]
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

if __name__ == "__main__":
    image = skimage.io.imread(os.path.join(curdir, sys.argv[1]))
    dict = getPixelMaskDict(image)
    print(dict)