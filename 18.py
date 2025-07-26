# 导入数据处理模块
import pandas as pd
# 导入配置项
from pyecharts import options as opts
# 导入图形
from pyecharts.charts import Pie, Bar, Line

# 读取ddd.csv文件
try:
    df = pd.read_csv('ddd.csv')
    print("ddd.csv文件读取成功！")
except FileNotFoundError:
    print("ddd.csv文件不存在，请检查文件路径是否正确！")
except pd.errors.ParserError:
    print("ddd.csv文件格式可能有问题，无法正确解析，请检查文件内容格式。")

if 'df' in locals():
    # 获取ddd.csv文件数据的招聘地区分布情况数据（饼图）
    x_area = df['招聘地区'].value_counts().index.to_list()
    y_area = df['招聘地区'].value_counts().to_list()

    pie_chart = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(x_area, y_area)],
            center=["40%", "50%"],
        )
        .set_global_opts(
            # 设置可视化标题
            title_opts=opts.TitleOpts(title="招聘地区分布情况（ddd.csv数据）"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # 导出可视化效果: 保存html文件
        .render("pie_招聘地区分布情况_ddd.html")
    )

    # 获取ddd.csv文件数据的要求工作经验分布情况数据（柱状图）
    x_work_exp = df['要求工作经验'].value_counts().index.to_list()
    y_work_exp = df['要求工作经验'].value_counts().to_list()

    bar_chart = (
        Bar()
        .add_xaxis(x_work_exp)
        .add_yaxis("要求工作经验", y_work_exp, stack="stack1")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-要求工作经验分布情况（ddd.csv数据）"))
        .render("bar_要求工作经验分布情况_ddd.html")
    )

    # 获取ddd.csv文件数据的要求学历分布情况数据（折线图）
    x_edu = df['要求学历'].value_counts().index.to_list()
    y_edu = df['要求学历'].value_counts().to_list()

    line_chart = (
        Line()
        .add_xaxis(x_edu)
        .add_yaxis("要求学历", y_edu, is_connect_nones=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-要求学历分布（ddd.csv数据）"))
        .render("line_要求学历分布_ddd.html")
    )
