from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader

def output_dummy(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(42.3, 33.9, 0.25, 107.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(86.9, 33.9, 0.25, 107.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(114.9, 33.9, 0.25, 107.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(145.4, 33.9, 0.25, 107.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(162.7, 33.9, 0.25, 107.4,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(42.3, 137.1, 123.4, 0.25,'F')
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
