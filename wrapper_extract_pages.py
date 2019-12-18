import subprocess
import argparse
import traceback

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract PDF pages as JPEG images')
    parser.add_argument('pdf_file_path', help='Path of the PPM pdf file')
    parser.add_argument('output_folder', help='Path of the folder where pages will be extracted')
    parser.add_argument('begin_page', help='Start extraction from this page number')
    parser.add_argument('end_page', help='End extraction at this page')

    args = parser.parse_args()
    args.pdf_file_path, args.output_folder, args.begin_page, args.end_page

    done = False
    begin_page = args.begin_page
    while not done:
        try:
            print('(Re)starting at page {}.'.format(begin_page))
            command = ['python', 'extract_pages.py', \
                       args.pdf_file_path, args.output_folder, \
                       begin_page, args.end_page]
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            print(stderr)
            lines = stdout.decode('utf-8').split('\n')
            output = lines[-2]
            if output != 'Done':
                begin_page = lines[-2]
            else:
                done = True

        except subprocess.CalledProcessError as e:
            print(e.output)
        except Exception:
            traceback.print_exc()
            break
