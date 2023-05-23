import fitz
import os

file_list = os.popen("ls *.pdf").read().strip().split("\n")
for file_name in file_list:
    base_name, ext_name = file_name.split(".")
    doc = fitz.open(file_name)
    os.mkdir(base_name)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc,xref)
            if pix.n < 5:
                pix.writePNG(f"./{base_name}/{base_name}-image-{i},{xref}")
            else:
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix.writePNG(f"./{base_name}/{base_name}-image-{i},{xref}")
                pix1 = None
            pix = None
