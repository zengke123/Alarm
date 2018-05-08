#!/usr/bin/env python
# 根据网管数据库导出的原始文件生成Excel报表
# VPMN-SCP-AS业务报表
# Volte彩铃业务报表
# 主机性能报表

import os
import datetime
import logging
from TxtParse import TxtParse

def format_excel(file,tb_title,tb_name):
    excel = TxtParse(file, sep="|", titles=tb_title)
    excel.to_excel(tb_name)

def main():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    catas_file = "volte_crbt" + str(yesterday) + ".unl"
    scpas_file = "volte_scpas" + str(yesterday) + ".unl"
    host_file = "host" + str(yesterday) + ".unl"
    if os.path.exists(catas_file):
        catas_title = ['网元标识', '网元名称', '统计开始时间', '统计结束时间', '占用次数(次)',
                       '接通次数(次),', '应答次数/呼叫成功次数(次)	', '彩铃调用次数(次)',
                       '彩铃调用成功次数(次)', '呼叫成功数(次)', '呼叫失败数(次)',
                       '会话正常释放次数(次)', '会话建立时间(毫秒)', '通话持续时长(秒)',
                       '振铃持续时长(秒)', '转发INVITE次数(次)', '收到180次数(次)', '与MS之间交互异常次数(次)',
                       '播放高清铃音次数(次)', '播放标清铃音次数(次)', '被叫关机次数(次)', '网络决定忙次数(次)',
                       '主叫早释次数(次)', '被叫终端将主叫设置为黑名单次数(次)', '平均会话建立时间(秒)',
                       'ms资源申请成功率(%)', '平均通话时长(秒)', '平均振铃时长(秒)', '被叫接听比率(%)',
                       'invite响应率(%)', '彩铃放音成功率(%)', '网络接通率(%)', '处理器平均负荷(%)',
                       '处理器的最大负荷(%)', '处理器过载时长(秒)', '系统内存占用率(%)',
                       'AS平均CAPS(Erl)', 'none1', 'none2']
        catas_xlsx = "volte_crbt_" + str(yesterday) + ".xlsx"
        format_excel(catas_file, catas_title, catas_xlsx)
        logging.info("正在生成报表：" + catas_xlsx)
    else:
        logging.error(catas_file + "原始文件不存在")

    if os.path.exists(scpas_file):
        scpas_title = ['网元编号', '网元名称', '开始时间', '结束时间', '群内试呼(次)', '群内接通	', '群内应答(次)	',
                       '群外呼出试呼(次)', '群外呼出接通(次)', '群外呼出应答(次)', '群外呼入试呼(次)', '群外呼入接通(次)',
                       '群外呼入应答(次)', '群内呼出平均占用时长(Erl)', '群内呼出平均接通时长(Erl)', '群内呼出平均应答时长(Erl)',
                       '群外呼入平均占用时长(Erl)', '群外呼入平均接通时长(Erl)', '群外呼入平均应答时长(Erl)',
                       '群外呼出平均占用时长(Erl)', '群外呼出平均接通时长(Erl)', '群外呼出平均应答时长(Erl)', '群内呼出接通率(%)',
                       '群内呼出应答率(%)', '群外呼出接通率(%)', '群外呼出应答率(%)', '群外呼入接通率(%)', '群外呼入应答率(%)',
                       'AS平均CAPS	', '群内呼叫占用时长(秒)', '群内呼叫接通时长(秒)', '群内呼叫应答时长(秒)',
                       '群外呼入占用时长(秒)', '群外呼入接通时长(秒)', '群外呼入应答时长(秒)', '群外呼出占用时长(秒)',
                       '群外呼出接通时长(秒)', '群外呼出应答时长(秒)', '群内呼叫试呼处理次数(次)', '群外呼入试呼处理次数(次)',
                       '群外呼出试呼处理次数(次)', '用户原因拆线次数(次)', '用户原因拆线时间(秒)', '群内呼叫invite响应率(%)',
                       '群外呼入invite响应率(%)', '群外呼出invite响应率(%)','网络接通率(%)', 'none1', 'none2', 'none3']
        scpas_xlsx = "volte_vpmn_" + str(yesterday) + ".xlsx"
        format_excel(scpas_file, scpas_title, scpas_xlsx)
        logging.info("正在生成报表：" + scpas_xlsx)
    else:
        logging.error(scpas_file + "原始文件不存在")

    if os.path.exists(host_file):
        host_title = ['开始时间', '结束时间', '集群名称', '主机名称', 'CPU负荷(%)',
                      '内存剩余率(%)', '利用率最高的分区利用率(最大值)(%)']
        host_xlsx = "host_pfmc_" + str(yesterday) + ".xlsx"
        #format_excel(host_file, host_title, host_xlsx)
        host_data = TxtParse(host_file, sep="|", titles=host_title)
        df = host_data.get_df()
        df["集群名称"] = df["集群名称"].map(str.strip)
        df["主机名称"] = df["主机名称"].map(str.strip)
        df["内存使用率(%)"] = df["内存剩余率(%)"].apply(lambda x: 100 - x)
        df.to_excel(host_xlsx,index=False)
        logging.info("正在生成报表：" + host_xlsx)
    else:
        logging.error(host_file + "原始文件不存在")


# 日志输出
def logger():
    '''''
    configure logging
    '''
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="info.log")


if __name__ == "__main__":
    logger()
    logging.info("生成AS业务报表及主机性能报表")
    main()
    logging.info("Done.")