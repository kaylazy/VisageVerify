# VisageVerify
 VisageVerify is a powerful image comparison tool that uses facial recognition technology to identify and match faces in photographs. It allows users to compare a set of reference images to a set of unknown images, and returns a percentage match for the best match found. It can be used for a variety of applications, such as identifying and removing duplicate images, or identifying and tracking individuals in security or surveillance applications. With its easy-to-use interface and high accuracy, VisageVerify is a valuable tool for anyone who needs to process and analyze large sets of images. 

 Additionally, VisageVerify can also be used to detect AI-generated images that do not accurately depict the subject intended to be in the image, making it an excellent tool for sifting through large amounts of images to find any potential inaccuracies or manipulations. With its advanced facial recognition technology, VisageVerify ensures that the images you work with are accurate and trustworthy.
 



### Instructions:
 1. Clone Repo or Download [VisageVerify.py](https://github.com/kaylazy/VisageVerify/blob/main/VisageVerify.py), and then Run VisageVerify.py
 2. Select a reference folder (this folder must contain images of the person(s)'s face(s) that you are attempting to detect, atleast one is required)
 3. Select a compare folder (this folder must contain images of faces you wish to compare the reference images to, atleast one is required)
 4. An image in the compare folder will be displayed with the percentage of the best match found within your reference folder. Press [K] to keep the image, [D] to delete the image, or [C] to cancel the program.
 5. After making a selection the next image will be displayed.




### Release Notes:

**v2.0 (WIP)**:

-   [x] Refactored Code
-   [x] Fast Scan Feature (stop scanning reference images if a specified match percentage value or greater is already found)
-   [ ] Auto Delete Feature (automatically delete compared images that do not meet specific match percentage)
-   [ ] Skip Feature (do not display images that do not meet a specific match percentage)
-   [ ] Installable Executable

**v1.1**:

-   Added progress bar using tqdm library
-   Added more detailed prompts for selecting folders
-   Added instructions for user input 
-   Changed the way reference images are stored and matched to improve performance
-   Fixed issue with images not closing after input selection

**v1.0**:

 -  Initial release
 -  Allows user to select two folders, one for reference images and one for images to compare
 -  Compares images in the comparison folder to all images in the reference folder
 -  Shows match percentage and best match found
 -  Allows user to delete or keep the images in the comparison folder