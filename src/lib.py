import os
from concurrent import futures

import grpc
import time

import chunk_pb2, chunk_pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB


def get_file_chunks(filename):
    with open(filename, 'rb') as f:
        while True:
            piece = f.read(CHUNK_SIZE);
            if len(piece) == 0:
                return
            yield chunk_pb2.Chunk(buffer=piece)


def save_chunks_to_file(chunks, filename):
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)


class FileClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = chunk_pb2_grpc.FileServerStub(channel)

    def upload(self, in_file_name):
        chunks_generator = get_file_chunks(in_file_name)
        response = self.stub.upload(chunks_generator)
        assert response.length == os.path.getsize(in_file_name)

    def download(self, target_name, out_file_name):
        response = self.stub.download(chunk_pb2.Request(name=target_name))
        save_chunks_to_file(response, out_file_name)


class FileServer(chunk_pb2_grpc.FileServerServicer):
    def __init__(self):

        class Servicer(chunk_pb2_grpc.FileServerServicer):
            def __init__(self):
                self.tmp_file_name = '/tmp/server_tmp'

            def upload(self, request_iterator, context):
                save_chunks_to_file(request_iterator, self.tmp_file_name)
                return chunk_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

            def download(self, request, context):
                if request.name:
                    return get_file_chunks(self.tmp_file_name)

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chunk_pb2_grpc.add_FileServerServicer_to_server(Servicer(), self.server)

    def start(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)
