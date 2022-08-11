# pip install opencv-python
# pip install numpy
import cv2
import sys
import numpy as np

#https://www.analyticsvidhya.com/blog/2021/07/colour-quantization-using-k-means-clustering-and-opencv/
def quantimage(image,k):
    i = np.float32(image).reshape(-1,3)
    condition = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,1.0)
    ret,label,center = cv2.kmeans(i, k , None, condition,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    final_img = center[label.flatten()]
    final_img = final_img.reshape(image.shape)
    return final_img, center

def process(infilename, outwidth_inches, headsize_inches, heads_per_pixel, outheight_inches, color_count):
    # read the image
    img = cv2.imread(infilename,cv2.IMREAD_COLOR)
    cv2.imshow('original',img)
    inpixels_x, inpixels_y, channels = np.shape(img)
    cropped = img
    # crop
    # if we need to crop widthwize
    if outwidth_inches/outheight_inches < inpixels_x/inpixels_y:
        print("cropping widthwize")
        out_pixel_size_inches = outheight_inches/inpixels_y
        print("pixel size " + str(out_pixel_size_inches))
        newWidth_pixels = int(outwidth_inches/out_pixel_size_inches)
        border = int((inpixels_y - newWidth_pixels)/2)
        print("removing " + str(border) + " pixels from left and right")
        # numpy slicing
        if border:
            cropped = img[:, border:-border]
    # or heightwize
    else:
        print("cropping heightwize")
        out_pixel_size_inches = outwidth_inches/inpixels_x
        print("pixel size " + str(out_pixel_size_inches))
        newHeight_pixels = int(outheight_inches/out_pixel_size_inches)
        border = int((inpixels_x - newHeight_pixels)/2)
        print("removing " + str(border) + " pixels from top and bottom")
        # numpy slicing
        if border:
            cropped = img[border:-border,:]
    
    cv2.namedWindow('cropped', cv2.WINDOW_NORMAL)  #  2. use 'normal' flag
    cv2.imshow('cropped',cropped)
    cv2.resizeWindow('cropped', inpixels_x, inpixels_y)
    
    # pixelate / resize
    desired_inches_per_pixel = headsize_inches * heads_per_pixel
    desired_pixels_x        = int(outwidth_inches  / desired_inches_per_pixel)
    desired_pixels_y        = int(outheight_inches / desired_inches_per_pixel)
    pixelated = cv2.resize(cropped, (desired_pixels_x, desired_pixels_y), interpolation = cv2.INTER_AREA)
    cv2.namedWindow('pixelated', cv2.WINDOW_NORMAL)  #  2. use 'normal' flag
    cv2.imshow('pixelated',pixelated)
    cv2.resizeWindow('pixelated', inpixels_x, inpixels_y)
    
    # quantize colors (palette reduction)
    quantized, centers = quantimage(pixelated, color_count)
    print("final color palette " + str(centers))
    cv2.namedWindow('quantized', cv2.WINDOW_NORMAL)  #  2. use 'normal' flag
    cv2.imshow('quantized',quantized)
    cv2.resizeWindow('quantized', inpixels_x, inpixels_y)
    
    # resize by heads_per_pixel
    final_pixels_x        = int(desired_pixels_x * heads_per_pixel)
    final_pixels_y        = int(desired_pixels_y * heads_per_pixel)
    final = cv2.resize(quantized, (final_pixels_x, final_pixels_y), interpolation = cv2.INTER_AREA)
    
    # raster GCODE
    # for each color
    for i, center in enumerate(centers):
        
        header = """
        PUT INITIALIZATION GCODE HERE
        """

        gcode = header
        for x in range(final_pixels_x):
            for y in range(final_pixels_y):
                xpos = x * headsize_inches
                ypos = y * headsize_inches
                # if that pixel is here, lower the head
                if np.array_equal(final[y,x], center):
                    zpos = -1
                else:
                    zpos = 1
                gcode += "    GOTO X=" + str(xpos)   + ", Y=" + str(ypos) + ", Z=" + str(zpos) + ";\n" 
                gcode += "    GOTO X=" + str(xpos+1) + ", Y=" + str(ypos) + ", Z=" + str(zpos) + ";\n" 
                    
        footer = """
        PUT FINISHING GCODE HERE
        """
        gcode +=footer

        with open(str(center) + ".gcode", "w+") as f:
            f.write(gcode)
        
    
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image

if __name__ == "__main__":
    outwidth_inches = 20
    outheight_inches = 24
    headsize_inches = 0.1
    heads_per_pixel = 2
    color_count     = 5
    infilename = "Lenna.png"
    for i, arg in enumerate(sys.argv):
        if arg == "-w" or arg == "--width":
            outwidth_inches = int(sys.argv[i+1])
        if arg == "-h" or arg == "--height":
            outheight_inches = int(sys.argv[i+1])
        if arg == "-i" or arg == "--image":
            infilename = sys.argv[i+1]
        if arg == "-s" or arg == "--headsize":
            headsize_inches = float(sys.argv[i+1])
        if arg == "-p" or arg == "--headsperpixel":
            heads_per_pixel = int(sys.argv[i+1])
        if arg == "-c" or arg == "--colors":
            color_count = int(sys.argv[i+1])
            
    process(infilename = infilename, 
            outwidth_inches = outwidth_inches, 
            headsize_inches = headsize_inches, 
            outheight_inches = outheight_inches,
            color_count = color_count,
            heads_per_pixel = heads_per_pixel
           )
