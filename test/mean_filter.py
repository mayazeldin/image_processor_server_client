import shutil
import unittest
import subprocess
from PIL import Image, ImageFilter
import sys
import os

# Add the root directory of your project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.helpers import are_images_identical

# check that a command that applies a mean filter will apply a mean filter to the image
class TestClientScript(unittest.TestCase):
    def test_photo_movement(self):
        # Set up the initial paths
        original_path = 'nueralink_test.PNG'
        new_path = "mean.PNG"

        # Run the client script with appropriate arguments
        command = "python ../client.py --host 127.0.0.1 --port 50051 --mean " \
                  "--input " + original_path + " --output " + new_path

        subprocess.run(command, check=True)

        # Assert that the new path exists
        self.assertTrue(os.path.exists(new_path))
        original_image = Image.open(original_path)
        rotated_image = Image.open(new_path)
        # Does the new image equal the old image with a mean filter
        self.assertTrue(are_images_identical(original_image.filter(ImageFilter.BoxBlur(1)), rotated_image))

    # delete all files and directories that have been created
    def tearDown(self):
        if os.path.exists("mean.png"):
            os.remove("mean.png")


if __name__ == '__main__':
    unittest.main()