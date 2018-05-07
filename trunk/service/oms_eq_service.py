#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback

from dao import SESSION
from utils.globals import MessageError
from utils.globals import RUNLOG
from database import Equipment


def update(values):
    """service层处理新增网关接口信息请求"""
    returnCode = 0
    errorMessage = "操作成功"
    try:
        t_ems_equipment = Equipment()
        params = {"sn": values.pop("sn")}
        query_result = t_ems_equipment.all(**params)
        if len(query_result) == 0:
            returnCode = 501001
            errorMessage = "sn信息不存在"
            return
        elif query_result[0]['sold'] == 2:
            returnCode = 501004
            errorMessage = "sn已出售"
            return
        elif query_result[0]['status'] == 0:
            returnCode = 501005
            errorMessage = "损坏设备不可被绑定"
            return
        # 更新数据到数据库(oms调用此接口，意味着设备已经被订单绑定)
        values['sold'] = 2
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
