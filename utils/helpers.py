import logging
import io
import grpc
from PIL import Image
from utils import image_pb2

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
        # Read incoming image data
        incoming_data = request.data if hasattr(request, 'data') else request.image.data

        # Open the incoming data as an image
        image = Image.open(io.BytesIO(incoming_data))

        # Call the provided processing function
        processed_image = process_func(image, request)

        # Create a bytes buffer for the processed image
        processed_image_buffer = io.BytesIO()

        # Save the processed image to the buffer
        processed_image.save(processed_image_buffer, format='PNG')

        # Get the byte data from the buffer
        processed_image_data = processed_image_buffer.getvalue()

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
