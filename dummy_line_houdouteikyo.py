from fpdf import FPDF
import PyPDF2

def resizePage0(src,dst):
    pdf = PyPDF2.PdfFileReader(src)
    page0 = pdf.getPage(0)
    rate =  595.2 / float(page0.mediaBox[2])
    print(rate)
    page0.scaleBy(rate)
    writer = PyPDF2.PdfFileWriter()
    writer.addPage(page0)
    with open(dst, "wb+") as f:
        writer.write(f)

def output_dummy_typeA(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')
    linePDF.rect(28.0, 18.6, 0.25, 259.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(50.5, 18.6, 0.25, 259.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(72.5, 18.6, 0.25, 259.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.output(path, 'F')

def output_dummy_typeB(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')
    linePDF.rect(33.0, 14.6, 0.25, 265.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(55.5, 14.6, 0.25, 265.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(77.5, 14.6, 0.25, 265.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.output(path, 'F')

def output_dummy_typeC(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')
    linePDF.rect(35.0, 12.6, 0.25, 269.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(57.5, 12.6, 0.25, 269.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(79.5, 12.6, 0.25, 269.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.output(path, 'F')

def output_dummy_typeD(path):
    linePDF = FPDF()
    linePDF.add_page(orientation='P', format='A4')
    linePDF.rect(37.0, 9.6, 0.25, 275.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(59.5, 9.6, 0.25, 275.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.rect(81.5, 9.6, 0.25, 275.5,'F')
    linePDF.set_fill_color(0,0,0)
    linePDF.output(path, 'F')

def output_mergePDF(linePdfPath,sourcePdfPath,mergePdfPath):
    outputPDF = PyPDF2.PdfFileWriter()
    sourcePDF = PyPDF2.PdfFileReader(open(sourcePdfPath, "rb"))
    linePDF = PyPDF2.PdfFileReader(open(linePdfPath, "rb"))

    for pageNum in range(sourcePDF.numPages):
        if pageNum != 0:
            linePlace = linePDF.getPage(0)
            currentPage = sourcePDF.getPage(pageNum)
            currentPage.mergePage(linePlace)
            outputPDF.addPage(currentPage)

    outputPDFStream = open(mergePdfPath, "wb")
    outputPDF.write(outputPDFStream)
    outputPDFStream.close()
