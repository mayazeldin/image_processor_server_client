import shutil
import unittest
import subprocess
from PIL import Image, ImageFilter
import sys
import os

# Add the root directory of project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from utils.helpers import are_images_identical


# Test that both rotate and mean can be called within the same command
class TestClientScript(unittest.TestCase):
    def test_photo_movement(self):
        # Set up the initial paths
        original_path = 'test/neuralink_test.PNG'
        new_path = "test/combine_command.PNG"

        os.chdir("..")
        # Run the client script with appropriate arguments
        command_server = "./server.py --hort 127.0.0.1 --port 50051"
        command_client = "./client.py --host 127.0.0.1 --port 50051 --rotate NINETY_DEG --mean " \
                         "--input " + original_path + " --output " + new_path
        subprocess.Popen(command_server)
        process = subprocess.Popen(command_client)
        process.wait()

        # Assert that the new path exists
        self.assertTrue(os.path.exists(new_path))
        original_image = Image.open(original_path)
        original_image = original_image.rotate(90, expand=True)
        rotated_image = Image.open(new_path)
        # Assert that the new file is equal to the original file filtered and rotated
        self.assertTrue(are_images_identical(original_image.filter(ImageFilter.BoxBlur(1)), rotated_image))

    # delete all files and directories that have been created
    def tearDown(self):
        if os.path.exists("combine_command.png"):
            os.remove("combine_command.png")



if __name__ == '__main__':
    unittest.main()