# Import statements
import requests
import threading
import warnings
import sys

def download_part (start, end, url, filename, current):
    headers = {'Range' : 'bytes=%d-%d' % (start, end)}

    #Do Get Verify = True, do not leave like this
    pull = requests.get(url, headers=headers, stream=True, verify=False)
    file_portion = open("part_" + str(current + 1) + "." + filename.split('.')[-1], "wb")
    with open(filename, "r+b") as file:
        file.seek(int(start))
        info = file.tell()
        file.write(pull.content)
        file_portion.write(pull.content)

def download_file (url_of_file, number_of_threads):
    warnings.filterwarnings("ignore")
    #Do Get Verify = True, do not leave like this
    pull = requests.head(url_of_file, verify=False)
    file_name = url_of_file.split('/')[-1]
    try:
        file_size = int(pull.headers['content-length'])
    except:
        print("The URL is invalid")
        return

    portion_of_file = int(file_size) / number_of_threads
    file = open(file_name, "wb")
    file.write(b'\0' * file_size)
    file.close()

    for i in range(number_of_threads):
        start = i * portion_of_file
        end = start + portion_of_file

        thread = threading.Thread(target=download_part, kwargs= {'start': start, 'end':end, 'url': url_of_file, 'filename': file_name, 'current': i})
        thread.setDaemon(True)
        thread.start()

        main_thread = threading.current_thread()
        for thread in threading.enumerate():
            if thread is main_thread:
                continue
            thread.join()

if __name__ == '__main__':
    download_file(str(sys.argv[1]), int(sys.argv[2]))
