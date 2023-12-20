import grpc
import sys
from PIL import Image, ImageFilter
from utils import image_pb2_grpc, image_pb2
from concurrent.futures import ThreadPoolExecutor
from utils.helpers import is_port_valid, is_valid_ip, process_image
import logging
import argparse

class NLImageService(image_pb2_grpc.NLImageServiceServicer):
    def RotateImage(self, request, context):
        return process_image(request, context, self.rotate_image)

    def MeanFilter(self, request, context):
        return process_image(request, context, self.apply_mean_filter)

    def rotate_image(self, image, request):
        return image.rotate(request.rotation, expand=True)

    def apply_mean_filter(self, image, request):
        return image.filter(ImageFilter.BoxBlur(1))

def serve(port, host):
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageService(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logging.info(f"started logging at {host}:{port}")
    server.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NLImage gRPC Client")
    parser.add_argument("--port", type=int, default=50051, help="Port to bind to")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server to bind to")
    args = parser.parse_args()
    port = args.port
    host = args.host
    is_valid_ip(host)
    is_port_valid(port)

    serve(port, host)