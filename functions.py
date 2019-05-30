import json
import threading
import time

def save_image(
        content_url,
        encoding_format,
        file_name = None,
        directory = "./",
        max_fname_len = 50
):
    if file_name == None:
        file_name = content_url.split('/')[-1]
        if len(file_name) > max_fname_len:
            file_name = file_name[-1 * max_fname_len : ]
    else:
        file_name += "." + encoding_format

    from urllib.request import Request, urlopen

    req = Request(content_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    output = open(directory + file_name, "wb")
    output.write(webpage.read())
    output.close()

def download_images(fname, num_workers = 4, directory='./'):
    start_time = time.time()

    data = None

    # load data
    with open(fname) as json_file:
        data = json.load(json_file)

    im_meta = data["images"]

    # divide work amongst works
    num = len(im_meta)
    ims_per_worker = []
    base_partition = int(num / num_workers)
    for i in range(0,num_workers): ims_per_worker.append(base_partition)
    leftover = num % num_workers
    i = 0
    while leftover > 0:
        ims_per_worker[i] += 1
        leftover -= 1
    worker_starts = [0]
    for i in range(1,num_workers): worker_starts.append(worker_starts[i-1] + ims_per_worker[i-1])

    # work divided - execute threads.
    threads = []
    for i in range(0,num_workers):
        new_thread = threading.Thread(target=t_save_images, args=(im_meta, worker_starts[i], ims_per_worker[i], directory,))
        threads.append(new_thread)
        new_thread.start()

    for thread in threads:
        thread.join()

    print("Images downloaded in {} seconds".format(time.time() - start_time))


def t_save_images(
        im_meta,
        start,
        num,
        directory
):
    for i in range(start, start+num):
        content_url = im_meta[i]['content_url']
        encoding_format = im_meta[i]['encode_format']
        file_name = str(i)

        print("Attempting to execute image {}".format(i))
        try:
            save_image(content_url, encoding_format, file_name=file_name, directory=directory)
        except:
            "Didn't work"


