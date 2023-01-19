import os
import shutil

from sklearn.model_selection import train_test_split

# Read images and annotations
images = [os.path.join('images', x) for x in os.listdir('images')]

images.sort()

# Split the dataset into train-valid-test splits
train_images, val_images = train_test_split(images, test_size=0.3,
                                            random_state=1)
val_images, test_images = train_test_split(val_images,
                                           test_size=0.7, random_state=1)


# Utility function to move images
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False


# Move the splits into their folders
move_files_to_folder(train_images, 'images/train')
move_files_to_folder(val_images, 'images/val/')
move_files_to_folder(test_images, 'images/test/')
