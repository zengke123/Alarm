#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 2018-04-28
import datetime
import os
import logging
from MailSender import MailSender
from MailConfig import Config

def logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',filename="mail.log")

if __name__ =="__main__":
    logger()
    now = datetime.datetime.now().strftime("%m-%d %H:%M")
    report_alarm = "history_alarm_5m.html"
    config = Config()
    server = config.server
    mail_user = config.user
    mail_password = config.password
    send_addr = config.test_addr
    sub_title = "【重要告警提醒】 " + str(now)
    if os.path.exists(report_alarm):
        Mail = MailSender(server, mail_user, mail_password)
        with open(report_alarm, "r") as file:
            lines = file.readlines()
        content = "".join([line for line in lines])
        Mail.add_content(sub_title,content)
        if Mail.send(send_addr):
            logging.info("30分钟内重要告警发送成功")
            try:
                os.remove(report_alarm)
            except:
                logging.error("删除文件错误")
        Mail.close()
    else:
        logging.info("30分钟内无重要告警")

