import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# Booking cost tests

def test_standard_booking():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("premium", 2, 2, False)


def test_invalid_nights():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_peak_season():
    assert booking_cost("standard", 1, 2, True) == 2500


def test_extra_guests():
    assert booking_cost("standard", 2, 3, False) == 5000


def test_long_stay_discount():
    assert booking_cost("standard", 7, 2, False) == 12600


# Cancellation refund tests

def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_half_refund():
    assert cancellation_refund(1000, 3, False) == 500


def test_no_refund():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_bonus():
    assert cancellation_refund(1000, 3, True) == 750


# Room upgrade tests

def test_no_rooms_available():
    assert room_upgrade("standard", True, 0) == "standard"


def test_standard_member_upgrade():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_deluxe_member_upgrade():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_no_upgrade_for_non_member():
    assert room_upgrade("standard", False, 1) == "standard"