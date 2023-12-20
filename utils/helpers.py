import ipaddress
import socket
import logging
import sys
import tempfile
import os
import grpc
from PIL import Image
from utils import image_pb2

def is_valid_ip(address):
    """
    check if supplied param is a valid ip address
    if not valid, exit and throw logging error
    """
    try:
        ipaddress.ip_address(address)
    except ValueError:
        logging.error("Invalid IPAddress given")
        sys.exit(1)


def is_port_valid(port):
    """
    check if supplied porm is valid port
    if not valid, exit and throw logging error
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
        except socket.error:
            logging.error("Port already in use")
            sys.exit(1)

def process_image(request, context, process_func):
    """
    process an image given the process function
    return the new image as a nlimage
    :param request: request that contains the image data
    :param context: place to store error messages, processing information
    :param process_func: process function to apply to image data to produce new image
    :return: nlimage
    """
    logging.info(f"trying to process image in server using {process_func.__name__}")

    try:
        # Create a temporary file to save the incoming image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(request.data if hasattr(request, 'data') else request.image.data)

            # Open the temporary file as an image
            image = Image.open(temp_file.name)

            # Call the provided processing function
            processed_image = process_func(image, request)

            # Save the processed image back to the temporary file
            processed_image.save(temp_file.name, format='PNG')

            # Read the processed image data from the temporary file
            with open(temp_file.name, 'rb') as temp_outfile:
                processed_image_data = temp_outfile.read()

        # Clean up the temporary file
        os.remove(temp_file.name)

        # Create and return the NLImage with the processed image data
        nl_image = image_pb2.NLImage(data=processed_image_data)
        return nl_image

    except Exception as e:
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details(f'Error processing image: {str(e)}')
        logging.error("Error processing image occurred")
        return image_pb2.NLImage()

def are_images_identical(img1, img2):
    """
    are the two images the same?
    :param img1: Image
    :param img2: Image
    :return: bool
    """
    if img1.size != img2.size:
        return False

    # Compare pixels
    for x in range(img1.width):
        for y in range(img1.height):
            if img1.getpixel((x, y)) != img2.getpixel((x, y)):
                return False

    return True
