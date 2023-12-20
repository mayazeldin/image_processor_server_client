from PIL import ImageFilter


def rotate_image(image, request):
    """
    rotates image given rotation degrees stored in request
    :param image: (Image) image to rotate
    :param request: request that stores image info
    :return: Image
    """
    return image.rotate(request.rotation, expand=True)


def apply_mean_filter(image, request):
    """
    applies mean filter to image
    :param image: (Image) to apply mean filter
    :param request:
    :return: Image
    """
    return image.filter(ImageFilter.BoxBlur(1))
