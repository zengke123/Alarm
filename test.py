import datetime
import shutil
import re
from TxtParse import parseHtml
today = datetime.date.today()


def get_data(unl):
    with open(unl, "r") as f:
        lines = f.readlines()
        data = [ line.split("|") for line in lines ]
    for x in data:
        try:
            x.remove("\n")
        except ValueError:
            pass
    return data

def user_analyse():
    today = datetime.date.today().strftime("%Y%m%d")
    vpmn_file = "vpmnvolteuser." + str(today) + ".unl"
    hjh_file = "hjhvolteuser." + str(today) + ".unl"
    pyq_file = "pyqvolteuser." + str(today) + ".unl"
    crbt_file = "crbttjvolte." + str(today) + ".unl"
    vpmn = float(get_data(vpmn_file)[0][0])
    hjh = float(get_data(hjh_file)[0][0])
    pyq = float(get_data(pyq_file)[0][0])
    crbt = sum([ float(x[1]) for x in get_data(crbt_file)])

    data = [["系统承载业务","用户类别","用户数"]]
    data.append(["VPMN","Volte",format(vpmn,",")])
    data.append(["合家欢","Volte",format(hjh,",")])
    data.append(["朋友圈","Volte",format(pyq,",")])
    data.append(["彩铃","Volte",format(crbt,",")])
    user_html = parseHtml(data, title="业务用户数",return_all=True)
    return user_html


def getMaxNum():
    today = datetime.date.today().strftime("%Y%m%d")
    record_file = "tjnew." + str(today) + ".unl"
    record_data =get_data(record_file)
    MaxStreamNumber = None
    MaxCluster = None
    for x in record_data:
        if re.match('scp[1-9]{3}',str(x[0])):
            MaxCluster = x[0]
            MaxStreamNumber = x[1].strip("\n")
            break
    return MaxCluster, MaxStreamNumber


def quato_analyse(quato_file):
    clusters = []
    values = []
    with open(quato_file, "r") as f:
        for line in f.readlines():
            line = line.split("|")
            clusters.append(line[0])
            values.append(line[1])
    MaxCluster , MaxStreamNumber = getMaxNum()
    clusters.append(MaxCluster)
    values.append(MaxStreamNumber)
    quato_name = ["2/3G 彩铃播放成功率", "2/3G V网呼叫成功率", "SCP忙时CAPS数","SCP话单流水号"]
    quato_data = list(zip(quato_name, clusters, values))
    quato_data.insert(0, ["指标项","集群","指标"])
    quato_html = parseHtml(quato_data, title="关键业务指标",return_all=True)
    return quato_html




if __name__ == "__main__":
    today = datetime.date.today()
    test = "test.html"
    quato_file = "ywzb" + str(today) + ".unl"
    shutil.copy("alarm.html", test)
    # user_html = user_analyse()
    quato_html = quato_analyse(quato_file)
    with open(test, "a") as f:
        f.write(quato_html)

