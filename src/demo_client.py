import os

import lib


if __name__ == '__main__':
    client = lib.FileClient('localhost:8888')

    # demo for file uploading
    in_file_name = '/tmp/large_file_in'
    client.upload(in_file_name)

    # demo for file downloading:
    out_file_name = '/tmp/large_file_out'
    if os.path.exists(out_file_name):
        os.remove(out_file_name)
    client.download('whatever_name', out_file_name)
    os.system(f'sha1sum {in_file_name}')
    os.system(f'sha1sum {out_file_name}')
