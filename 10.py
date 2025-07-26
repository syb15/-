# 导入自动化模块
from DrissionPage import ChromiumPage
# 导入格式化输出模块
import json
# 导入csv模块
import csv

# 定义要爬取的不同网址列表
urls = [
    "https://we.51job.com/pc/search?jobArea=000000&keyword=%E7%AE%97%E6%B3%95&searchType=2&keywordType=",
]

# 创建文件对象，所有数据都存入qc.csv
f = open('qc9.csv', mode='w', encoding='utf-8', newline='')
# 字典写入方法
csv_writer = csv.DictWriter(f, fieldnames=[
        '岗位名称',
        '招聘地区',
        '招聘城区',
        '要求工作经验',
        '要求学历',
        '薪水',
        '发布时间',
        '公司名称',
        '公司信息',
        '职位技能关键词',
])
# 写入表头
csv_writer.writeheader()

# 实例化浏览器对象
dp = ChromiumPage()

# 循环处理每个网址
for url in urls:
    # 访问当前循环对应的网址
    dp.get(url)
    # 循环翻页
    for page in range(1, 51):
        print(f'正在采集第{page}页（对应网址 {url}）的内容')
        # 下滑页面
        dp.scroll.to_bottom()
        # 监听数据包
        divs = dp.eles('css:.joblist-item')
        for div in divs:
            try:
                info = div.ele('css:.joblist-item-job').attr('sensorsdata')
                json_data = json.loads(info)
                c_name = div.ele('css:.cname').attr('title')
                c_info_list = [i.text for i in div.eles('css:.dc')]
                tags = ''.join([j.text for j in div.eles('css:.tag')])
                dit = {
                    '岗位名称': json_data['jobTitle'],
                    '招聘地区': json_data['jobArea'],
                    '要求工作经验': json_data['jobYear'],
                    '要求学历': json_data['jobDegree'],
                    '薪水': json_data['jobSalary'],
                    '发布时间': json_data['jobTime'],
                    '公司名称': c_name,
                    '公司信息': c_info_list,
                    '职位技能关键词': tags,
                }
                # 写入数据
                csv_writer.writerow(dit)
                print(dit)
            except Exception as e:
                print(e)
        # 判断是否是最后一页，如果是最后一页则不点击下一页（避免报错，因为最后一页没有下一页按钮了）
        if page < 50:
            dp.ele('css:.btn-next').click()