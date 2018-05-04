#!/usr/bin/env python
import pandas as pd
from TxtParse import TxtParse, parseHtml
from config import cluters_dict,cluters_map
# 判断网元类型
def get_cluster_type(cluster):
    _type = "None"
    for cluster_type, clusters in cluters_dict.items():
        if cluster in clusters:
            _type = cluster_type
    return _type

#判断性能指标增长或下降
def check(x):
    _flag = ""
    if str(x).startswith("-"):
        _flag = "下降"
    else:
        _flag = "增长"
    return _flag + str(x)

def get_max_cpu(df, col):
    # 将数据按网元类型分组,按col分组,并获取最大CPU和内存占用
    grouped = df.groupby(col)
    # 获取最大CPU占用和最小内存剩余
    cpu = grouped.agg("max")["CPU"]
    mem = grouped.agg("min")["内存"]
    io = grouped.agg("min")["IO"]
    cluster_types = df[col].drop_duplicates().values
    cpu_data = [[col, "最大值项:CPU", "最大值项:MEM","最大值项：IO"]]
    for cluster_type in cluster_types:
        cpu_data.append([cluster_type, cpu[cluster_type], 100-mem[cluster_type],100-io[cluster_type]])
    return cpu_data

# CPU&内存分析
def cpu_analyse(cpu_file):
    title = ['网元', '主机', 'CPU', '内存', 'IO']
    data = TxtParse(cpu_file, sep='|', titles=title)
    df = data.get_df()
    # 增加对应的网元类型
    df["网元类型"] = list(map(lambda x: get_cluster_type(x), df["网元"]))
    # 数据分割，当天，前一天，前一周
    num = df.index[df['网元'].isin(["全网昨天CPU&内存数据获取"]) == True].tolist()[0]
    num1 = df.index[df['网元'].isin(["全网前天CPU&内存数据"]) == True].tolist()[0]
    num2 = df.index[df['网元'].isin(["全网前一周CPU&内存数据"]) == True].tolist()[0]
    # 昨天AS主机性能数据
    df_td = df.loc[:num - 1]
    # 全网昨天性能数据
    df_ytd = df.loc[num + 1:num1 - 1]
    # 全网前天性能数据
    df_b4ytd = df.loc[num1 + 1:num2 - 1]
    # 全网前一周性能数据
    df_wk = df.loc[num2 + 1:]
    # 将数据进行分组处理,并转成list,方便生成HTML
    list_td_grp= get_max_cpu(df_td, col="网元")
    list_ytd_grp = get_max_cpu(df_ytd, col="网元类型")
    list_b4ytd_grp = get_max_cpu(df_b4ytd, col="网元类型")
    list_wk_grp = get_max_cpu(df_wk, col="网元类型")
    # 转为DataFrame
    df_ytd_grp = pd.DataFrame(list_ytd_grp[1:],columns=["网元类型","CPU","MEM","IO"])
    df_b4ytd_grp = pd.DataFrame(list_b4ytd_grp[1:],columns=["网元类型","CPU","MEM","IO"])
    df_wk_grp = pd.DataFrame(list_wk_grp[1:],columns=["网元类型","CPU","MEM","IO"])
    # 昨天、前天、上周数据合并为一张表
    df_temp = pd.merge(df_b4ytd_grp,df_wk_grp,how="left",on="网元类型")
    df_merge = pd.merge(df_ytd_grp,df_temp,how="left",on="网元类型")
    # 计算同比增长（前一周比较）
    df_merge["t_cpu_growth"] = (df_merge["CPU"] - df_merge["CPU_y"]) / df_merge["CPU_y"]
    df_merge["t_mem_growth"] = (df_merge["MEM"] - df_merge["MEM_y"]) / df_merge["MEM_y"]
    # 计算环比增长（前一天比较）
    df_merge["h_cpu_growth"] = (df_merge["CPU"] - df_merge["CPU_x"]) / df_merge["CPU_x"]
    df_merge["h_mem_growth"] = (df_merge["MEM"] - df_merge["MEM_x"]) / df_merge["MEM_x"]
    # 将小数转换成百分数
    for col in ["t_cpu_growth","t_mem_growth","h_cpu_growth","h_mem_growth"]:
        df_merge[col] = df_merge[col].apply(lambda x: format(x, ".2%"))
    # 将CPU MEM统一保留2位小数
    for col in ["CPU","MEM"]:
        df_merge[col] = df_merge[col].apply(lambda x: format(x, ".2f"))
    # 输出表格
    output_data = [["网元类型","性能指标分析"]]
    for i in range(len(df_merge.index)):
        str = "CPU占用: 最高	{}%	,同比(前一周同一天的数据对比){}	,环比(前一天数据对比){}, 内存占用: 最高	{}%	,同比{}	,环比\
        	{}".format(df_merge.ix[i]["CPU"],check(df_merge.ix[i]["t_cpu_growth"]),check(df_merge.ix[i]["h_cpu_growth"]),df_merge.ix[i]["MEM"],check(df_merge.ix[i]["t_mem_growth"]),check(df_merge.ix[i]["h_mem_growth"]))
        output_data.append([cluters_map.get(df_merge.ix[i]["网元类型"]),str])

    zyjh_html = parseHtml(output_data,"作业计划指标")
    cpu_today_html = parseHtml(list_td_grp, "AS主机昨日性能指标")
    cpu_yes_html = parseHtml(list_ytd_grp, "全网主机昨日性能指标")
    # cpu_week_html = parseHtml(list_wk_grp, "全网主机上周性能指标")
    cpu_html = cpu_today_html + cpu_yes_html
    return zyjh_html, cpu_html

# 业务指标分析
def quato_analyse(quato_file):
    clusters = []
    values = []
    with open(quato_file, "r") as f:
        for line in f.readlines():
            line = line.split("|")
            clusters.append(line[0])
            values.append(line[1])
    quato_name = ["2/3G 彩铃播放成功率", "2/3G V网呼叫成功率", "SCP忙时CAPS数", "二卡充值成功率"]
    quato_data = list(zip(quato_name, clusters, values))
    quato_data.insert(0, ["指标项","集群","指标"])
    quato_html = parseHtml(quato_data, title="关键业务指标")
    return quato_html