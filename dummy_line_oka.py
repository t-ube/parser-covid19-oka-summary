from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader

def output_dummy_TypeA(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')

    '''
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(30.7, 29.9, 0.25, 4.8, 'F')
    linePDF.rect(35.4, 29.9, 0.25, 4.8, 'F')
    linePDF.rect(41.9, 29.9, 0.25, 4.8, 'F')
    linePDF.rect(30.7, 29.9, 11.2, 0.25, 'F')
    linePDF.rect(30.7, 34.6, 11.2, 0.25, 'F')
    '''
    '''
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(17.3, 29.3, 183, 0.25,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(17.3, 37.1, 183, 0.25,'F')
    linePDF.set_fill_color(0,0,0)
    '''

    '''
    linePDF.rect(26.7, 37, 0.25, 70.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(50, 37, 0.25, 70.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(65.8, 37, 0.25, 70.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(77.2, 37, 0.25, 70.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(90.1, 37, 0.25, 70.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(110.5, 37, 0.25, 70.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(120.4, 37, 0.25, 70.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(120.4, 37, 0.25, 195.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(157.7, 37, 0.25, 195.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(171.3, 37, 0.25, 195.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(186.4, 37, 0.25, 195.2,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(200, 37, 0.25, 195.2,'F')
    linePDF.set_fill_color(0,0,0)
    '''

    linePDF.rect(33.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(60.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(72.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(91.9, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(100.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)

    #for i in range(50):
    #    linePDF.set_fill_color(0,0,0)
    #    linePDF.rect(17.3, 42.3 + i*5.409, 183, 0.25,'F')

    linePDF.output(path, 'F')

def output_dummy_TypeB(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')

    linePDF.rect(38.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(65.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(77.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(96.9, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(105.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)

    linePDF.output(path, 'F')

def output_dummy_TypeC(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')

    linePDF.rect(36.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(63.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(75.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(94.9, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(103.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)

    linePDF.output(path, 'F')

def output_dummy_TypeD(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')

    linePDF.rect(36.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(63.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(75.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(95.9, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(105.7, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(36.0, 162.34, 73.25, 0.25,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(36.0, 166.83, 73.25, 0.25,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(36.0, 171.32, 73.25, 0.25,'F')
    linePDF.set_fill_color(0,0,0)

    linePDF.output(path, 'F')

def output_dummy_TypeE(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')

    linePDF.rect(32.0, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(66.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(78.5, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(98.9, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(113.3, 96.6, 0.25, 81.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(30.0, 162.34, 83.25, 0.25,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(30.0, 166.83, 83.25, 0.25,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(30.0, 171.32, 83.25, 0.25,'F')
    linePDF.set_fill_color(0,0,0)

    linePDF.output(path, 'F')

def output_mergePDF(linePdfPath,sourcePdfPath,mergePdfPath):
    outputPDF = PdfFileWriter()
    sourcePDF = PdfFileReader(open(sourcePdfPath, "rb"))
    linePDF = PdfFileReader(open(linePdfPath, "rb"))

    for pageNum in range(sourcePDF.numPages):
        if pageNum == 0:
            linePlace = linePDF.getPage(0)
            currentPage = sourcePDF.getPage(pageNum)
            currentPage.mergePage(linePlace)
            outputPDF.addPage(currentPage)
            break

    outputPDFStream = open(mergePdfPath, "wb")
    outputPDF.write(outputPDFStream)
    outputPDFStream.close()
