from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader

def output_dummy(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(32.3, 33.9, 0.25, 127.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(76.9, 33.9, 0.25, 127.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(114.9, 33.9, 0.25, 127.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(145.4, 33.9, 0.25, 127.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(178.7, 33.9, 0.25, 127.4,'F')
    linePDF.set_fill_color(0,0,0)
    #linePDF.rect(30.3, 153.5, 150.4, 0.25,'F')
    for num in range(16):
        if num > 5:
            temp = 160.1 - (7.7 * num)
        else:
            temp = 160.1 - (7.4 * num)
        linePDF.rect(30.3, temp, 150.4, 0.25,'F')

    linePDF.set_fill_color(0,0,0)

    #for i in range(20):
    #    linePDF.set_fill_color(0,0,0)
    #    linePDF.rect(39.3, 36.7 + i * 6.2, 130, 0.25,'F')

    linePDF.output(path, 'F')

def output_mergePDF(linePdfPath,sourcePdfPath,mergePdfPath):
    outputPDF = PdfFileWriter()
    sourcePDF = PdfFileReader(open(sourcePdfPath, "rb"))
    linePDF = PdfFileReader(open(linePdfPath, "rb"))

    for pageNum in range(sourcePDF.numPages):
        linePlace = linePDF.getPage(0)
        currentPage = sourcePDF.getPage(pageNum)
        currentPage.mergePage(linePlace)
        outputPDF.addPage(currentPage)

    outputPDFStream = open(mergePdfPath, "wb")
    outputPDF.write(outputPDFStream)
    outputPDFStream.close()
