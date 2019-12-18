from wand.image import Image
from wand.exceptions import DelegateError
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import numpy as np
import time
import argparse
import traceback

# class MemoryRelatedException(Exception):
#     pass

def save_images(pdf_file_path, output_folder, begin_page, end_page=200):
    
    assert begin_page > 0
    begin_page = begin_page - 1 #begin_page starts from 1, not 0.
    
    num_pages_per_split = 10
    
    idx = begin_page
    
    page = begin_page + 1 #page numbers to save are not 0-index based.
    page_until = begin_page

    try:
        with open(pdf_file_path, "rb") as f:
            inputpdf = PdfFileReader(f)

            for i in range(begin_page, end_page, num_pages_per_split):
                
                output = PdfFileWriter()

                last_page = i+num_pages_per_split
                if last_page >= inputpdf.numPages:
                    last_page = inputpdf.numPages

                idx += 1
                
                for j in range(i, last_page):
                    output.addPage(inputpdf.getPage(j))
                with open("temp_%s.pdf" % (page), "wb") as outputStream:
                    output.write(outputStream)
                
                temp_file = "temp_%s.pdf" % (page)
                
                with open(temp_file, "wb") as outputStream:
                    output.write(outputStream)

                print('Wrote {}'.format(temp_file))

                with Image(filename=temp_file, resolution=300) as image_pdf:
                    image_jpeg = image_pdf.convert('jpeg')

                    for img in image_jpeg.sequence: #[begin_page:begin_page+num_pages]:
                        nimg = Image(img)

                        nimg.save(filename=os.path.join(output_folder, 'page_{}.jpg'.format(page)))
                        
                        page += 1

                        #if page > 20:
                        #    raise Exception('testing')

                os.remove(temp_file)
                print('Done until {}.'.format(last_page))
                page_until = last_page

                
    except DelegateError:
        return page_until
    return "Done"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract PDF pages as JPEG images')
    parser.add_argument('pdf_file_path', help='Path of the PPM pdf file')
    parser.add_argument('output_folder', help='Path of the folder where pages will be extracted')
    parser.add_argument('begin_page', type=int, help='Start extraction from this page number')
    parser.add_argument('end_page', type=int, help='End extraction at this page')

    args = parser.parse_args()
    print(save_images(args.pdf_file_path, args.output_folder, args.begin_page, args.end_page))
    #print(1)
