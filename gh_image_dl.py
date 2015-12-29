#!/usr/bin/python3

import os
import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from PIL import Image


def get_yes_no():
    while True:
        try:
            reply = input('Is this OK? [yes/no] ')
            if 'yes'.startswith(reply.lower()):
                return True
            elif 'no'.startswith(reply.lower()):
                return False
            else:
                print('Invalid input.')
        except:
            print('Invalid input')


def delete_corrupt_images(absdir, all_post_ids):
    print('\nWould you like to delete all corrupt files?\nNote: Some files '
          + 'that are very damaged will have errors while trying to read them'
          + '\n and this will output messages to the command line, but this is'
          + ' to be expected.')

    if get_yes_no() is False:
        return

    for img_name, post_id_list in all_post_ids.items():
        absimgpath = os.path.join(absdir, img_name)
        try:
            Image.open(absimgpath)
        except:
            print('Removing corrupt file \'%s\'' % absimgpath)
            os.remove(absimgpath)


def find_images(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    # Grab all inner post tags
    innerpost_tags = soup.find_all('div', {'class': 'inner'})

    image_urls = []
    post_ids = defaultdict(list)
    for _ in innerpost_tags:
        # Search innerpost tag for images
        image_tags = _.find_all('a', {'class': 'highslide'})

        if len(image_tags) is 0:
            continue

        # Get post id. This is saved for generating the report file that will
        # point each image back to all posts it was uploaded to
        post_id = _.attrs['id']

        # When a post with images was found, save the image URLs as well as
        # the post id that they came from
        for tag in image_tags:
            try:
                image_url = tag.attrs['href']

                # Check for invalid images
                if 'PHPSESSID' in image_url:
                    continue
                if 'emoji' in image_url:
                    continue
                if image_url.endswith('.gif') or image_url.endswith('.html'):
                    continue

                # Extract just the image name for URL
                image_name = image_url.rsplit('/', 1)[-1]

                # Only add to the URL list if the image hasn't been found yet
                if image_name not in post_ids:
                    image_urls.append(image_url)
                    post_ids[image_name].append(post_id)

            except:
                pass

    return image_urls, post_ids


def download_image(url, absdir, localFilename, numLeft):
    try:
        fullfilepath = os.path.join(absdir, localFilename)

        if os.path.exists(fullfilepath) is not True:
            r = requests.get(url)
            if r.status_code == 200:
                print('Downloading %s... %d remaining' % (localFilename,
                                                          numLeft))

            with open(fullfilepath, 'wb') as fo:
                for chunk in r.iter_content(4096):
                    fo.write(chunk)
    except:
        pass


def generate_report(absdir, all_post_ids, topicno):
    print('\nGenerating report file...')
    while True:
        fn = input('Enter name for report file.\nFilename: ')

        reportfilepath = os.path.join(absdir, fn)

        if os.path.exists(reportfilepath):
            print('Invalid report file name. Already exists.')
        else:
            break

    print('Report file will be placed at \'%s\'' % reportfilepath)

    with open(reportfilepath, 'w') as f:
        for img_name, post_id_list in all_post_ids.items():
            # Write image name to report file
            f.write('%s\n' % img_name)

            for post_id in post_id_list:
                # Extract post number from post id string and create the
                # post url address
                m = re.match('msg_(\d+)', post_id)
                if m is None:
                    continue

                # Write URL address to file
                f.write(' https://geekhack.org/index.php?topic=%d.msg%s#msg%s\n'
                        % (topicno, m.group(1), m.group(1)))

            # Add newline between references
            f.write('\n')


def prepare_directory():
    # Get directory name
    absdir = input('\nEnter the absolute filepath of an directory to '
                   + 'store thread images.\n'
                   + 'It will be created if it does not already exist.\n'
                   + '(ie imgs directory on the Desktop would become '
                   + '\'/home/your_username/Desktop/imgs\')\nFilepath: ')

    # If the directory doesn't yet exist create it
    if os.path.exists(absdir) is False:
        try:
            os.makedirs(absdir)
            print('Created directory \'%s\' to store images.' % absdir)
        except:
            print('Exiting. No permissions to create directory \'%s\'.'
                  % absdir)
            raise PermissionError
    else:
        # If it the path already exists, verify it is in fact a directory
        if os.path.isdir(absdir) is False:
            print('Exiting: \'%s\' is not a directory.' % absdir)
            raise NotADirectoryError
        elif os.access(absdir, os.W_OK) is False:
            print('Exiting. No permissions to write to \'%s\'' % absdir)
            raise PermissionError

        # Confirmation
        print('Images will be stored in \'%s\'\n' % absdir)

    return absdir


def get_thread_details():
    while True:
        try:
            topic_no = int(input(
                'Enter the topic number of the thread you want images '
                + 'downloaded from.\nFor instance, if the entire URL of the '
                + 'thread is:\n'
                + 'https://geekhack.org/index.php?topic=35864.12100\n'
                + 'The topic number is what follows topic=. In this case that'
                + ' is 35864\nTopic Number: '))
            break
        except:
            print('Invalid topic number input.')

    while True:
        try:
            start_page = int(input(
                'Enter the starting page number you would like images '
                + 'downloaded.\n(ie 1 to start at the first page)\nStart page'
                + ' number: '))
            if start_page < 1:
                print('Invalid start page input.')
                continue
            break
        except:
            print('Invalid start page input.')

    while True:
        try:
            end_page = int(input(
                'Enter the ending page you would like images downloaded.\n'
                + '(ie 243 if you want images downloaded all the way to page'
                + ' 243)\nIt is acceptable to have the end page match the '
                + 'start page.\nEnd page number: '))
            if end_page < start_page:
                print('Invalid end page input. Cannot be less then start '
                      + 'page.')
                continue
            break
        except:
            print('Invalid end page input.')

    return (topic_no, start_page, end_page)


def find_images_all_pages(page_urls, all_image_urls, all_post_ids, start_page):
    # Find and collect all images
    for i, url in enumerate(page_urls):

        print('Finding images on page %d' % (i + start_page))
        image_urls, post_ids = find_images(url)

        print('Found %d images!' % len(image_urls))

        for url in image_urls:
            # Get the image name from the end of the URL
            image_name = url.rsplit('/', 1)[-1]

            # If this image has never been encountered before add it
            if image_name not in all_post_ids:
                all_image_urls.append(url)

        # Add the post ID of the first instance of each image to a dictionary
        # for use when creating the report file.
        for _image_name, _post_id_list in post_ids.items():
            for _post_id in _post_id_list:
                # Only add post id to dictionary if it's not already present
                if _image_name not in all_post_ids:
                    all_post_ids[_image_name].append(_post_id)


def generate_page_urls(topic_no, start_page, end_page):
    nums = [x for x in range((start_page - 1) * 50, (end_page) * 50, 50)]
    return ['https://geekhack.org/index.php?topic=%d.%d' %
            (topic_no, num) for num in nums]


def download_all_images(absdir, all_image_urls):
    for i, url in enumerate(all_image_urls):
        download_image(url, absdir, url.rsplit('/', 1)[-1],
                       len(all_image_urls) - (i + 1))


def main():
    print('\nGeekhack Thread Image Downloader\n')

    # Obtain topic, start page, and end page
    topic_no, start_page, end_page = get_thread_details()

    # prepare directory for storing images
    try:
        absdir = prepare_directory()
    except PermissionError:
        return
    except NotADirectoryError:
        return
    except:
        print('Unknown error occurred creating/finding directory')

    # using topic number, start and end page create all thread page urls
    page_urls = generate_page_urls(topic_no, start_page, end_page)

    # list of all image urls found on all pages of thread
    all_image_urls = []
    # dictionary to contain all images found and post id they came from
    all_post_ids = defaultdict(list)

    # Find images on all pages
    find_images_all_pages(page_urls, all_image_urls, all_post_ids, start_page)

    print('\nDownloading %d images' % len(all_image_urls))

    # Now, download all the images and save them
    download_all_images(absdir, all_image_urls)

    # Optionally delete corrupt images
    delete_corrupt_images(absdir, all_post_ids)

    # Finally, generate the report file
    generate_report(absdir, all_post_ids, topic_no)


if __name__ == '__main__':
    main()
