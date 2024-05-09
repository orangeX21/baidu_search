import requests
from lxml import etree


def get_web_page(wd, pn):
    url = 'https://www.baidu.com/s'

    # print(ua)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
        'Cookie': 'BIDUPSID=905BC976D63824F6553C88ABA9D61598; PSTM=1715248546; BAIDUID=905BC976D63824F65C6A3F577B5DCF8C:FG=1; BD_UPN=123253; BA_HECTOR=0l0gah858g2l2h2084002085j00fgs1j3p7d31t; ZFY=exc3m0VQDg7:AH9fdzMJeI6LMh9ic7j4jOCONwXsokis:C; BAIDUID_BFESS=905BC976D63824F65C6A3F577B5DCF8C:FG=1; H_PS_PSSID=40301_40446_40499_40080',
        'Host': 'www.baidu.com'
    }
    params = {
        'wd': wd,
        'pn': pn
    }
    response = requests.get(url, headers=headers, params=params)
    response.encoding = 'utf-8'
    # print(response.text)
    response = response.text
    return response


def parse_page(response):
    html = etree.HTML(response)
    selectors = html.xpath('//div[@class="c-container"]')
    data = []
    nub = 0
    for selector in selectors:
        title = "".join(selector.xpath('.//h3/a//text()'))
        titleUrl = selector.xpath('.//h3/a/@href')[0]
        print(title)
        print(titleUrl)
        nub += 1
        data.append([title, titleUrl])
    print(f"当前页一共有{nub}条标题和网址的信息！")
    return data


def save_data(datas, kw, page):
    for data in datas:
        with open(f'./百度{kw}的共{page}页的数据(xpath).csv', 'a', encoding='utf-8') as fp:
            fp.write(str(data) + '\n')
    print(f"百度{kw}的第{page}页的数据已经成功保存！")


def main():
    kw = input("请输入要查询的关键词：").strip()
    page = int(input("请一共要查询的页码："))
    for _ in range(page):
        page = str(_).strip()
        page_pn = int(page)
        page_pn = str(page_pn * 10 - 10)
        resp = get_web_page(kw, page_pn)
        datas = parse_page(resp)
        save_data(datas, kw, page)


if __name__ == '__main__':
    main()
