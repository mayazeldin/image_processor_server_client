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


# does rotating the image 0, 90, 180, and 270 degrees work?
class TestClientScript(unittest.TestCase):

    def setUp(self):
        # Set up common variables for all tests
        self.original_path = 'test/neuralink_test.PNG'
        self.new_path_0 = "test/0.PNG"
        self.new_path_90 = "test/90.PNG"
        self.new_path_180 = "test/180.PNG"
        self.new_path_270 = "test/270.PNG"
        os.chdir("..")

    def call_client_script(self, rotate_enum, new_path):

        command_server = "python3 ../server.py --hort 127.0.0.1 --port 50051"
        command_client = f"python3 ../client.py --host 127.0.0.1 --port 50051" \
                  f" --rotate {rotate_enum} --input {self.original_path} --output {new_path}"
        subprocess.Popen(command_server)
        process = subprocess.Popen(command_client)
        process.wait()
        self.assertTrue(os.path.exists(new_path))

    def test_photo_movement_0_deg(self):
        self.call_client_script("NONE", self.new_path_0)
        self.compare_images(0, self.new_path_0)

    def test_photo_movement_90_deg(self):
        self.call_client_script("NINETY_DEG", self.new_path_90)
        self.compare_images(90, self.new_path_90)

    def test_photo_movement_180_deg(self):
        self.call_client_script("ONE_EIGHTY_DEG", self.new_path_180)
        self.compare_images(180, self.new_path_180)

    def test_photo_movement_270_deg(self):
        self.call_client_script("TWO_SEVENTY_DEG", self.new_path_270)
        self.compare_images(270, self.new_path_270)

    def compare_images(self, angle, new_path):
        original_image = Image.open(self.original_path)
        rotated_image = Image.open(new_path)
        self.assertTrue(are_images_identical(original_image.rotate(angle, expand=True), rotated_image))

    def tearDown(self):
        if os.path.exists("0.PNG"):
            os.remove("0.PNG")
        if os.path.exists("90.PNG"):
            os.remove("90.PNG")
        if os.path.exists("180.PNG"):
            os.remove("180.PNG")
        if os.path.exists("270.PNG"):
            os.remove("270.PNG")


if __name__ == '__main__':
    unittest.main()