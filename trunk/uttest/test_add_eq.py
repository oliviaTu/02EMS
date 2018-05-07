#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from service.add_eq_service import insert
from service.del_eq_service import delete


class TestAddEq(object):
    @pytest.mark.parametrize("values, expected",[
        ({"way": 0, "sn": "07-01-00000001", "status": 1}, 0),
        ({"way": 0, "sn": "07-01-00000002", "status": 1}, 0),
        ({"way": 1, "sn": "07-01", "endValue": "00000005", "startValue": "00000003", "status": 1}, 0),
        ])
    def test_addeq(self, values, expected):
        assert insert(values)[0] == expected
