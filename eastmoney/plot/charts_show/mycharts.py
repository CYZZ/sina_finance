from pyecharts.charts import Bar
from pyecharts import options as opts

bar = Bar()
bar.add_xaxis(['衬衫','T恤衫','裤子','羊毛衫'])
bar.add_yaxis('商家A',[5,20,30,10])
bar.add_yaxis('商家B',[100,23,43,89])
bar.set_global_opts(title_opts=opts.TitleOpts(title='某商场销售情况',subtitle='各个商家的销量'))

# bar.render_notebook()
bar.render('./yanmaoshan.html')