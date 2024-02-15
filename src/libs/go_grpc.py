import imp
import grpc
from numpy import byte
import grpc
from src.libs.pb import stream_pb2, stream_pb2_grpc


class GoGrpcManager:
    def request_generate_content(imagefile: byte, user_unique_id: str):
        # connect grpc
        with grpc.insecure_channel('http://localhost:50051') as channel:
            stub = stream_pb2_grpc.StreamServiceStub(channel)
            request = stream_pb2.Request(
                image=imagefile,
                id=user_unique_id
            )
            responses = stub.GeneratedContentStream(request)
            return responses

