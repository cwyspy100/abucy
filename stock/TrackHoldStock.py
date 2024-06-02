import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_all_institution_url():
    all_link = []
    url = "https://www.futunn.com/quote/institution-tracking?global_content=%7B%22promote_id%22%3A13766,%22sub_promote_id%22%3A3%7D"
    add_link = "https://www.futunn.com"
    response = requests.get(url)
    html_content = response.content
    # print(html_content)
    soup = BeautifulSoup(html_content, "html.parser")
    result = soup.find("div", {"class": "content-main"})
    links = result.find_all('a', {"class": "list-item"})
    # print(result1)
    # 遍历每个 a 标签
    for link in links:
        # 获取 href 属性
        href = link.get('href')
        # print(href)
        all_link.append(add_link+href)
    hot_institution = soup.find("div", {"class": "hot-institution-content"})
    links = hot_institution.find_all('a', {"class": "hot-institution-item"})
    # print(result1)
    # 遍历每个 a 标签
    for link in links:
        # 获取 href 属性
        href = link.get('href')
        all_link.append(add_link+href)
    return all_link


def track_hold_stock(url):
    # url = "https://www.futunn.com/quote/institution-tracking/all-institutions/255251?global_content=%7B%22promote_id%22%3A13766,%22sub_promote_id%22%3A3%7D&institution_upper=1"
    response = requests.get(url)
    html_content = response.content
    # print(html_content)
    soup = BeautifulSoup(html_content, "html.parser")
    result = soup.find("h2", {"class": "institution-name"})
    institution = result.text
    # print(result.text)
    result1 = soup.find("div", {"class": "content-main"})
    # print(result1)
    links = result1.find_all('a', class_='list-item')

    # 创建一个空的 DataFrame
    data = []
    # 遍历每个 a 标签
    for link in links:
        # 获取子元素的文本内容
        code = link.select_one('.code').text
        name = link.select_one('.name').text
        value1 = link.select('.value')[0].text
        value2 = link.select('.value')[1].text
        value3 = link.select('.value')[2].text
        value4 = link.select('.value')[3].text
        value5 = link.select('.value')[4].text
        industry = link.select_one('.industry').text
        date = link.select_one('.date').text
        file = link.select_one('.file').text

        # 将数据存储到 data 列表中
        data.append({
            '机构名称': institution,
            'code': code,
            'name': name,
            '持仓': value1,
            '变动股份': value2,
            '变动比列': value3,
            '持股市值': value4,
            '持股比列': value5,
            'industry': industry,
            'date': date,
            'file': file
        })

        # # 打印出读取的内容
        # print('code:', code)
        # print('name:', name)
        # print('持仓:', value1)
        # print('变动股份:', value2)
        # print('变动比列:', value3)
        # print('持股市值:', value4)
        # print('持股比列:', value5)
        # print('industry:', industry)
        # print('date:', date)
        # print('file:', file)
        # print('------------')

    # 创建 DataFrame
    df = pd.DataFrame(data)
    today = time.strftime('%Y%m%d')
    df.to_csv(today + '机构持仓.csv', mode='a', encoding='utf-8', index=False)
    print("institution {} finish !!".format(institution))


def track_change_stock(url):
    # url = "https://www.futunn.com/quote/institution-tracking/all-institutions/255251?global_content=%7B%22promote_id%22%3A13766,%22sub_promote_id%22%3A3%7D&institution_upper=1"
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    result = soup.find("h2", {"class": "institution-name"})
    institution = result.text
    result1 = soup.find("div", {"class": "share-holding-change"})
    result2 = result1.find_all("div", {"class": "holding-change-wrapper"})
    data = []
    today = time.strftime('%Y%m%d')
    for hold_change in result2:
        change_name = hold_change.find("p", {"class": "holding-change-name"}).text

        # 获取 list-content 中的所有 <a> 标签
        list_rows = hold_change.find_all('a', class_='list-row')
        for row in list_rows:
            code = row.find('span', class_='code').text
            name = row.find('span', class_='name').text
            number = row.find('span', class_='number').text
            ratio = row.find('span', class_='ratio').text
            data.append({
                '日期': today,
                '机构名称': institution,
                '操作类型': change_name,
                'code': code,
                'name': name,
                '变动股份': number,
                '变动比列': ratio
            })
    df = pd.DataFrame(data)
    df.to_csv(today + '机构持仓变动.csv', mode='a', encoding='utf-8', index=False)
    print("institution {} finish !!".format(institution))


if __name__ == '__main__':
    all_links = get_all_institution_url()
    for url in all_links:
        # track_hold_stock(url)
        # time.sleep(10)
        track_change_stock(url)
        time.sleep(5)

