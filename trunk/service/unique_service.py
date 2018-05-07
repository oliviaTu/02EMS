#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
#————————————————————————————————————————————————————
# Copyright (python) ,2016-2036, Sowell Tech. Co,Ltd
# FileName: unique_service.py
# Version: 0.0.1
# Author : YouShaoPing
# LastChange: 2017-02-20
# Desc:
# History:
#————————————————————————————————————————————————————
"""
import traceback

from utils.globals import MessageError
from utils.globals import RUNLOG
# from database import NetElement
# from database import Group
# from database import User
from database import Equipment, FailingSn


def unique_query(values):
    """service层处理查询服务器负载信息请求"""
    errorMessage = "操作成功"
    returnCode = 0
    t_net_element = Equipment()
    # t_group = FailingSn()
    # t_user = User()
    # t_cdn_gateway = CDNGateWay()
    size = 0
    try:
        count_params = {}
        if "flag" in values:
            examine_column = values["examine_column"].split(",")
            examine_data = values["examine_data"].split(",")
            for index in xrange(0,len(examine_column)):
                    count_params[examine_column[index]] = examine_data[index]
        else:
            count_params[values["examine_column"]] = values["examine_data"]
            # 根据网元id精确查询

        if int(values["unique_type"]) == 1:
            size = t_net_element.count("table_id", **count_params)
        # elif int(values["unique_type"]) == 2:
        #     print count_params
        #     size = t_group.count("table_id", **count_params)
        #     print "=================size================"
        #     print size
        # elif int(values["unique_type"]) == 3:
        #     size = t_user.count("table_id", **count_params)
        # elif int(values["unique_type"]) == 4:
        #     pass
        # elif int(values["unique_type"]) == 5:
        #     size = t_cdn_gateway.count("table_id", **count_params)
            # from dao import SESSION
            # from utils.globals import converter
            # 测试mysql的session,是ok的
            # session = SESSION()
            # obj = session.query(CDNGateWay).filter(CDNGateWay.name == count_params['name']).order_by(CDNGateWay.table_id.desc()).all()
            # obj2 = converter(obj)
            # size = len(obj2)
            # session.close()
            # print t_cdn_gateway.all(**count_params)
        else:
            raise MessageError(501004, "参数错误")
        if size != 0:
            raise MessageError(501007, "参数已存在")

    except MessageError, ex:
        returnCode = ex.error_code
        errorMessage = ex.errorMessage

    except BaseException:
        returnCode = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        result = {
            "returnCode": returnCode,
            "errorMessage": errorMessage,
        }
    return result
