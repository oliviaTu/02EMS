#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback

from dao import SESSION
from utils.globals import MessageError
from utils.globals import RUNLOG
from database import Equipment


def update(values):
    """service层处理更新设备信息"""
    returnCode = 0
    errorMessage = "操作成功"
    try:
        t_ems_equipment = Equipment()
        # 查询需更新信息是否存在
        params = {"sn": values["sn"]}
        query_result = t_ems_equipment.all(**params)

        for item in values.keys():
            if item not in ['sn', 'status', 'desc']:
                values.pop(item)

        if len(query_result) == 0:
            returnCode = 501001
            errorMessage = "sn信息不存在"
        data_result = t_ems_equipment.update(values, **params)
        if data_result == 0:
            returnCode = 501100
            errorMessage = "操作数据库错误"

    except BaseException:
        returnCode = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        return returnCode, errorMessage
