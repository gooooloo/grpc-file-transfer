from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Chunk(_message.Message):
    __slots__ = ["buffer", "hash"]
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    buffer: bytes
    hash: str
    def __init__(self, hash: _Optional[str] = ..., buffer: _Optional[bytes] = ...) -> None: ...

class Reply(_message.Message):
    __slots__ = ["length", "msg"]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    length: int
    msg: str
    def __init__(self, msg: _Optional[str] = ..., length: _Optional[int] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
