import os
import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict


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


def main():
    print('\nGeekhack Thread Image Downloader\n')

    base_url = input(
        'Enter URL of the LAST page of the thread to download images from.\n'
        + '(ie https://geekhack.org/index.php?topic=35864.12100)\n'
        + 'Note: For it to work correctly, nothing should trail the numbers'
        + '\n      after topic= in the URL address.\nURL: ')

    # Collect relevant data from URL
    m = re.match('.*topic=(\d+)\.(\d+)', base_url)
    if m is None:
        print('URL address doesn\'t match required format, Exiting.')
        return

    # Extract topic number
    topicno = int(m.group(1))

    # Extract last page of thread from URL
    lastpageno = int(m.group(2))

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
            print('Error creating directory. Exiting')
            return
    else:
        # If it wasn't just created, verify it is in fact a directory
        if os.path.isdir(absdir) is False:
            print('Exiting: \'%s\' is not a directory.' % absdir)
            return

        # Confirmation
        print('Images will be stored in \'%s\'\n' % absdir)

    nums = [x for x in range(0, lastpageno + 50, 50)]
    urls = ['https://geekhack.org/index.php?topic=%d.%d' % (topicno, num)
            for num in nums]

    # dictionary to contain all images found and post id they came from
    all_image_urls = []
    all_post_ids = defaultdict(list)

    # Find and download all images in a single page
    for i, url in enumerate(urls):

        print('Finding images on page %d' % (i + 1))
        image_urls, post_ids = find_images(url)

        print('Found %d images!' % len(image_urls))

        for url in image_urls:
            # Get the image name from the end of the URL
            image_name = url.rsplit('/', 1)[-1]

            # If this image has never been encountered before add it
            if image_name not in all_post_ids:
                all_image_urls.append(url)

        for _image_name, _post_id_list in post_ids.items():
            for _post_id in _post_id_list:
                if _image_name not in all_post_ids:
                    all_post_ids[_image_name].append(_post_id)

    print('\nDownloading %d images' % len(all_image_urls))

    # Now, download all the images and save them
    for i, url in enumerate(all_image_urls):
        download_image(url, absdir, url.rsplit('/', 1)[-1],
                       len(all_image_urls) - (i + 1))

    # Finally, generate the report file
    generate_report(absdir, all_post_ids, topicno)

if __name__ == '__main__':
    main()
