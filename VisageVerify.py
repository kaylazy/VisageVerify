import face_recognition
import os
import cv2
from tqdm import tqdm

def select_folder(prompt):
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    folder_path = askdirectory(title=prompt) # show an "Open" dialog box and return the path to the selected folder
    return folder_path

def compare_faces(reference_encoding, unknown_encoding):
    return face_recognition.face_distance([reference_encoding], unknown_encoding)[0]

def main():
    
    reference_folder_path = select_folder("Select Reference Folder")
    images_folder_path = select_folder("Select Compare Folder")
    reference_images = []
    for filename in os.listdir(reference_folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(reference_folder_path, filename))
            reference_images.append((filename, image))
    print("Press 'k' to keep, 'd' to delete, 'c' to cancel")
    for filename in os.listdir(images_folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            unknown_image_path = os.path.join(images_folder_path, filename)
            unknown_image = face_recognition.load_image_file(unknown_image_path)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
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
            if max_match > 0:
                match_percentage = "%.2f%%" % (100 * max_match)
                print("Match found:", filename, " - ", match_percentage, " - Best match: ", reference_match)
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
