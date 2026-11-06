
import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# --------------------------------------------------
# 1. BOOKING COST – Decision and branch coverage
# --------------------------------------------------

def test_valid_room():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_invalid_room():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("invalid", 2, 2, False)


def test_valid_nights():
    assert booking_cost("standard", 1, 2, False) == 2000


def test_invalid_nights():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_peak_season_true():
    assert booking_cost("standard", 1, 2, True) == 2500


def test_peak_season_false():
    assert booking_cost("standard", 1, 2, False) == 2000


def test_extra_guests_true():
    assert booking_cost("standard", 2, 3, False) == 5000


def test_extra_guests_false():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_long_stay_discount_true():
    assert booking_cost("standard", 7, 2, False) == 12600


def test_long_stay_discount_false():
    assert booking_cost("standard", 6, 2, False) == 12000


# --------------------------------------------------
# 2. CANCELLATION REFUND – Decision and branch coverage
# --------------------------------------------------

def test_refund_seven_or_more_days():
    assert cancellation_refund(1000, 7, False) == 1000


def test_refund_between_two_and_six_days():
    assert cancellation_refund(1000, 3, False) == 500


def test_refund_less_than_two_days():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_bonus_true():
    assert cancellation_refund(1000, 3, True) == 750


def test_member_bonus_false():
    assert cancellation_refund(1000, 3, False) == 500


# --------------------------------------------------
# 3. ROOM UPGRADE – Decision and branch coverage
# --------------------------------------------------

def test_no_rooms_available():
    assert room_upgrade("standard", True, 0) == "standard"


def test_rooms_available_standard_member():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_rooms_available_standard_non_member():
    assert room_upgrade("standard", False, 1) == "standard"


def test_deluxe_member_upgrade():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_deluxe_non_member_no_upgrade():
    assert room_upgrade("deluxe", False, 1) == "deluxe"


def test_suite_member_no_upgrade():
    assert room_upgrade("suite", True, 1) == "suite"
