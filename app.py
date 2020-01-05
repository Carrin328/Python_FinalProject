#! usr/bin/python
# -*- coding: utf-8 -*-
'''
@user: sean
@project_name:final
@file_name:app 
@date:2020/1/5
'''


import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType,ThemeType
from pyecharts.charts import Pie, Timeline, Funnel, Map
from loguru import logger

app = Flask(__name__)

regions_available = [
                    "人均消费",
                    "抚养比",
                    "人口自然增长率",
                    "人口自然增长率和人均消费、抚养比的对比"]

@app.route('/', methods=['GET'])
def home_page():
    return render_template('results1.html',
                           the_select_region=regions_available)


@app.route('/subpage', methods=['POST'])
def run_select():
    the_region = request.form["the_region_selected"]
    logger.debug(the_region)  # 检查用户输入
    if the_region == regions_available[0]:
        df = pd.read_csv('人均消费.csv', encoding='utf8', index_col=0)
        data_str = df.to_html()
        tl = Timeline()
        for i in range(2011, 2019):
            pie = (
                Pie()
                    .add(
                    "数值",
                    list(zip(list(df.index), list(df["{}年".format(i)]))),
                    rosetype="radius",
                    radius=["30%", "55%"],
                )
                # .set_global_opts(title_opts=opts.TitleOpts("人均消费".format(i)))
            )
            tl.add(pie, "{}年".format(i))
        return render_template('results2.html',
                               the_plot_all=tl.render_embed(),
                               the_res=data_str,
                               the_select_region=regions_available)

    elif the_region == regions_available[1]:
        df = pd.read_csv('fuyang.csv', encoding='utf8', index_col=0)
        data_str = df.to_html()
        tl = Timeline()
        for i in range(2011, 2019):
            pie = (
                Pie()
                    .add(
                    "数值",
                    list(zip(list(df.index), list(df["{}年".format(i)]))),
                    rosetype="radius",
                    radius=["30%", "55%"],
                )
            )
            tl.add(pie, "{}年".format(i))
        return render_template('results2.html',
                               the_plot_all=tl.render_embed(),
                               the_res=data_str,
                               the_select_region=regions_available)

    elif the_region == regions_available[2]:
        df1 = pd.read_csv('growth.csv', encoding='utf8', index_col=0)
        data_str = df1.to_html()
        tl = Timeline()
        for i in range(2011, 2019):
            c = (
                Funnel()
                    .add("人口自然增长率", list(zip(list(df1.index), list(df1["{}年".format(i)]))), label_opts=opts.LabelOpts(position='inside'))
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="{}人口自然增长率".format(i), subtitle="",
                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=18,
                                                                                         font_style="italic")),
                    visualmap_opts=opts.VisualMapOpts(min_=1, max_=15)
                )
            )
            tl.add(c, "{}年".format(i))
        return render_template('results2.html',
                               the_plot_all=tl.render_embed(),
                               the_res=data_str,
                               the_select_region=regions_available)

    elif the_region == regions_available[3]:
        df = pd.read_csv('人均消费.csv', encoding='utf8', index_col=0)
        df1 = pd.read_csv('growth.csv', encoding='utf8', index_col=0)
        df2 = pd.read_csv('fuyang.csv', encoding='utf8', index_col=0)
        tl1 = Timeline()
        for i in range(2011, 2019):
            map0 = (
                Map()
                    .add(
                    "人口自然增长率", list(zip(list(df1.index), list(df1["{}年".format(i)]))), "china", is_map_symbol_show=False
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="{}人口自然增长率".format(i), subtitle="",
                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=18,
                                                                                         font_style="italic")),
                    visualmap_opts=opts.VisualMapOpts(min_=-1, max_=11.5),

                )
            )
            tl1.add(map0, "{}年".format(i))

        tl2 = Timeline()
        for i in range(2011, 2019):
            map0 = (
                Map()
                    .add(
                    "人均消费水平", list(zip(list(df.index), list(df["{}年".format(i)]))), "china", is_map_symbol_show=False
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="{}人均消费".format(i), subtitle="",
                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=18,
                                                                                         font_style="italic")),
                    visualmap_opts=opts.VisualMapOpts(min_=5000, max_=50000),

                )
            )
            tl2.add(map0, "{}年".format(i))

        tl3 = Timeline()
        for i in range(2011, 2019):
            map0 = (
                Map()
                    .add(
                    "抚养比", list(zip(list(df2.index), list(df2["{}年".format(i)]))), "china", is_map_symbol_show=False
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="{}抚养比".format(i), subtitle="",
                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=18,
                                                                                         font_style="italic")),
                    visualmap_opts=opts.VisualMapOpts(min_=21, max_=50),

                )
            )
            tl3.add(map0, "{}年".format(i))
        return render_template('results3.html',
                                the_plot1=tl1.render_embed(),
                                the_plot2=tl2.render_embed(),
                                the_plot3=tl3.render_embed(),
                                the_select_region=regions_available)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)