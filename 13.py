import requests
from pprint import pprint
import csv

# 定义要爬取的不同网址列表
urls = [
    "https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job",
]

# 创建文件对象，所有数据都存入lp.csv
f = open('lp.csv', mode='w', encoding='utf-8', newline='')
# 字典写入方法
csv_writer = csv.DictWriter(f, fieldnames=[
        '岗位名称',
        '公司名称',
        '招聘地区',
        '要求工作经验',
        '要求学历',
        '薪水',
        '职位技能关键词',
        '岗位详情页链接',
        '岗位联系人',
        '联系人职位',
])
# 写入表头
csv_writer.writeheader()

headers = {
        'Cookie': '__gc_id=f63275322c17461f95464db3c6b8f82c; _ga=GA1.1.2004545770.1733318502; __uuid=1733318502676.39; XSRF-TOKEN=OmgjIDuNSSKtkejPP6e1yw; __tlog=1733378844695.93%7C00000000%7C00000000%7C00000000%7C00000000; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1733318503,1733378845; HMACCOUNT=5EDE5D95B8B1038E; acw_tc=1a0c639717333788433905755e00c2f72ec5ed50f22aa294822ac040c1b1fe; __session_seq=12; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1733380000; __tlg_event_seq=60; _ga_54YTJKWN86=GS1.1.1733378845.2.1.1733380147.0.0.0',
        'Host': 'api-c.liepin.com',
        'Origin': 'https://www.liepin.com',
        'Referer': 'https://www.liepin.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Client-Type': 'web',
        'X-Fscp-Bi-Stat': '{"location": "https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage=0&pageSize=40&key=python&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salary=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&otherCity=&sfrom=search_job_pc&scene=condition&ckId=ljsgavdm4f2tz8w9htpt985czntc84zb&skId=hckpqfp7kzk1nmqr4ucdq7p9v1lilcg8&fkId=ljsgavdm4f2tz8w9htpt985czntc84zb&suggestId="}',
        'X-Fscp-Fe-Version': '',
        'X-Fscp-Std-Info': '{"client_id": "40108"}',
        'X-Fscp-Trace-Id': '907447b9-a551-4e49-a2b5-5a6af8216689',
        'X-Fscp-Version': '1.1',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'OmgjIDuNSSKtkejPP6e1yw',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
}

# 循环处理每个网址
for url in urls:
    # 循环爬取 10 页数据
    for page in range(1, 11):
        print(f'正在采集第{page}页（对应网址 {url}）的内容')
        data = {"data":{"mainSearchPcConditionForm":{"city":"410","dq":"410","pubTime":"","currentPage":str(page),"pageSize":40,"key":"python","suggestTag":"","workYearCode":"0","compId":"","compName":"","compTag":"","industry":"","salary":"","jobKind":"","compScale":"","compKind":"","compStage":"","eduLevel":""},"passThroughForm":{"scene":"condition","skId":"hckpqfp7kzk1nmqr4ucdq7p9v1lilcg8","fkId":"ljsgavdm4f2tz8w9htpt985czntc84zb"}}}
        try:
            response = requests.post(url=url, json=data, headers=headers)
            response.raise_for_status()  # 检查请求是否成功，若不成功则抛出异常
            json_data = response.json()
            jobCardList = json_data['data']['data']['jobCardList']
            for index in jobCardList:
                # 初始化 recruiter 字典结构，避免 KeyError
                if'recruiter' not in index:
                    index['recruiter'] = {}
                if'recruiterName' not in index['recruiter']:
                    index['recruiter']['recruiterName'] = "未知联系人"
                if'recruiterTitle' not in index['recruiter']:
                    index['recruiter']['recruiterTitle'] = "未知职位"

                dit = {
                    '岗位名称': index['job']['title'],
                    '公司名称': index['comp']['compName'],
                    '招聘地区': index['job']['dq'],
                    '要求工作经验': index['job']['requireWorkYears'],
                    '要求学历': index['job']['requireEduLevel'],
                    '薪水': index['job']['salary'],
                    '职位技能关键词': ','.join(index['job']['labels']),
                    '岗位详情页链接': index['job']['link'],
                    '岗位联系人': index['recruiter']['recruiterName'],
                    '联系人职位': index['recruiter']['recruiterTitle'],
                }
                csv_writer.writerow(dit)
                print(dit)
        except requests.RequestException as e:
            print(f"请求第{page}页（对应网址 {url}）数据出现错误: {e}")
            continue  # 出现错误则跳过当前页，继续采集下一页数据
        except KeyError as ke:
            print(f"解析第{page}页（对应网址 {url}）数据出现键错误: {ke}")
            continue  # 出现键不存在等解析错误也跳过当前页，继续采集下一页数据
        except Exception as ex:
            print(f"采集第{page}页（对应网址 {url}）数据出现其他未知错误: {ex}")
            continue  # 出现其他未知错误同样跳过当前页，继续采集下一页数据
# 关闭文件对象
f.close()