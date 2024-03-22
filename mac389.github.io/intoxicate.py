import pandas as pd
import numpy as np
import os

from bokeh.sampledata.iris import flowers
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components, json_item

from bokeh.io import show
from bokeh.models import CheckboxGroup, CustomJS

DATA_PATH = os.path.join('..', '_data', 'intoxicate')

df = pd.read_csv(os.path.join(DATA_PATH, 'intoxicate.patient_registry.stable.csv'))

p = figure(title = "Explore Intoxicate", 
           height=500, width=500,
           tools=["pan,reset,wheel_zoom"])

p.xaxis.axis_label = 'Risk Score'
p.yaxis.axis_label = 'No. of Patients'
p.vspan(x=[6],line_width=[2], line_color="red", line_dash="dashed")
# Histogram
bins = np.linspace(0, 60, num=20)
hist, edges = np.histogram(df['risk'], density=False, bins=bins)

LABELS = ["Option 1", "Option 2", "Option 3"]

checkbox_group = CheckboxGroup(labels=LABELS, active=[0, 1])
checkbox_group.js_on_change('active', CustomJS(code="""
    console.log('checkbox_group: active=' + this.active, this.toString())
"""))
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
         fill_color="black", line_color="white")

script, div = components(p)
checks = components(checkbox_group)

with open('../_includes/custom/intoxicate_embed_plot.html', 'w') as file:
    script, div = components(p)
    file.write(script)
    file.write('\n')
    file.write(div)
    file.write('\n')

    script, div = components(checkbox_group)
    file.write(script)
    file.write('\n')
    file.write(div)
