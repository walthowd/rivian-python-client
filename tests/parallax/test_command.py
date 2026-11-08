"""Tests for the signed `sendParallaxPayload` command encoder."""

from __future__ import annotations

import base64
import hashlib
import hmac

from rivian.parallax import encode_parallax_command
from rivian.parallax.proto import command_pb2 as command

KEY = b"k" * 32
REQUEST_ID = bytes(range(16))


def _payload(encoded: str) -> command.ParallaxPayload:
    return command.ParallaxPayload.FromString(base64.b64decode(encoded))


def test_encode() -> None:
    """The command is wrapped, timestamped and signed."""
    message = _payload(
        encode_parallax_command(
            "body.locks.unlock",
            b"\x08\x01",
            "vehicle_id",
            "identity_id",
            KEY,
            request_id=REQUEST_ID,
            timestamp_ns=1762600000_250000000,
        )
    )
    cmd = message.message.command
    assert cmd.rvm == "body.locks.unlock"
    assert cmd.field_2 == 3
    assert cmd.request_id == message.request_id == REQUEST_ID
    assert cmd.payload == b"\x08\x01"
    assert cmd.timestamp == message.timestamp
    assert (message.timestamp.seconds, message.timestamp.nanos) == (
        1762600000,
        250000000,
    )
    assert cmd.vehicle_id == "vehicle_id"
    assert message.signature.identity_id == "identity_id"
    assert message.signature.hmac.algorithm == command.HMAC_SHA256
    assert message.signature.hmac.mac == (
        hmac.new(KEY, cmd.SerializeToString(), hashlib.sha256).digest()
    )


def test_encode_without_payload() -> None:
    """A command without a payload gets a fresh request id."""
    first, second = (
        _payload(encode_parallax_command("body.locks.lock", b"", "vehicle", "id", KEY))
        for _ in range(2)
    )
    assert first.message.command.payload == b""
    assert len(first.request_id) == 16
    assert first.request_id != second.request_id
