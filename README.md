# geekhack_image_downloader
The purpose of this script is to download all images of a specified thread  
on Geekhack. This was originally written to support Python version 3.5.0  
although it may be compatible with other versions as well. The following is  
a short description of how to get setup to use the script successfully.  

First off, install Python 3.5 if you don't already have this. This may be  
slightly different depending on the distribution of Linux and package  
manager being used.  

For Arch Linux:  
$ sudo pacman -S python3  

For Ubuntu Linux:  
$ sudo apt-get install python3  

// Following successful installation of Python 3, use the following command   
// to check the version:  

$ python3 --version  
Python 3.5.0  

// You should see the above message indicating the version of Python. In  
// this case it is Python 3.5.0.  

// From here, it is necessary to install the following packages which  
// aren't part of the default Python installation. This can be done using  
// pip3 which is installed as part of Python 3.  

$ sudo pip3 install lxml  
$ sudo pip3 install beautifulsoup4  
$ sudo pip3 install requests  
$ sudo pip3 install Pillow

// Versioning information is given using the pip3 freeze command.  

$ pip3 freeze  

beautifulsoup4==4.4.1  
lxml==3.5.0  
Pillow==3.0.0  
requests==2.8.1  

// Once these packages have been successfully installed, the script  
// is ready to use. Start the script using the following incantation after  
// it has been downloaded.  

$ python3 gh_image_dl.py  

Geekhack Thread Image Downloader  

// Next, the script will ask for the topic number of the thread, a start page  
// number, and an end page number to download images. It explains how to extract  
// the topic number from the URL address and the start and end page numbers are  
// easy enough to figure out.  

Enter URL of the LAST page of the thread to download images from.  
(ie hnt images downloaded from.  
For instance, if the entire URL of the thread is:  
https://geekhack.org/index.php?topic=35864.12100  
The topic number is what follows topic=. In this case that is 35864  
Topic Number:  35864  

Enter the starting page number you would like images downloaded.  
(ie 1 to start at the first page)  
Start page number: 1  

Enter the ending page you would like images downloaded.  
(ie 243 if you want images downloaded all the way to page 243)  
It is acceptable to have the end page match the start page.  
End page number: 6  

// Next, the script will ask for a directory path to store the images.  

Enter the absolute filepath of an directory to store thread images.  
It will be created if it does not already exist.  
(ie imgs directory on the Desktop would become '/home/username/Desktop/imgs')  
Filepath: user_supplied_filepath  
Images will be stored in '/path/to/directory/here'  

// After the directory path has been correctly entered, the script will  
// conditionally create a directory to store the images if it does not  
// already exist.  

Finding images on page 1  
Found 13 images!  
Finding images on page 2  
Found 14 images!  
Finding images on page 3  
Found 4 images!  
Finding images on page 4  
Found 4 images!  
Finding images on page 5  
Found 9 images!  
Finding images on page 6  
Found 10 images!  

// The script will then iterate through all pages of the thread, find and  
// download images. It will eliminate duplicates based on filename here. With  
// each page it will display how many images it found.  

Downloading 50 images  
Downloading 6sl9n.jpg... 49 remaining  
Downloading 20450618.jpg... 48 remaining  
Downloading tumblr_lr4x4vJ7pk1qdy1rro1_500.jpg... 47 remaining  
Downloading 2ziq1s9.jpg... 46 remaining  
Downloading closeenough.png?1317606898... 45 remaining  
Downloading g1338251854876997822.jpg... 44 remaining  
Downloading DzbSf.jpg... 43 remaining  
Downloading inawefacesparklyeyesdra.png... 42 remaining  
...  

// After downloading all the images from the requested pages and topic, the script  
// will ask the user if they would like it to remove all the corrupted image  
// files. It makes sense to do this, but at this time there appears to be some  
// issues with handling some types of corrupt images in the Pillow library that  
// causes that program to spew error messages out to the terminal. This isn't a  
// problem although it might alert the user, so they are advised.  
Would you like to delete all corrupt files?  
Note: Some files that are very damaged will have errors while trying to read them  
 and this will output messages to the command line, but this is to be expected.  
Is this OK? [y/N]  

// Finally, after downloading all the images, it will request a name to store  
// the report. The report file consists of all the image names and the URL  
// address of the exact post they came from. Running head on the report  
// file that was generated demonstrates how it is formatted below.  
// Each filename is listed and on the second line a link to the post it was  
// uploaded in follows.  

Generating report file...  
Enter name for report file.  
Filename: report_file_name  
Report file will be placed at '/path/to/directory/here/report_file_name'  

// Now the report file can be viewed to see how the link between each image name  
// and a URL address exactly where that image was originally posted has been  
// created.  

$ head report_file_name  

HrHw4.jpg  
 https://geekhack.org/index.php?topic=35864.msgxxxxxxxxxxxxxxxxxx  

12605554253_d16796e9af_b.jpg  
 https://geekhack.org/index.php?topic=35864.msgxxxxxxxxxxxxxxxxxx  

PydoYrV.jpg  
 https://geekhack.org/index.php?topic=35864.msgxxxxxxxxxxxxxxxxxx  

