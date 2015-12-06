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

// From here, it is necessary to install the three following packages which  
// aren't part of the default Python installation. This can be done using  
// pip3 which is installed as part of Python 3.  

$ sudo pip3 install lxml  
$ sudo pip3 install beautifulsoup4  
$ sudo pip3 install requests  

// Versioning information is given using the pip3 freeze command.  

$ pip3 freeze  

beautifulsoup4 version 4.4.1  
requests version 2.8.1  

// Once both these packages have been successfully installed, the script  
// is ready to use. Start the script using the following incantation after  
// it has been downloaded.  

$ python3 gh_image_dl.py  

Geekhack Thread Image Downloader  

Enter URL of the LAST page of the thread to download images from.  
(ie https://geekhack.org/index.php?topic=35864.12100)  
URL: <enter_url_address_here>  

// Once an appropriate URL address has been entered, the script will then  
// ask for a directory path to store the images.  

Enter the absolute filepath of an directory to store thread images.  
It will be created if it does not already exist.  
(ie imgs directory on the Desktop would become '/path/to/directory/here')  
Filepath: <user_supplied_filepath>  
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

// The script will then iterate through all pages of the thread and find  
// images to download. It will eliminate duplicates based on filename here.  
// With each page it will display how many images it found.  

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

// It will then start downloading all the images to the previously specified  
// directory. When it discovers that some have already been downloaded  
// it will skip those.  

Generating report file...
Enter name for report file.
Filename: <report_file_name>
Report file will be placed at '/path/to/directory/here/<report_file_name>

// Finally, after downloading all the images, it will request a name to store  
// the report. The report file consists of all the image names and the URL  
// address of the exact post they came from. Running head on the report  
// file that was generated demonstrates how it is formatted below.  
// Each filename is listed and on the second line a link to the post it was  
// uploaded in follows.

$ head <report_file_name>

HrHw4.jpg  
 https://geekhack.org/index.php?topic=35864.msgxxxxxxxxxxxxxxxxxx  

12605554253_d16796e9af_b.jpg  
 https://geekhack.org/index.php?topic=35864.msgxxxxxxxxxxxxxxxxxx  

PydoYrV.jpg  
 https://geekhack.org/index.php?topic=35864.msgxxxxxxxxxxxxxxxxxx  

