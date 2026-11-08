"""Encoder for signed `sendParallaxPayload` commands."""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
import uuid

from .proto import command_pb2


def encode_parallax_command(
    rvm: str,
    payload: bytes,
    vehicle_id: str,
    identity_id: str,
    secret_key: bytes,
    *,
    request_id: bytes | None = None,
    timestamp_ns: int | None = None,
) -> str:
    """Encode a signed `sendParallaxPayload` command as a base64 string.

    `secret_key` is the key shared with the vehicle, see `utils.get_secret_key`.
    """
    seconds, nanos = divmod(
        time.time_ns() if timestamp_ns is None else timestamp_ns, 10**9
    )
    stamp = command_pb2.Timestamp(seconds=seconds, nanos=nanos)
    request_id = request_id or uuid.uuid4().bytes
    command = command_pb2.Command(
        rvm=rvm,
        field_2=3,
        request_id=request_id,
        payload=payload,
        timestamp=stamp,
        vehicle_id=vehicle_id,
    )
    mac = hmac.new(secret_key, command.SerializeToString(), hashlib.sha256).digest()
    message = command_pb2.ParallaxPayload(
        message=command_pb2.ParallaxPayload.Message(command=command),
        timestamp=stamp,
        request_id=request_id,
        signature=command_pb2.Signature(
            hmac=command_pb2.Signature.Hmac(algorithm=command_pb2.HMAC_SHA256, mac=mac),
            identity_id=identity_id,
        ),
    )
    return base64.b64encode(message.SerializeToString()).decode("utf-8")
