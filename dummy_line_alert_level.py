from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader

def output_dummy(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(20.3, 120.9, 0.75, 80.6,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(38.3, 120.9, 0.75, 80.6,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(45.3, 120.9, 0.75, 80.6,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(128.4, 120.9, 0.5, 80.6,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(156.7, 120.9, 0.5, 80.6,'F')
    linePDF.set_fill_color(0,0,0)

    linePDF.rect(20.3, 120.9, 136.4, 0.5,'F')
    linePDF.set_fill_color(0,0,0)

    for i in range(8):
        linePDF.rect(20.3, 134.9 + i * 9.5, 136.4, 0.5,'F')
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
