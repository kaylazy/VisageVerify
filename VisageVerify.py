import face_recognition
import os
import cv2
from tqdm import tqdm
from termcolor import colored

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

def find_best_match(reference_images, unknown_encoding, use_fast_scan = False, fast_scan_thres = 1):
    """
    find the best match from the reference images and return the best match's file name and match percentage
    """
    max_match = 0
    reference_match = ""
    with tqdm(total=len(reference_images)) as pbar:
        for reference_filename, reference_image in reference_images:
            reference_encoding = face_recognition.face_encodings(reference_image)[0]
            match_percentage = 1-compare_faces(reference_encoding, unknown_encoding)
            if use_fast_scan and match_percentage >= fast_scan_thres:
                reference_match = reference_filename
                return reference_match, match_percentage
            elif match_percentage > max_match:
                max_match = match_percentage
                reference_match = reference_filename
            pbar.update(1)
    return reference_match, match_percentage

def main():
    reference_folder_path = select_folder("Select Reference Folder")
    images_folder_path = select_folder("Select Compare Folder")
    reference_images = load_reference_images(reference_folder_path)

    fast_scan_enabled = input("Do you want to enable FastScan? (y/n): ") == 'y'
    fast_scan_threshold = 0
    if fast_scan_enabled:
        fast_scan_threshold = float(input("Enter FastScan threshold value between 0 and 1 (e.g. 0.55): "))        

    auto_skip_enabled = input("Do you want to enable AutoSkip (y/n): ") == 'y'
    auto_skip_threshold = 0
    if auto_skip_enabled:
        auto_skip_threshold = float(input("Enter AutoSkip threshold value between 0 and 1 (e.g. 0.55): "))     
        print(f"Auto-Skip Enabled. Threshold: {auto_skip_threshold}")

    auto_delete_enabled = auto_skip_enabled and input(colored("Do you want to enable AutoDelete (y/n): ","red")) == 'y'
    # auto_delete_threshold = 0
    if auto_delete_enabled:
        # if auto_skip_enabled:
        # auto_delete_threshold = auto_skip_threshold
        print("Auto-Delete Enabled. Using Auto Skip Threshold.")
        # else:
        #     auto_delete_threshold = float(input("Enter AutoDelete threshold value between 0 and 1 (e.g. 0.55): "))     
        #     print(f"Auto-Delete Enabled. Threshold: {auto_delete_threshold}")


    print("Press 'k' to keep, 'd' to delete, 'c' to cancel")
    for filename in os.listdir(images_folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            unknown_image_path = os.path.join(images_folder_path, filename)
            unknown_image = face_recognition.load_image_file(unknown_image_path)
            face_encodings = face_recognition.face_encodings(unknown_image)
            if(face_encodings.count == 0):
                print("No faces found. Skipped File:", filename)
            else:
                for face_encoding in face_encodings:
                    unknown_encoding = face_encoding
                    best_match, match_percentage_value = find_best_match(reference_images, unknown_encoding, fast_scan_enabled, fast_scan_threshold)
                    if match_percentage_value != 0:
                        match_percentage = "%.2f%%" % (100 * match_percentage_value)
                        percentage_color = "white"
                        if(match_percentage_value >= 0.85):
                            percentage_color = "light_green"
                        elif(match_percentage_value >= 0.7):
                            percentage_color = "green"
                        elif(match_percentage_value >= 0.55):
                            percentage_color = "light_yellow"
                        elif(match_percentage_value >= 0.4):
                            percentage_color = "yellow"
                        print("Match found:", colored(filename,percentage_color), " - ", colored(match_percentage,percentage_color), " - Best match: ", colored(best_match,percentage_color))
                        # if auto_delete_enabled and match_percentage_value <= auto_delete_threshold:
                        if auto_delete_enabled and match_percentage_value <= auto_skip_threshold:
                            os.remove(unknown_image_path)
                            print(colored(("Deleted File:", filename),"red"))
                        elif auto_skip_enabled and match_percentage_value <= auto_skip_threshold:
                            print("Skipped File:", filename)
                        else:
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
                        if auto_delete_enabled:
                            os.remove(unknown_image_path)
                            print(colored(("Deleted File:", filename),"red"))
                
if __name__ == "__main__":
    main()
