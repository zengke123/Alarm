#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid
from email.header import Header

class MailSender():
    _attachments = []

    # 初始化邮件服务器，邮件体
    def __init__(self,server,user,passwd):

        self.server = smtplib.SMTP(server)
        #self.server.set_debuglevel(1)
        self.server.login(user,passwd)
        print("Connect to the mail server...")
        self.msg = MIMEMultipart()
        self.msg['From'] = user
        self.msg['Date'] = formatdate(localtime=1)
        self.msg['Message-ID'] = make_msgid()
        print("Connection succeeded...")

    #邮件主题、正文
    def add_content(self,sub,content):
        self.msg.attach(MIMEText(content, 'html', 'utf-8'))
        self.msg['Subject'] = sub

    # 添加附件
    def add_attachment(self,file):
        mime = MIMEApplication(open(file, "rb").read())
        #mime.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', filename))
        mime.add_header('Content-Disposition', 'attachment', filename=Header(file,"gbk").encode())
        self._attachments.append(mime)

    def send(self,to_addr):
        self.msg['To'] = to_addr
        for mime in self._attachments:
            self.msg.attach(mime)
        try:
            self.server.sendmail(self.msg['From'], self.msg['To'].split(','), self.msg.as_string())
            return True
        except Exception:
            return False


    def close(self):
        self.server.quit()
        print("Connection closed...")

