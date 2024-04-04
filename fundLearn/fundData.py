


from bs4 import BeautifulSoup
import urllib.request
import json

# 获取基金数据
# 从天天基金网获取基金数据
def getFundData(fundCode):
    # 从天天基金网获取基金数据
    # fundCode: 基金代码
    # 返回值: 基金数据
    # 说明: 基金数据为json格式
    # 例子: http://fundgz.1234567.com.cn/js/001186.js?rt=1463558676006
    # 返回: jsonpgz({"fundcode":"001186","name":"富国文体健康股票","jzrq":"2016-05-17","dwjz":"1.0680","gsz":"1.0680","gszzl":"0.00","gztime":"2016-05-18 15:00"});
    # 说明: jsonpgz(后面的数据为json格式)
    # fundCode = '001186'
    #     'fundcode': 基金代码，例如 '000001'。
    # 'name': 基金名称，例如 '华夏成长混合'。
    # 'jzrq': 净值日期，表示基金净值的日期，例如 '2023-09-14'。
    # 'dwjz': 单位净值，即每份基金的净值，例如 '0.8890'。
    # 'gsz': 估算净值，表示基金的估算净值，例如 '0.8883'。
    # 'gszzl': 估算涨跌百分比，表示基金的估算涨跌幅度，例如 '-0.08'，表示跌了0.08%。
    # # 'gztime': 估值时间，表示估算净值的时间，例如 '2023-09-15 15:00'。

    url = 'http://fundgz.1234567.com.cn/js/' + fundCode + '.js?rt=1463558676006'
    # print(url)
    # 获取数据

    response = urllib.request.urlopen(url)
    # 读取数据
    data = response.read()
    # print(data)
    # 转换为字符串
    dataStr = data.decode('utf-8')
    # print(dataStr)
    # 去掉jsonpgz(
    dataStr = dataStr.replace('jsonpgz(', '')
    # 去掉最后的分号
    dataStr = dataStr.replace(');', '')
    # print(dataStr)
    # 转换为json格式
    dataJson = json.loads(dataStr)
    # print(dataJson)
    return dataJson

print(getFundData('001186'))



# 从天天基金网获取所有的基金code
def getFundCode(url):
    # 从天天基金网获取所有的基金code
    # 返回值: 基金代码列表
    # 说明: 基金代码列表为字符串列表
    # 例子: http://fund.eastmoney.com/js/fundcode_search.js
    # 返回: var r = [ ["000001","华夏成长混合","华夏基金","混合型"], ["000002","华夏成长混合","华夏基金","混合型"], ... ];
    # 说明: r为基金代码列表，每个元素为一个列表，包含4个元素，分别为基金代码、基金名称、基金公司名称、基金类型。
    # url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    # print(url)
    # 获取数据
    response = urllib.request.urlopen(url)
    # 读取数据
    data = response.read()
    print(type(data))
    # 转换为字符串
    dataStr = data.decode('utf-8-sig')
    # print(type(dataStr)
    dataJson = json.loads(dataStr)
    print(dataJson)
    # 获取基金代码列表
    fundCodeList = []
    for fundCode in dataJson:
        fundCodeList.append(fundCode[0])
    return fundCodeList


fundCodeList = getFundCode('http://fund.eastmoney.com/js/fundcode_search.js')









# fundCodes = '[["000001","HXCZHH","华夏成长混合","混合型-灵活","HUAXIACHENGZHANGHUNHE"],["000002","HXCZHH","华夏成长混合(后端)","混合型-灵活","HUAXIACHENGZHANGHUNHE"]]'
# fundCodes = json.loads(fundCodes)
# for fundCode in fundCodes:
#     print(fundCode[0])

# # 如何能将上面fundCodes解析为json
# def parseFundCodes(fundCodes):
#     for subList in fundCodes:
#         print(subList)

# parseFundCodes(fundCodes)



# 从天天基金网获取所有基金code

# get funccode from http://fund.eastmoney.com/js/fundcode_search.js
