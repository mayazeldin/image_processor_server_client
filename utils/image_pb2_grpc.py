# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from utils import image_pb2 as image__pb2


class NLImageServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RotateImage = channel.unary_unary(
                '/NLImageService/RotateImage',
                request_serializer=image__pb2.NLImageRotateRequest.SerializeToString,
                response_deserializer=image__pb2.NLImage.FromString,
                )
        self.MeanFilter = channel.unary_unary(
                '/NLImageService/MeanFilter',
                request_serializer=image__pb2.NLImage.SerializeToString,
                response_deserializer=image__pb2.NLImage.FromString,
                )


class NLImageServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RotateImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MeanFilter(self, request, context):
        """A request to mean filter the given image and return the new filtered
        image.  The mean filter can be computed for each pixel in an image by
        taking the average of a pixel and all of its neighbors.  As an example,
        if you have an image with 9 pixels:
        A B C
        D E F
        G H I
        Then a few examples of pixels from the mean filter of this
        image are:
        A_mean_filter = (A + B + E + D) / 4
        D_mean_filter = (D + A + B + E + G + H) / 6
        E_mean_filter = (E + A + B + C + D + F + G + H + I) / 9
        For color images, the mean filter is the image with this filter
        run on each of the 3 channels independently.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NLImageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RotateImage': grpc.unary_unary_rpc_method_handler(
                    servicer.RotateImage,
                    request_deserializer=image__pb2.NLImageRotateRequest.FromString,
                    response_serializer=image__pb2.NLImage.SerializeToString,
            ),
            'MeanFilter': grpc.unary_unary_rpc_method_handler(
                    servicer.MeanFilter,
                    request_deserializer=image__pb2.NLImage.FromString,
                    response_serializer=image__pb2.NLImage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'NLImageService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NLImageService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RotateImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NLImageService/RotateImage',
            image__pb2.NLImageRotateRequest.SerializeToString,
            image__pb2.NLImage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MeanFilter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NLImageService/MeanFilter',
            image__pb2.NLImage.SerializeToString,
            image__pb2.NLImage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
