#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
import datetime
from dao import SESSION
from utils.globals import MessageError
from utils.globals import RUNLOG
from database import Equipment, FailingSn


def insert(values):
    """service层处理新增网关接口信息请求"""

    returnCode = 0
    errorMessage = "操作成功"
    recordNum = 0
    try:
        if len(values['sn']) == 0:
            returnCode = 501400
            errorMessage = 'sn参数不合法'
            return
        # way判断新增设备的方式，0单条 1批量
        if int(values["way"]) == 0:
            recordNum = 1
            values.pop("way")
            eq_type = values['sn'].split("-")
            if len(eq_type) < 3:
                returnCode = 501400
                errorMessage = 'sn参数不合法'
                return
            values['eq_type'] = eq_type[1]
            # 插入数据到数据库
            if len(values['sn']) != 14:
                returnCode = 501400
                errorMessage = "sn参数不合法"
                return
            
            returnCode, errorMessage = db_insert(values)

        elif int(values["way"]) == 1:
            start_num = values.pop("startValue")
            end_num = values.pop("endValue")
            if (start_num == end_num) or (len(start_num) != 8) or (len(end_num) != 8):
                returnCode = 501400
                errorMessage = "sn参数不合法"
                return
            sn_former = values["sn"] + '-'
            recordNum = 0
            eq_type = sn_former.split("-")
            values['eq_type'] = eq_type[1]

            snum = 0
            for index in end_num:
                if index != '0':
                    break
                else:
                    snum = snum + 1
                    if end_num[snum] != '0':
                        break

            if snum != 0:
                # endnum中不是有效数字，需要处理数字前面的0,（先判断并分离前面的0，在做循环）
                sn_former = sn_former + end_num[:snum]
                for num in range(int(start_num[snum - 1:]), int(end_num[snum - 1:]) + 1):
                    digit_num = len(str(int(end_num) + 1))
                    len_num = len(str(num))
                    if len_num < digit_num:
                        num = (digit_num - len_num) * '0' + str(num)
                    recordNum += 1
                    values["sn"] = sn_former + str(num)
                    print values["sn"]
                    # if len(values['sn']) != 14:
                    #     returnCode = 501400
                    #     errorMessage = "sn参数不合法"
                    #     continue
                    returnCode, errorMessage = db_insert(values)
            else:
                # endnum 全是有效数字，例如10000000
                for num in range(int(start_num), int(end_num) + 1):
                    recordNum += 1
                    values["sn"] = sn_former + str(num)
                    print values["sn"]
                    # if len(values['sn']) != 14:
                    #     returnCode = 501400
                    #     errorMessage = "sn参数不合法"
                    #     return
                    returnCode, errorMessage = db_insert(values)

    except BaseException:
        returnCode = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        return returnCode, errorMessage, recordNum


def db_insert(values):
    """
    数据库插入操作
    :param values:
    :return:
    """
    returnCode = 0
    errorMessage = "操作成功"
    session = SESSION()
    try:
        t_ems_equipment = Equipment()
        if len(values['sn']) >= 16:
            RUNLOG.info("sn:%s长度大于16！！！" % values['sn'])
            failing_insert(values)
        va_sn = {'sn': values['sn']}
        data_ex = t_ems_equipment.all(**va_sn)
        if len(data_ex) != 0:
            returnCode = 501002
            errorMessage = "数据库已存在此数据"
            return
        data_result = t_ems_equipment.insert(values)
        if data_result["errorcode"] == -1:
            returnCode = 501100
            errorMessage = "操作数据库错误"
            RUNLOG.info("操作数据库错误")
            RUNLOG.info("sn:%s新增失败" % values['sn'])
            if "way" in values.keys():
                failing_insert(values)

        else:
            # RUNLOG.info("sn:%s新增成功之后，删除表t_failing_sn中的这条sn记录" %  values['sn'])
            session.query(FailingSn).filter(FailingSn.sn == values['sn']).delete(synchronize_session=False)
            session.flush()
            session.commit()

    except BaseException:
        session.rollback()
        returnCode = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        session.close()
        return returnCode, errorMessage


def failing_insert(values):
    t_failing_sn = FailingSn()
    t_failing_sn.insert(values)



