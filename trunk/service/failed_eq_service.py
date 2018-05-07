#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
import datetime
from dao import SESSION
from utils.globals import MessageError
from utils.globals import RUNLOG
from database import Equipment, ImportRecord, FailingSn


def query(values):
    """service层处理查询网关接口信息请求"""
    returnCode = 0
    errorMessage = "操作成功"
    eq_info_list = []
    total_size = 0
    t_emsfail_eq = FailingSn()
    try:
        # 一次查询条数
        params = {"filters": []}
        count_params = {"filters": []}
        params["limit"] = values['pageSize']
        params["offset"] = int(values["pageNum"]) - 1

        params["order_by"] = "update_time"
        params["direction"] = "desc"
        # 根据sn模糊查询
        if "sn" in values.keys():
            str = values["sn"]
            str = str.replace('%', '[%')
            sn = str.replace('_', '[_')
            params["filters"].append({"op": "like", "value": sn, "name": "sn"})
            count_params["filters"].append({"op": "like", "value": sn, "name": "sn"})

        # 根据eq_type模糊查询
        if "eqType" in values.keys():
            strs = values["eqType"]
            strs = strs.replace('%', '[%')
            eqType = strs.replace('_', '[_')
            params["filters"].append({"op": "==", "value": eqType, "name": "eq_type"})
            count_params["filters"].append({"op": "==", "value": eqType, "name": "eq_type"})

        # 根据起始时间模糊查询startTime，endTime
        if "startTime" in values.keys():
            str = values["startTime"]
            str = str.replace('%', '[%')
            startTime = str.replace('_', '[_')
            params["filters"].append({"op": ">=", "value": startTime, "name": "update_time"})
            count_params["filters"].append({"op": ">=", "value": startTime, "name": "update_time"})

        if "endTime" in values.keys():
            str = values["endTime"]
            str = str.replace('%', '[%')
            endTime = str.replace('_', '[_')
            params["filters"].append({"op": "<=", "value": endTime, "name": "update_time"})
            count_params["filters"].append({"op": "<=", "value": endTime, "name": "update_time"})

        # 数据库查询
        eq_info_list = t_emsfail_eq.all(**params)
        # for eq_info in eq_info_list:
        #     eq_info['update_time'] = eq_info['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        if len(eq_info_list) != 0:
            for eq_info in eq_info_list:
                if "update_time" not in eq_info.keys() or not eq_info['update_time']:
                    continue
                else:
                    eq_info['update_time'] = eq_info['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        total_size = t_emsfail_eq.count("sn", **count_params)

    except BaseException:
        returnCode = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        result = {"returnCode": returnCode, "errorMessage": errorMessage}
        result['list'] = eq_info_list
        result['total'] = total_size            # 总记录数
        # result['size'] = len(eq_info_list)                  # 当前页的数量
        result['pages'] = int(total_size)/int(values['pageSize'])                 # 总页数
        if int(total_size) % int(values['pageSize']) != 0:
            result['pages'] = result['pages'] + 1
        # result['pageNum'] = values['pageNum']                # 当前页
        result['pageSize'] = values['pageSize']               # 每页的数量
        return result
