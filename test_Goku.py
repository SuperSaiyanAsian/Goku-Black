#! /usr/bin/env python3
import pytest

from Goku import update_stats


def test_update_stats():
    with pytest.raises(Exception):
        update_stats()
