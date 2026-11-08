"""Tests for the Parallax equivalents of vehicle commands."""

from __future__ import annotations

from typing import Any

import pytest

from rivian import VehicleCommand
from rivian.exceptions import RivianBadRequestError
from rivian.parallax import encode_vehicle_command, vehicle_command_feature


@pytest.mark.parametrize(
    ("command", "params", "model", "rvm", "payload"),
    [
        (VehicleCommand.LOCK_ALL_CLOSURES_FEEDBACK, None, None, "body.locks.lock", b""),
        (
            VehicleCommand.UNLOCK_ALL_CLOSURES,
            None,
            None,
            "body.locks.unlock",
            b"\x08\x01",
        ),
        (
            VehicleCommand.OPEN_ALL_WINDOWS,
            None,
            None,
            "body.closures.open",
            b"\x0a\x02\x90\x4e",
        ),
        (
            VehicleCommand.CLOSE_FRUNK,
            None,
            None,
            "body.closures.close",
            b"\x0a\x01\x05",
        ),
        (
            VehicleCommand.OPEN_LIFTGATE_UNLATCH_TAILGATE,
            None,
            "R1S",
            "body.closures.open",
            b"\x0a\x01\x07",
        ),
        (
            VehicleCommand.OPEN_LIFTGATE_UNLATCH_TAILGATE,
            None,
            "R1T",
            "body.closures.open",
            b"\x0a\x01\x06",
        ),
        (VehicleCommand.PANIC_ON, None, None, "security.alarm.enable_panic", b""),
        (
            VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP,
            {"HVAC_set_temp": 21.0},
            None,
            "comfort.cabin.set_preconditioning_temperature",
            b"\x0d\x00\x00\xa8\x41",
        ),
        (
            VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP,
            {"HVAC_set_temp": 0},
            None,
            "comfort.cabin.set_preconditioning_temperature",
            b"\x0d\x00\x00\x00\x00",
        ),
        (
            VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT,
            {"level": 2},
            None,
            "comfort.cabin.set_cabin_surface",
            b"\x08\x05\x10\x01\x18\x02\x20\x01",
        ),
        (
            VehicleCommand.CABIN_HVAC_STEERING_HEAT,
            {"level": 0},
            None,
            "comfort.cabin.set_cabin_surface",
            b"\x08\x01\x18\x01\x20\x01",
        ),
        (
            VehicleCommand.CABIN_HVAC_DEFROST_DEFOG,
            {"level": 1},
            None,
            "comfort.cabin.set_defrost_defog",
            b"\x08\x03",
        ),
        (
            VehicleCommand.CABIN_HVAC_DEFROST_DEFOG,
            {"level": 0},
            None,
            "comfort.cabin.set_defrost_defog",
            b"\x08\x04",
        ),
        (
            VehicleCommand.CHARGING_LIMITS,
            {"SOC_limit": 80},
            None,
            "charging.energy.set_charge_limit",
            b"\x08\x50",
        ),
    ],
)
def test_encode(
    command: VehicleCommand,
    params: dict[str, Any] | None,
    model: str | None,
    rvm: str,
    payload: bytes,
) -> None:
    """Commands encode like the Rivian app's."""
    assert encode_vehicle_command(command, params, model) == (rvm, payload)


def test_feature() -> None:
    """Each command is sent over Parallax per its category's feature."""
    assert vehicle_command_feature(VehicleCommand.UNLOCK_ALL_CLOSURES) == "PVS_BD_CMD"
    assert vehicle_command_feature(VehicleCommand.PANIC_OFF) == "PVS_SEC_CMD"
    assert (
        vehicle_command_feature(VehicleCommand.CABIN_HVAC_LEFT_SEAT_VENT)
        == "PVS_COMF_CMD"
    )
    assert vehicle_command_feature(VehicleCommand.START_CHARGING) == "PVS_ENRG_CMD"
    assert vehicle_command_feature(VehicleCommand.WAKE_VEHICLE) is None
    assert vehicle_command_feature("NOT_A_COMMAND") is None


@pytest.mark.parametrize(
    ("command", "params"),
    [
        (VehicleCommand.WAKE_VEHICLE, None),
        (VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT, {"level": 1}),
        (VehicleCommand.CABIN_HVAC_STEERING_HEAT, {"level": 4}),
        (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 30}),
        (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 40}),
        (VehicleCommand.CHARGING_LIMITS, None),
        (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 80.5}),
        (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": "warm"}),
    ],
)
def test_invalid(command: VehicleCommand, params: dict[str, Any] | None) -> None:
    """Commands without an equivalent, or with invalid params, are rejected."""
    with pytest.raises(RivianBadRequestError):
        encode_vehicle_command(command, params)
