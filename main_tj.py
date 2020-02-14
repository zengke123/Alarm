#!/usr/bin/env python
# 生成每日告警分析
# 生成业务指标统计

import datetime
import os
import shutil
import logging
import db
from TxtParse import TxtParse
from alarm_tj import alarm_analyse, alarm_compare_new, alarm_to_db

def logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filename="info.log")

if __name__ == "__main__":
    logger()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    # 生成历史告警文件
    # 待处理文件
    file_today = "history_alarm_" + str(today) + ".unl"
    file_yesterday = "history_alarm_" + str(yesterday) + ".unl"
    # 输出文件
    alarm_report = "report_alarm_" + str(today) + ".html"
    alarm_xlsx = "history_alarm_export_" + str(today) + ".xlsx"
    title = ['告警ID', '业务平台ID', '业务平台名称', '集群ID', '集群名称', '主机ID',
             '主机名称', '账户', '告警源', '告警码', '告警标题', '告警原因', '告警影响',
             '告警解决方法', '告警类型', '告警类别', '是否关联', '告警实例', '告警级别',
             '告警触发时间', '最近更新时间', '告警累计次数', '告警确认状态', '告警确认时间',
             '告警确认人', '告警清除状态', '告警清除类型', '告警清除时间', '告警清除人', '告警值',
             '告警附加信息', '告警过滤方式', '是否派工单']
    if os.path.exists(alarm_report):
        os.remove(alarm_report)
    shutil.copy("alarm.html", alarm_report)

    if os.path.exists(file_today):
        alarm = TxtParse(file_today, sep="|", titles=title)
        alarm.to_excel(alarm_xlsx)
        df = alarm.get_df()
        try:
            db.create_engine('root', '123456', 'tongji', '127.0.0.1')
            alarm_to_db(db, df)
        except Exception as e:
            logging.error("告警入库失败")

        try:
            t_start = '<table class="tableizer-table" cellspacing=0 width="95%";>\n'
            t_end = '</table>\n'
            today_alarm, _ = alarm_analyse(df)
            logging.info("今日告警分析生成成功")
            if os.path.exists(file_yesterday):
                try:
                    alarm_old = TxtParse(file_yesterday, sep="|", titles=title)
                    df_old = alarm_old.get_df()
                    clear_alarm, same_alarm, add_alarm = alarm_compare_new(df, df_old)
                    today_alarm = add_alarm + today_alarm + same_alarm + clear_alarm
                    logging.info("告警同比分析生成成功")
                except:
                    pass
            # 生成告警分析HTML
            with open(alarm_report, "a") as f:
                f.write(t_start + today_alarm + t_end)
            os.system("sh up2.sh > /dev/null")
        except:
            logging.error("生成告警分析文件失败")
    else:
        logging.error("历史告警文件缺失")