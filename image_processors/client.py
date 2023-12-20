#!/usr/bin/env python

from __future__ import print_function
import logging
import sys
import argparse
import grpc
import os

# Add the root directory of project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from utils import image_pb2_grpc, image_pb2
from pathlib import Path
from utils.helpers import is_port_valid, is_valid_ip



def run(host, port, input, output, rotate, mean):
    """
    call on the server to process an image and store new image in specified output path given parameters
    :param host: (string) ip address to connect to
    :param port: (int) port to connect to
    :param input: (string) path where original image stored
    :param output: (string) path to store output image
    :param rotate: (int) degrees to rotate image by
    :param mean: (bool) should mean filter be applied?
    """
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = image_pb2_grpc.NLImageServiceStub(channel)

        # Create an NLImage object to pass to the server
        try:
            with open(input, 'rb') as image_file:
                image_data = image_file.read()
        except FileNotFoundError:
            logging.error(f"Error: File not found at path: {input}")
            sys.exit(1)

        nl_image = image_pb2.NLImage(data=image_data)

        # Rotate Image
        rotate_request = image_pb2.NLImageRotateRequest(rotation=rotate, image=nl_image)
        try:
            nl_image = stub.RotateImage(rotate_request)
            logging.info("Rotated Image ", rotate, " degrees")
        # log if error occured
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INTERNAL:
                logging.error(f"Internal server error: {e.details()}")
            elif e.code() == grpc.StatusCode.CANCELLED:
                # This code block will be executed if the request was cancelled
                logging.warning("Request cancelled by the client")
            else:
                # Handle other gRPC error codes as needed
                logging.error(f"gRPC error: {e.code()}: {e.details()}")

        # Mean Filter Image
        if mean:
            nl_image_request = image_pb2.NLImage(data=nl_image.data)
            try:
                nl_image = stub.MeanFilter(nl_image_request)
                logging.info("Filtered Image")
            # log if error occured
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.INTERNAL:
                    logging.error(f"Internal server error: {e.details()}")
                elif e.code() == grpc.StatusCode.CANCELLED:
                     # This code block will be executed if the request was cancelled
                    logging.warning("Request cancelled by the client")
                else:
                    # Handle other gRPC error codes as needed
                    logging.error(f"gRPC error: {e.code()}: {e.details()}")


        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as file:
            file.write(nl_image.data)
            logging.info("Outputted file at path: ", output)

def get_rotate(rotate):
    """
    return corresponding integer value for given rotation_enum
    throw error and exit if invalid enum given
    :param rotate: rotation enum (string)
    :return: integer
    """
    rotation_enum_mapping = {
        "NONE": 0,
        "NINETY_DEG": 90,
        "ONE_EIGHTY_DEG": 180,
        "TWO_SEVENTY_DEG": 270,
    }

    if (rotate is not None) and (rotate not in rotation_enum_mapping):
        logging.error(f"Error: Invalid rotation '{rotate}'."
                      f" Valid rotations are: NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG")
        sys.exit(1)

    # Example: RotateImage RPC with user-specified rotation
    return rotation_enum_mapping.get(rotate, 0)

if __name__ == "__main__":

    # optional inputs
    parser = argparse.ArgumentParser(description="NLImage gRPC Client")
    parser.add_argument("--rotate", type=str, default=None,
                        help='Rotation in string format (NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG)')
    parser.add_argument("--mean", default=False, action='store_true', help='Apply mean filter')
    parser.add_argument("--port", type=int, default=50051, help="Port to bind to (default is 50051)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server to bind to (default is 127.0.0.1)")
    parser.add_argument("--input", type=str, required=True, help="path to inputted image")
    parser.add_argument("--output", type=str, required=True, help="path for outputted image")
    args = parser.parse_args()

    # required inputs
    port = args.port
    host = args.host
    input = args.input
    output = args.output
    is_valid_ip(host)
    is_port_valid(port)

    rotate = get_rotate(args.rotate)
    mean = args.mean
    print(f"request with output {output} and rotate {rotate} and mean {mean}")

    run(host, port, input, output, rotate, mean)