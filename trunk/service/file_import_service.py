#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
#————————————————————————————————————————————————————
# Copyright (python) ,2016-2036, Sowell Tech. Co,Ltd
# FileName: cdn_gateway_service.py
# Version: 0.0.1
# Author : tumin
# LastChange: 2018-02-03
# Desc:
# History:
#————————————————————————————————————————————————————
"""
import traceback
import xlrd
import datetime
from dao import SESSION
from utils.globals import MessageError
from utils.globals import RUNLOG
from database import Equipment, ImportRecord, FailingSn


def analysis(path):
    """
    解析表格
    """
    list_rows = []
    returnCode = 0
    errorMessage = "操作成功"
    try:
        workbook = xlrd.open_workbook(path)
        for sheet_name in workbook.sheet_names():
            sheet2 = workbook.sheet_by_name(sheet_name)
            lst_1_line = sheet2.row_values(0)
            for row in range(1, sheet2.nrows):      # 确认读取的行数是？
                res = {}
                rows = sheet2.row_values(row)
                if row == 1:
                    eq_type = sheet2.row_values(row)[-1]
                    if not isinstance(eq_type, int):
                        if isinstance(eq_type, float):
                            RUNLOG.info("In excel, the eq_type  is  float")
                            eq_type = int(eq_type)
                        else:
                            RUNLOG.info("In excel, the eq_type  is  not  int or float")
                            returnCode = 501300
                            errorMessage = "表格不规范"
                            return
                    continue
                elif row == 2 or row == 3 or row == 4:
                    continue
                elif row != 2:
                    if not isinstance(rows, list):
                        RUNLOG.info("In excel, the rows_type  is  not  list")
                        returnCode = 501300
                        errorMessage = "表格不规范"
                        return
                    if not isinstance(rows[0], unicode):
                        RUNLOG.info("In excel, the rows[0]  is  not  unicode")
                        returnCode = 501300
                        errorMessage = "表格不规范"
                        return
                    res['sn'] = rows[0]
                res['eq_type'] = eq_type
                if row >= 3:
                    list_rows.append(res)
                else:
                    del res

    except BaseException:
        returnCode = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        return list_rows, returnCode, errorMessage


def insert(path, fileparm):
    """service层处理新增sn信息请求"""
    returnCode = 0
    errorMessage = "操作成功"
    recordNum = 0
    retude = returnCode
    try:
        # 吧文件给analysis() 解析 ！！！！
        RUNLOG.info(path)
        list_rows, returnCode, errorMessage = analysis(path)
        print list_rows
        if returnCode != 0:
            retude = returnCode
            return
        for param in list_rows:
            # 将表格中的数据存入数据库
            returnCode, errorMessage, status = db_insert(param)
            if status == 2:
                fileparm['status'] = 2
            if returnCode == 0:
                recordNum += 1
            else:
                retude = returnCode
        fileparm['file_name'] = path
        # 表格导入状态存到数据库
        t_ems_import_record = ImportRecord()
        t_ems_import_record.insert(fileparm)
    except BaseException:
        retude = 501000
        errorMessage = "系统内部错误"
        RUNLOG.error(traceback.format_exc())

    finally:
        return retude, errorMessage, recordNum


def db_insert(values):
    """
    数据库插入操作
    :param values:
    :return:
    """
    returnCode = 0
    errorMessage = "操作成功"
    session = SESSION()
    status = 1                               # 1成功  2失败
    try:
        t_ems_equipment = Equipment()
        t_failing_sn = FailingSn()
        if len(values['sn']) != 14:
            returnCode = 501400
            errorMessage = "sn参数不合法"
            fail_sn = session.query(FailingSn).filter(FailingSn.sn == values['sn']).all()
            if len(fail_sn) == 0:
                values['status'] = 2
                t_failing_sn.insert(values)
            return

        sn_obj = session.query(Equipment).filter(Equipment.sn == values['sn']).all()
        if len(sn_obj) == 0:
            data_result = t_ems_equipment.insert(values)
            if data_result["errorcode"] == -1:
                returnCode = 501100
                errorMessage = "操作数据库错误"
                RUNLOG.info("操作数据库错误")
                status = 2
                RUNLOG.info("sn:%s新增失败" % values['sn'])
                # 插入数据库失败的数据，先查看是不是已经存在设备正常表中了，如果没有，请插入到设备异常表
                if len(sn_obj) == 0:
                    values['status'] = 2
                    t_failing_sn.insert(values)

            else:
                # 对于新增成功的设备，先处理设备异常表中是否存在此设备号并删除
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
        return returnCode, errorMessage, status
