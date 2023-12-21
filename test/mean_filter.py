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
        original_path = 'test/neuralink_test.PNG'
        new_path = "test/mean.PNG"

        # Run the client script with appropriate arguments
        os.chdir("..")
        command_server = "./server.sh --host 127.0.0.1 --port 50051"
        command_client = "./client.sh --host 127.0.0.1 --port 50051 --mean " \
                         "--input " + original_path + " --output " + new_path
        process_server = subprocess.Popen(command_server, shell=True)
        process_client = subprocess.Popen(command_client, shell=True)
        process_client.wait()

        # Assert that the new path exists
        self.assertTrue(os.path.exists(new_path))
        original_image = Image.open(original_path)
        rotated_image = Image.open(new_path)
        # Does the new image equal the old image with a mean filter
        self.assertTrue(are_images_identical(original_image.filter(ImageFilter.BoxBlur(1)), rotated_image))

        process_server.kill()

    # delete all files and directories that have been created
    def tearDown(self):
        if os.path.exists("./test/mean.png"):
            os.remove("./test/mean.png")


if __name__ == '__main__':
    unittest.main()