import grpc
import unittest
import sys
import os

# Add the root directory of your project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils import image_pb2, image_pb2_grpc

# Test that an invalid protobuf would cause the server to throw an error but not crash
class TestNLImageService(unittest.TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.port = 50051
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = image_pb2_grpc.NLImageServiceStub(self.channel)

    def test_invalid_image_handling(self):
        # Create an invalid NLImage message
        invalid_image = image_pb2.NLImage(data=b'invalid data')

        try:
            self.stub.RotateImage(invalid_image)
            self.fail("No error was thrown for an invalid image")
        except grpc.RpcError as e:
            self.assertEqual(e.code(), grpc.StatusCode.INTERNAL)
            self.assertIn('Exception deserializing request', e.details())

    # delete all files and directories that have been created
    def tearDown(self):
        self.channel.close()

if __name__ == '__main__':
    unittest.main()