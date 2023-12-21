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


# check that the outputted image is stored in the path supplied by the output variable
class TestClientScript(unittest.TestCase):
    def test_photo_movement(self):
        # Set up the initial paths
        original_path = 'test/neuralink_test.PNG'
        new_path = "test/new_dict/new_photo.png"

        os.chdir("..")
        # Run the client script with appropriate arguments
        command_server = "./server.py --host 127.0.0.1 --port 50051"
        command_client = "./client.py " \
                         "--host 127.0.0.1 --port 50051 --input " + original_path + " --output " + new_path
        subprocess.Popen(command_server)
        process = subprocess.Popen(command_client)
        process.wait()

        # Assert that the new path exists
        self.assertTrue(os.path.exists(new_path))
        original_image = Image.open(original_path)
        moved_image = Image.open(new_path)
        # does the new image in the path specified at output equal the original image?
        self.assertTrue(are_images_identical(original_image, moved_image))

    # delete all files and directories that have been created
    def tearDown(self):
        if os.path.exists("new_dict/new_photo.png"):
            os.remove("new_dict/new_photo.png")
            os.rmdir("new_dict")


if __name__ == '__main__':
    unittest.main()