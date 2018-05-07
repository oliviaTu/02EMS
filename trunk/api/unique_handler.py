#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
#——————————————————————————
# Copyright (python) ,2016-2036, Sowell Tech. Co,Ltd
# FileName: unique_handler.py
# Version: 0.0.1
# Author :YouShaoPing
# LastChange: 2017-3-10
# Desc:
# History:
#———————————————————————————
"""
import traceback
import datetime
from json import dumps
from json import loads

from tornado import web

from service.unique_service import unique_query
from utils.globals import RUNLOG, cas
from utils.globals import MessageError


class UniqueHandler(web.RequestHandler):
    """唯一性验证接口"""

    def data_received(self, chunk):
        pass

    def get(self):
        """
            通过此接口查询系统直播流详情请求
            参数说明：
                unique_type     必选  正整数 8   表示从哪开始查询    
                examine_column  必选  字符   64  网元id
            异常：
                -1 ：      操作失败
                400:       参数错误
                500:       系统内部错误
                1000:      操作数据库错误
                5000:      输入参数已经存在
        """
        returnCode = -1
        errorMessage = "操作失败"
        total_size = 0
        result = {
            "returnCode": returnCode, 
            "errorMessage": errorMessage
        }
        values = {}
        try:
            # 读取参数
            arguments = self.request.arguments
            RUNLOG.info("receive request arguments = %s" % arguments)
            for key, value in arguments.items():
                values[key] = value[0]

            # 参数合法性校验
            for item in ["unique_type", "examine_column", "examine_data"]:
                if item not in values.keys():
                    returnCode = 401400
                    errorMessage = "参数错误"
                    raise MessageError(returnCode, errorMessage)

            result = unique_query(values)

        except MessageError, ex:
            result["returnCode"] = ex.error_code
            result["errorMessage"] = ex.errorMessage
            RUNLOG.warn("returnCode = %s, errorMessage = %s" % (returnCode, errorMessage))

        except BaseException:
            result["returnCode"] = 501000
            result["recordNum"] = "系统内部错误"
            RUNLOG.error(traceback.format_exc())

        finally:
            self.write(dumps(result))
