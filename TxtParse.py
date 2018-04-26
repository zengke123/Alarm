#!/usr/bin/env python
import pandas as pd
class TxtParse():

    def __init__(self,filename, sep, titles):
        self.df = pd.read_table(filename,index_col=False, names=titles, sep=sep, encoding="gbk")

    def to_excel(self,output):
        self.df.to_excel(output, index=False)

    def get_df(self):
        return self.df

def parseHtml(data ,title,return_all = False):
    t_start = '<table class="tableizer-table" cellspacing=0;>\n'
    t_end = '</table>\n'
    cols = len(data[0])
    rows = len(data)
    t_title = '<thead><tr class="tableizer-firstrow"><th align=left>{}</th>'.format(title)
    for i in range(cols -1):
        t_title = t_title + "<th>&nbsp;</th>"
    t_title = t_title +"</thead>"
    # 生成表格内容
    t_body = '<tbody>\n<tr bgcolor="#E0E0E0">' + "".join(["<td>" + str(data[0][i]) + "</td>" for i in range(cols)]) + "</tr>\n"
    # 逐行生成
    for i in range(1, rows):
        line = "<tr>" + "".join(["<td>" + str(data[i][j]) + "</td>" for j in range(cols)]) + "</tr>\n"
        t_body = t_body + line
    t_body = t_body + "</tbody>"
    if return_all:
        table = t_start + t_title + t_body + t_end
    else:
        table = t_title + t_body
    return table
