import numpy as np
from scipy import sparse
from scipy.spatial import cKDTree
from bokeh import models, plotting, io
from bokeh.models import LinearColorMapper, Slider, Div, Button
from bokeh.layouts import row, column
from time import sleep
from itertools import cycle

import gas

color_mapper = LinearColorMapper(palette="Turbo256", low = -np.pi, high = np.pi)

system = gas.System(N=100,L=50.0, T=1.0)
dt = 1.0
edges=np.linspace(0,5,32)

def animate():
    for k in range(1):
        system.evolve(dt)
    r = system.r
    speed = np.linalg.norm(system.v,axis=1)
    histo = np.histogram(speed, bins=edges,density=True)
    return r[:,0],r[:,1],speed,histo


# setting the data
x, y, speed, histo = animate()
data = {'x': x, 'y': y,'speed':speed, #for gas plot
}
hist={'hist':histo[0],'left':histo[1][:-1],'right':histo[1][1:]}
data_source = models.ColumnDataSource(data)
histo_source = models.ColumnDataSource(hist)

p = plotting.figure(
    title="Kinetic Gas",
    tools=["save", "reset", "box_zoom"],
    plot_width=500, plot_height=500,
    x_range=(0, system.L),
    y_range=(0, system.L)

)
# p.title.text_font = '32px'
p.toolbar.logo = None
p.scatter(x="x", y="y",
          source=data_source,
          marker="circle",
          color={'field': 'speed', 'transform': color_mapper},
          # line_color={'field': 'angle', 'transform': color_mapper},
          # line_alpha="color",
          size=8,
          width=4.0,
          syncable=False
)

distribution = plotting.figure(
    plot_width=400, plot_height=400,
    x_axis_label="|v|",
    y_axis_label="pdf",
    y_range=(0, 1),
    # x_range=(0, L),
    # y_range=(0, L)
)
distribution.toolbar_location = None
distribution.quad(top='hist', bottom=0,
        left='left', right='right',
         fill_color="skyblue", line_color="white",source=histo_source)
theory_x, theory_y = system.theory()
distribution.line(x=theory_x, y=theory_y)
def stream():
    x, y, speed, histo = animate()
    data = {'x': x, 'y': y,'speed':speed, #for gas plot
    }
    hist={'hist':histo[0],'left':histo[1][:-1],'right':histo[1][1:]}
    data_source.data = data
    histo_source.data = hist

# density_slider.on_change('value', reset)
# noise_slider.on_change('value', update_noise)
# speed_slider.on_change('value', update_speed)

callback_id = None
def run():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = io.curdoc().add_periodic_callback(stream, 100)
    else:
        button.label = '► Play'
        io.curdoc().remove_periodic_callback(callback_id)

button = Button(label='► Play', width=60)
button.on_event('button_click', run)

controls = column(button,distribution, Div(
    text='by <a href="https://francescoturci.net" target="_blank">Francesco Turci </a> '))

io.curdoc().add_root(row(p, controls))
io.curdoc().title = "Kinetic Gas"
