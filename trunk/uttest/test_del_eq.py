#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from service.del_eq_service import delete


class TestAddEq(object):

    @pytest.mark.parametrize("values, expected", [
        ({"snArray": "07-01-00000001"}, 0),
        ({"snArray": "07-01-00000002,07-01-00000003,07-01-00000004,07-01-00000005"}, 0),
    ])
    def test_deleq(self, values, expected):
        assert delete(values)[0] == expected


