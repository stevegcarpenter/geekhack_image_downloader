import os
import re
import requests
from bs4 import BeautifulSoup


def find_images(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    g_data = soup.find_all("a", {"class": "highslide"})

    todownload = []
    for item in g_data:
        try:
            todownload.append(item.attrs['href'])
        except:
            pass

    return todownload


def downloadImg(url, absdir, localFilename, numLeft):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print('Downloading %s... %d remaining'
                  % (localFilename, numLeft))

            fullfilepath = os.path.join(absdir, localFilename)

            # Only download images that have not yet been downloaded.
            # This accounts for the same image uploaded to multiple image
            # hosting sites
            if os.path.exists(fullfilepath) is False:
                with open(fullfilepath, 'wb') as fo:
                    for chunk in r.iter_content(4096):
                        fo.write(chunk)
    except:
        pass


def main():
    print('\nGeekhack Thread Image Downloader\n')

    base_url = input(
        'Enter URL of the LAST page of the thread to download images from.\n'
        + '(ie https://geekhack.org/index.php?topic=35864.12100)\n'
        + 'Note: For it to work correctly, nothing should trail the numbers'
        + '\n      after topic= in the URL address.\nURL: ')

    # Collect relevant data from URL
    m = re.match('.*topic=\d+\.(\d+)$', base_url)
    if m is None:
        print('URL address doesn\'t match required format, Exiting.')
        return

    # Extract last page of thread from URL
    lastpageno = int(m.group(1))

    # Get directory name
    absdir = input('Enter the absolute filepath of an existing directory to '
                   + 'store thread images.\n'
                   + '(ie imgs directory on the Desktop would become '
                   + '\'/home/your_username/Desktop/imgs\')\nFilepath: ')

    # Exit if directory doesn't exist
    if os.path.isdir(absdir) is False:
        print('Exiting: \'%s\' directory doesn\'t exist.' % absdir)
        return

    # Confirmation
    print('Found directory! Images will be stored in \'%s\'' % absdir)

    nums = [x for x in range(0, lastpageno, 50)]
    urls = ['https://geekhack.org/index.php?topic=35864.%d' % num
            for num in nums]

    todownload = []
    # Build list of image URL addresses from each page of the thread
    for url in urls:
        for img in find_images(url):
            if ("PHPSESSID" not in img
                    and not img.endswith('.gif')
                    and not img.endswith('.html')):
                todownload.append(img)

    # remove duplicates (This only accounts for duplicate images with the
    # exact same URL)
    todownload = list(set(todownload))

    print("Downloading %d images" % len(todownload))

    for i, url in enumerate(todownload):
        downloadImg(url, absdir, url.rsplit('/', 1)[-1], len(todownload)-(i+1))

if __name__ == '__main__':
    main()
