#!/usr/bin/env python
import shutil, os
import logging
from TxtParse import TxtParse, parseHtml

def logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',filename="info.log")


if __name__ == "__main__":
    logger()
    alarm_5m_file = "history_alarm_5m.unl"
    output = "history_alarm_5m.html"
    curr_level = {
        0 : "严重",
        1 : "重要",
        2 : "次要",
        3 : "警告",
        4 : "信息"
    }
    clear_status = {
        0:"未清除",
        1:"已清除"
    }
    if os.path.exists(output):
        os.remove(output)

    if os.path.exists(alarm_5m_file):
        title = ['集群名称','告警主机','告警源','告警码','告警标题','告警实例','告警级别','告警触发时间','最近更新时间','告警累计次数','告警清除状态']
        alarm_data = TxtParse(alarm_5m_file,  sep="|", titles=title)
        df = alarm_data.get_df()
        if len(df.index) != 0:
            df["告警级别"] = df["告警级别"].apply(lambda x: curr_level.get(x))
            df["告警清除状态"] = df["告警清除状态"].apply(lambda x : clear_status.get(x))
            alarm_list = df.values.tolist()
            alarm_list.insert(0,title)
            html = parseHtml(alarm_list,title="30分钟内重要告警",return_all=True)
            shutil.copy("alarm.html", output)
            with open(output, "a") as f:
                f.write(html)
            logging.info("30分钟重要告警分析完成")
        else:
            logging.info("30分钟内暂无重要告警")
        os.remove(alarm_5m_file)
    else:
        logging.error("告警原始文件缺失：30分钟粒度")
