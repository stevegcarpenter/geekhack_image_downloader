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

// From here, it is necessary to install the two following packages which  
// aren't part of the default Python installation. This can be done using  
// pip3 which is installed as part of Python 3.  

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
Note: For it to work correctly, nothing should trail the numbers  
      after topic= in the URL address.  
URL: <enter_url_address_here>  

// Once an appropriate URL address has been entered, the script will then  
// ask for a directory path to store the images. This thread will not  
// create the directory for you, it must already exist.  

Enter the absolute filepath of an existing directory to store thread images.  
(ie imgs directory on the Desktop would become   
 '/home/your_username/Desktop/imgs')  
Filepath: </path/to/directory/here>  

Found directory! Images will be stored in '/path/to/directory/here'  

// After the directory path has been correctly entered, the script will  
// verify its existance and start downloading images to it. You will see how  
// many images are being downloaded and how many are left as progress is  
// made.  

Downloading 41 images  
Downloading 2OfxT.jpg... 40 remaining  
Downloading DSC_0219_zpsc638c74d.jpg... 39 remaining  
Downloading DSC_0206_zpsdc726314.jpg... 38 remaining  
Downloading TDzid.jpg... 37 remaining  
Downloading 90.png... 36 remaining  
Downloading tAQFK.jpg... 35 remaining  
...  







