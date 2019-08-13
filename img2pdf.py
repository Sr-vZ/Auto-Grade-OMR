from PIL import Image
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
# ap.add_argument("-o", "--out", required=True, help="filename for the pdf")
args = vars(ap.parse_args())

# im1 = Image.open("/Users/apple/Desktop/bbd.jpg")
# im2 = Image.open("/Users/apple/Desktop/bbd1.jpg")
# im3 = Image.open("/Users/apple/Desktop/bbd2.jpg")
# im_list = [im2, im3]
print(args["image"][:-4])
# print(args["out"])
img = Image.open(args["image"])

pdf_filename = str(args["image"][:-3]+"pdf")

img.save(pdf_filename, "PDF", resolution=100.0,save_all=True)
