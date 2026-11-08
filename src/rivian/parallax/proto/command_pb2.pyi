from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HmacAlgorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HMAC_ALGORITHM_UNSPECIFIED: _ClassVar[HmacAlgorithm]
    HMAC_SHA256: _ClassVar[HmacAlgorithm]
HMAC_ALGORITHM_UNSPECIFIED: HmacAlgorithm
HMAC_SHA256: HmacAlgorithm

class ParallaxPayload(_message.Message):
    __slots__ = ("message", "timestamp", "request_id", "signature")
    class Message(_message.Message):
        __slots__ = ("command",)
        COMMAND_FIELD_NUMBER: _ClassVar[int]
        command: Command
        def __init__(self, command: _Optional[_Union[Command, _Mapping]] = ...) -> None: ...
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    message: ParallaxPayload.Message
    timestamp: Timestamp
    request_id: bytes
    signature: Signature
    def __init__(self, message: _Optional[_Union[ParallaxPayload.Message, _Mapping]] = ..., timestamp: _Optional[_Union[Timestamp, _Mapping]] = ..., request_id: _Optional[bytes] = ..., signature: _Optional[_Union[Signature, _Mapping]] = ...) -> None: ...

class Command(_message.Message):
    __slots__ = ("rvm", "field_2", "request_id", "payload", "timestamp", "vehicle_id")
    RVM_FIELD_NUMBER: _ClassVar[int]
    FIELD_2_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_ID_FIELD_NUMBER: _ClassVar[int]
    rvm: str
    field_2: int
    request_id: bytes
    payload: bytes
    timestamp: Timestamp
    vehicle_id: str
    def __init__(self, rvm: _Optional[str] = ..., field_2: _Optional[int] = ..., request_id: _Optional[bytes] = ..., payload: _Optional[bytes] = ..., timestamp: _Optional[_Union[Timestamp, _Mapping]] = ..., vehicle_id: _Optional[str] = ...) -> None: ...

class Signature(_message.Message):
    __slots__ = ("hmac", "identity_id")
    class Hmac(_message.Message):
        __slots__ = ("algorithm", "mac")
        ALGORITHM_FIELD_NUMBER: _ClassVar[int]
        MAC_FIELD_NUMBER: _ClassVar[int]
        algorithm: HmacAlgorithm
        mac: bytes
        def __init__(self, algorithm: _Optional[_Union[HmacAlgorithm, str]] = ..., mac: _Optional[bytes] = ...) -> None: ...
    HMAC_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    hmac: Signature.Hmac
    identity_id: str
    def __init__(self, hmac: _Optional[_Union[Signature.Hmac, _Mapping]] = ..., identity_id: _Optional[str] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
