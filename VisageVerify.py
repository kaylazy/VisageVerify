import face_recognition
import os
import cv2
from tqdm import tqdm

def select_folder(prompt):
    """
    Prompts the user to select a folder using a file dialog.
    :param prompt: The title of the file dialog.
    :return: The path to the selected folder.
    """
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    folder_path = askdirectory(title=prompt) # show an "Open" dialog box and return the path to the selected folder
    return folder_path

def compare_faces(reference_encoding, unknown_encoding):
    """
    Compares two face encodings and returns the distance between them.
    :param reference_encoding: The encoding of the reference face.
    :param unknown_encoding: The encoding of the unknown face.
    :return: The distance between the two encodings.
    """
    return face_recognition.face_distance([reference_encoding], unknown_encoding)[0]

def load_reference_images(reference_folder_path):
    """
    load all reference images in the folder and return a list of tuple of (file name, image)
    """
    reference_images = []
    for filename in os.listdir(reference_folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(reference_folder_path, filename))
            reference_images.append((filename, image))
    return reference_images

def find_best_match(reference_images, unknown_encoding):
    """
    find the best match from the reference images and return the best match's file name and match percentage
    """
    max_match = 0
    reference_match = ""
    with tqdm(total=len(reference_images)) as pbar:
        for reference_filename, reference_image in reference_images:
            reference_encoding = face_recognition.face_encodings(reference_image)[0]
            match_percentage = 1-compare_faces(reference_encoding, unknown_encoding)
            if match_percentage > max_match:
                max_match = match_percentage
                reference_match = reference_filename
            pbar.update(1)
    match_percentage = "%.2f%%" % (100 * max_match)
    return reference_match, match_percentage

def main():
    reference_folder_path = select_folder("Select Reference Folder")
    images_folder_path = select_folder("Select Compare Folder")
    reference_images = load_reference_images(reference_folder_path)
    print("Press 'k' to keep, 'd' to delete, 'c' to cancel")
    for filename in os.listdir(images_folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            unknown_image_path = os.path.join(images_folder_path, filename)
            unknown_image = face_recognition.load_image_file(unknown_image_path)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            best_match, match_percentage = find_best_match(reference_images, unknown_encoding)
            if match_percentage != 0:
                print("Match found:", filename, " - ", match_percentage, " - Best match: ", best_match)
                img = cv2.imread(unknown_image_path)
                cv2.imshow(filename, img)
                while True:
                    key = cv2.waitKey(1)
                    if key == ord("k"):
                        break
                    elif key == ord("d"):
                        os.remove(unknown_image_path)
                        break
                    elif key == ord("c"):
                        exit()
                cv2.destroyAllWindows()
            else:
                print("No match found:", filename)
                
if __name__ == "__main__":
    main()
