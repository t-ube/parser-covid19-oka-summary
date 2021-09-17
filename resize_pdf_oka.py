import PyPDF2
import sys

#pdf = sys.argv[1]
#out = sys.argv[2]

def resize(src,dst):
    pdf = PyPDF2.PdfFileReader(src)
    page0 = pdf.getPage(0)
    rate =  595.2 / float(page0.mediaBox[2])
    print(rate)

    page0.scaleBy(rate)
    writer = PyPDF2.PdfFileWriter()
    writer.addPage(page0)
    with open(dst, "wb+") as f:
        writer.write(f)
