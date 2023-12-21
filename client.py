#!/usr/bin/env python

from __future__ import print_function
import logging
import sys
import argparse
import grpc
from utils import image_pb2_grpc, image_pb2
from pathlib import Path


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

    # connect to server
    channel = grpc.insecure_channel(f"{host}:{port}")
    try:
        grpc.channel_ready_future(channel).result(timeout=10)  # Timeout in seconds
    except grpc.FutureTimeoutError:
        logging.error(f"Error: Cannot connect to the server at {host}:{port}")
        sys.exit(1)
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
    # log if error happened
    except grpc.RpcError as e:
        throw_error(e)

    # Mean Filter Image
    if mean:
        nl_image_request = image_pb2.NLImage(data=nl_image.data)
        try:
            nl_image = stub.MeanFilter(nl_image_request)
            logging.info("Filtered Image")
        # log if error happened
        except grpc.RpcError as e:
            throw_error(e)

    # write returned image data to given output path (make necessary subdirectories
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as file:
        file.write(nl_image.data)
        logging.info("Outputted file at path: ", output)


def throw_error(e):
    """
    log an error message based on error supplied
    :param e: grpc.RpcError
    """
    if e.code() == grpc.StatusCode.INTERNAL:
        logging.error(f"Internal server error: {e.details()}")
    elif e.code() == grpc.StatusCode.CANCELLED:
        # This code block will be executed if the request was cancelled
        logging.warning("Request cancelled by the client")
    else:
        # Handle other gRPC error codes as needed
        logging.error(f"gRPC error: {e.code()}: {e.details()}")


def get_rotate(rotate_val):
    """
    return corresponding integer value for given rotation_enum
    throw error and exit if invalid enum given
    :param rotate_val: rotation enum (string)
    :return: integer
    """
    rotation_enum_mapping = {
        "NONE": 0,
        "NINETY_DEG": 90,
        "ONE_EIGHTY_DEG": 180,
        "TWO_SEVENTY_DEG": 270,
    }

    if (rotate_val is not None) and (rotate_val not in rotation_enum_mapping):
        logging.error(f"Error: Invalid rotation '{rotate_val}'."
                      f" Valid rotations are: NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG")
        sys.exit(1)

    return rotation_enum_mapping.get(rotate_val, 0)


if __name__ == "__main__":

    # define inputs client takes in
    parser = argparse.ArgumentParser(description="NLImage gRPC Client")
    parser.add_argument("--rotate", type=str, default=None,
                        help='Rotation in string format (NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG)')
    parser.add_argument("--mean", default=False, action='store_true', help='Apply mean filter')
    parser.add_argument("--port", type=int, default=50051, help="Port to bind to (default is 50051)")
    parser.add_argument("--host", type=str, default="localhost", help="Server to bind to (default is 127.0.0.1)")
    parser.add_argument("--input", type=str, required=True, help="path to inputted image")
    parser.add_argument("--output", type=str, required=True, help="path for outputted image")
    args = parser.parse_args()

    # get inputs
    port = args.port
    host = args.host
    input_val = args.input
    output = args.output
    rotate = get_rotate(args.rotate)
    mean = args.mean
    run(host, port, input_val, output, rotate, mean)