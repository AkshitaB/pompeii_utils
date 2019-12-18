# pompeii_utils

Installations required: Wand, OpenCV, Flask


1. Extract PDF pages as images for processing.

```usage: extract_pages.py [-h] pdf_file_path output_folder begin_page end_page

Extract PDF pages as JPEG images

positional arguments:
  pdf_file_path  Path of the PPM pdf file
  output_folder  Path of the folder where pages will be extracted
  begin_page     Start extraction from this page number
  end_page       End extraction at this page

optional arguments:
  -h, --help     show this help message and exit
```

Eg. python extract_pages.py ../PPM/PDFs/PPM-4ocr2.pdf ../page_images/PPM4 22 25

2. Auto extract pictures

```usage: auto_extraction.py [-h] raw_folder output_folder

Extract pictures from PDF page images

positional arguments:
  raw_folder     Path of PDF page images
  output_folder  Path of the folder where pictures will be extracted

optional arguments:
  -h, --help     show this help message and exit
```

Eg. python auto_extraction.py ../page_images/PPM4 ../final_extraction/PPM4

3. Manual inspection with web interface (In repo Pompeii Explorer)

```usage: server.py [-h]
                 image_folder raw_image_folder marked_page_folder
                 load_previous_state

Web interface to mark incorrect extractions

positional arguments:
  image_folder         Path where pictures have been auto-extracted
  raw_image_folder     Path of PDF page images
  marked_page_folder   Path where incorrect pages will be stored
  load_previous_state  Load previously saved progress

optional arguments:
  -h, --help           show this help message and exit
```

Eg. python server.py ../final_extraction/PPM4 ../page_images/PPM4 ../final_extraction/trial False

4. Run LabelImg on ../final_extraction/trial

1) Click Pascal/VOC (to change the setting to YOLO).
2) Create label 'image' and mark it as default.
3) Load the marked_page_folder from previous step.
4) Annotate.

5. Extract annotations

```
usage: extract_images_from_annotations.py [-h]
                                          annotations_folder output_folder

Extract pictures from annotations

positional arguments:
  annotations_folder  Path of folder with raw images and annotations
  output_folder       Path of the folder where pictures will be extracted

optional arguments:
  -h, --help          show this help message and exit
```
Eg. python extract_images_from_annotations.py ../final_extraction/trial ../final_extraction/PPM4

