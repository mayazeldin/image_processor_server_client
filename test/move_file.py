import shutil
import unittest
import subprocess
from PIL import Image

import sys
import os

# Add the root directory of your project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.helpers import are_images_identical


class TestClientScript(unittest.TestCase):
    def test_photo_movement(self):
        # Set up the initial paths
        original_path = 'nueralink_test.PNG'
        new_path = "new_dict/new_photo.png"

        # Run the client script with appropriate arguments
        command = "python ../client.py --host 127.0.0.1 --port 50051 --input " + original_path + " --output " + new_path

        subprocess.run(command, check=True)

        # Assert that the new path exists
        self.assertTrue(os.path.exists(new_path))
        original_image = Image.open(original_path)
        moved_image = Image.open(new_path)
        self.assertTrue(are_images_identical(original_image, moved_image))

    def tearDown(self):
        if os.path.exists("new_dict/new_photo.png"):
            os.remove("new_dict/new_photo.png")
            os.rmdir("new_dict")

if __name__ == '__main__':
    unittest.main()