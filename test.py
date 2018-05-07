#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# ————————————————————————————————————————————————————
# Copyright (python) ,2018-2038, SVI
# FileName: user_table.py
# Version: 1.0
# Author : Payne
# LastChange: 2018-03-02
# Desc:异常支付信息表
# History:
# ————————————————————————————————————————————————————
"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import VARCHAR, TEXT
from sqlalchemy import Index
from sqlalchemy.dialects.mysql import TINYINT, DATETIME, DECIMAL, DATE
from dao import Base
from dao.base import BaseWrapper


class BadPay(Base, BaseWrapper):
    """
        【异常支付信息表】

    """

    __tablename__ = 't_bad_pay'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    userId = Column("user_id", VARCHAR(36))
    mobile = Column("mobile", VARCHAR(32))
    payType = Column("pay_type", TINYINT)
    badType = Column("bad_type", TINYINT, nullable=False)
    deviceType = Column("device_type", TINYINT)
    status = Column("status", TINYINT)
    bank = Column("bank", VARCHAR(255), nullable=False)
    money = Column("money", DECIMAL(10, 2), nullable=False)
    account = Column("account", VARCHAR(255), nullable=False)
    payTime = Column("pay_time", DATETIME)
    createTime = Column("create_time", DATETIME)
    updater = Column("updater", VARCHAR(255))
    updateTime = Column("update_time", DATETIME)
    remark = Column("remark", VARCHAR(255))
    day = Column(Integer)
    content = Column("content", TEXT)

    # mysql_engine = 'InnoDB'
    # mysql_charset = 'utf8'

    def __init__(self):
        BaseWrapper.__init__(self, self.__class__)

