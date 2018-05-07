#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback

from dao import SESSION
from utils.globals import RUNLOG
from database import Equipment


def query(values):
    """service层处理查询网关接口信息请求"""
    returnCode = 0
    errorMessage = "操作成功"
    t_ems_eq = Equipment()
    try:
        # 一次查询条数
        eq_info = t_ems_eq.all(**values)
        if len(eq_info) == 0:
            returnCode = 501001
            errorMessage = "sn信息不存在"
        elif eq_info[0]['sold'] == 2:
            returnCode = 501004
            errorMessage = "sn已出售"
        elif eq_info[0]['status'] == 0:
            returnCode = 501005
            errorMessage = "sn为损坏设备"

    except BaseException:
        returnCode = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        result = {"returnCode": returnCode, "errorMessage": errorMessage}
        return result
