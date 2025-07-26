import resp
from DrissionPage import ChromiumPage
from pprint import pprint
import csv
import time  # 新增，用于添加暂停时间

# 定义要爬取的不同网址列表
urls = [
    "https://www.zhipin.com/web/geek/job?city=100010000&position=290166",
    "https://www.zhipin.com/web/geek/job?city=100010000&position=100125",
    "https://www.zhipin.com/web/geek/job?city=100010000&position=100124",
    "https://www.zhipin.com/web/geek/job?city=100010000&position=101305",
    "https://www.zhipin.com/web/geek/job?query=python&city=100010000",
    "https://www.zhipin.com/web/geek/job?query=java&city=100010000",
    "https://www.zhipin.com/web/geek/job?query=C%23&city=100010000",
    "https://www.zhipin.com/web/geek/job?query=.NET&city=100010000",
    "https://www.zhipin.com/web/geek/job?query=%E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88&city=100010000",
    "https://www.zhipin.com/web/geek/job?query=%E8%BF%90%E7%BB%B4%E5%B7%A5%E7%A8%8B%E5%B8%88&city=100010000",
    "https://www.zhipin.com/web/geek/job?query=%E7%BD%91%E7%BB%9C%E5%B7%A5%E7%A8%8B%E5%B8%88&city=100010000",
    "https://www.zhipin.com/web/geek/job?query=IT%E6%8A%80%E6%9C%AF%E6%94%AF%E6%8C%81&city=100010000",
    "https://www.zhipin.com/web/geek/job?city=100010000&position=100408",
]
# 创建文件对象，所有数据都存入boss.csv
f = open('boss.csv', mode='w', encoding='utf-8', newline='')
# 字典写入方法
csv_writer = csv.DictWriter(f, fieldnames=['岗位名称',
                                           '公司名称',
                                           '招聘地区',
                                           '要求工作经验',
                                           '要求学历',
                                           '薪水',
                                           '职位技能关键词',
                                           '职位信息',
                                           '岗位要求',
                                           '岗位详情页链接',
                                           '岗位联系人',
                                           '联系人职位',
                                           '福利'
])
# 写入表头
csv_writer.writeheader()
# 实例化浏览器对象
dp = ChromiumPage()

# 循环处理每个网址
for url in urls:
    # 监听数据包
    dp.listen.start('search/joblist.json')
    # 访问当前循环对应的网址
    dp.get(url)
    # 循环翻页
    for page in range(1, 10):
        print(f'正在采集第{page}页（对应网址 {url}）的数据内容')
        # 下滑网页页面到底部
        dp.scroll.to_bottom()
        # 等待数据包加载
        resp = dp.listen.wait()
        # 获取响应数据
        json_data = resp.response.body
        # 提取职位信息所在列表
        jobList = json_data['zpData']['jobList']
        # for循环遍历, 提取列表里面元素 (30个岗位信息)
        for index in jobList:
            # 提取字段内容，保存到字典
            dit = {
                '岗位名称': index['jobName'],
                '公司名称': index['brandName'],
                '招聘地区': index['cityName'],
                '要求工作经验': index['jobExperience'],
                '要求学历': index['jobDegree'],
                '薪水': index['salaryDesc'],
                '职位技能关键词': index['jobName'],
                '职位信息': index['jobName'],
                '岗位要求': index['skills'],
                '岗位详情页链接': index['brandLogo'],
                '岗位联系人': index['bossName'],
                '联系人职位': index['bossTitle'],
                '福利': index['welfareList']
            }
            # 写入数据
            csv_writer.writerow(dit)
            print(dit)
        # 判断是否是最后一页，如果是最后一页则不点击下一页（避免报错，因为最后一页没有下一页按钮了）
        if page < 10:
            dp.ele('css:.ui-icon-arrow-right').click()
            time.sleep(0.5)  # 每翻一页暂停0.5秒

# 关闭文件对象
f.close()