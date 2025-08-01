from DrissionPage import ChromiumPage
import csv


def crawl_website(url, csv_writer):
    """爬取单个网站的招聘信息并写入CSV"""
    dp = ChromiumPage()
    dp.listen.start('joblist')
    dp.get(url)

    for page in range(1, 11):  # 爬取1-10页
        print(f'正在采集{page}页的数据内容')
        try:
            r = dp.listen.wait()
            json_data = r.response.body
            jobList = json_data['zpData']['jobList']

            for job in jobList:
                dit = {
                    '职位名称': job['jobName'],
                    '薪资': job['salaryDesc'],
                    '工作地点': job['businessDistrict'],
                    '工作经验': job['jobExperience'],
                    '学历要求': job['jobDegree'],
                    '公司名称': job['brandName'],
                    '公司规模': job['brandScaleName'],
                    '行业': job['brandIndustry'],
                }
                csv_writer.writerow(dit)
                print(dit)
                dp.scroll.to_bottom()
        except Exception as e:
            print(f"第{page}页爬取出错: {e}")
            continue  # 出错时继续下一页

    dp.quit()  # 关闭当前页面


# 打开CSV文件准备写入
with open('boss.csv', mode='w', encoding='utf-8', newline='') as f:
    # 确保fieldnames包含所有需要的字段（包括薪资）
    csv_writer = csv.DictWriter(f, fieldnames=[
        '职位名称',
        '工作地点',
        '工作经验',
        '学历要求',
        '公司名称',
        '公司规模',
        '行业',
        '薪资'  # 新增薪资字段，解决之前的错误
    ])
    csv_writer.writeheader()

    # 定义要爬取的网站列表
    websites = [
        # 第一个网站：北京的Python相关职位
        'https://www.zhipin.com/web/geek/jobs?city=100010000&position=290166',
        # 第二个网站：上海的Python相关职位（示例）
        'https://www.zhipin.com/web/geek/jobs?city=101020100&position=290166'
    ]

    # 依次爬取每个网站
    for i, url in enumerate(websites, 1):
        print(f"\n===== 开始爬取第{i}个网站: {url} =====")
        crawl_website(url, csv_writer)
        print(f"===== 第{i}个网站爬取完成 =====")

print("所有网站爬取完成！")