import panel as pn
import hvplot.pandas
import numpy as np
import pandas as pd

# Funciones para generar datos y gráficos
def sine(freq, phase):
    xs = np.linspace(0, np.pi, 100)
    ys = np.sin(xs * freq + phase)
    return pd.DataFrame({"X": xs, "Y": ys}) 

def cosine(freq, phase):
    xs = np.linspace(0, np.pi, 100)
    ys = np.cos(xs * freq + phase)
    return pd.DataFrame({"X": xs, "Y": ys})

def circle(freq, phase):
    theta = np.linspace(0, 2*np.pi, 100) 
    x = np.cos(theta * freq + phase)
    y = np.sin(theta * freq + phase)
    return pd.DataFrame({"X": x, "Y": y})
    
# Widgets para controlar los gráficos
frequency = pn.widgets.FloatSlider(name='Frequency', start=0, end=5, value=1) 
phase = pn.widgets.FloatSlider(name='Phase', start=0, end=np.pi, value=0)

# La cuadrícula para mostrar los gráficos
grid = pn.GridSpec(sizing_mode='stretch_width', max_height=500) 

# Índices para posicionar los gráficos  
grid_index = [0,0]   

# Función para agregar gráficos    
def add_graph(event):
    freq = frequency.value
    ph = phase.value
    
    if grid_index[1] < 3:
        df = sine(freq, ph)
        plot = df.hvplot().opts(width=300, height=200)
        grid[grid_index[0], grid_index[1]] = plot
    elif grid_index[1] < 6: 
        df = cosine(freq, ph)
        plot = df.hvplot().opts(height=250)
        grid[grid_index[0], grid_index[1]] = plot 
    else:
        df = circle(freq, ph)
        plot = df.hvplot().opts(height=200) 
        grid[grid_index[0], grid_index[1]] = plot
        
    grid_index[1] += 1
    if grid_index[1] >= grid.shape[1]:
        grid_index[0] += 1
        grid_index[1] = 0
        
button = pn.widgets.Button(name='Add Graph')        
button.on_click(add_graph)

# Template  
template = pn.template.MaterialTemplate(title='Graphs')

# Envuelvo grid en una lista  
template.main[:] = [grid] 

template.sidebar[:] = [frequency, phase, button]

template.servable()







































import panel as pn
import numpy as np
import pandas as pd
import holoviews as hv
import hvplot.pandas as hvplot
from math import pi

# Configuración para cargar FontAwesome
pn.config.sizing_mode = "stretch_width"
pn.extension(raw_css=[f'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'])

def panelLog():
    def sine(freq, phase):
        xs = np.linspace(0, np.pi, 100)
        ys = np.sin(xs * freq + phase)
        return pd.DataFrame({"X": xs, "Y": ys})

    plot_opts = dict(
        width=400,
        height=400,
        responsive=True,
        min_height=300
    )

    template = pn.template.FastGridTemplate(
        site="Dashboard",
        title="Graficos",
        header_background="red",
        header_color="white",
    )

    frequency_input = pn.widgets.FloatInput(name="Frecuencia", value=2)
    phase_input = pn.widgets.FloatInput(name="Fase", value=0)
    dial_value_input = pn.widgets.FloatInput(name="Valor del Dial", value=50)
    dial_lower_bound_input = pn.widgets.FloatInput(name="Límite Inferior del Dial", value=0)
    dial_upper_bound_input = pn.widgets.FloatInput(name="Límite Superior del Dial", value=100)

    graph_type_select = pn.widgets.RadioButtonGroup(
        name="Tipo de Gráfico",
        options=["\uf201", "\uf080", "\uf303", "\uf200"],  # Unicode para iconos de FontAwesome
        value="\uf201"
    )

    dial = pn.indicators.Dial(
        name='Engine', value=dial_value_input.value, format='{value} %',
        colors=[(0.2, 'green'), (0.8, 'gold'), (1, 'red')],
        sizing_mode="stretch_width"
    )

    graph_column1 = pn.Column()
    graph_column2 = pn.Row()

    graph_column = graph_column1 + graph_column2

    def add_graph(event):
        selected_icon = graph_type_select.value
        selected_frequency = frequency_input.value
        selected_phase = phase_input.value

        plot = None  # Definir plot con un valor por defecto

        if selected_icon == "\uf201":
            df = sine(selected_frequency, selected_phase)
            plot = df.hvplot(title='Sine', **plot_opts).opts(responsive=True, min_height=300)
        # Resto de las condiciones

        if plot is not None:
            graph_column.append(plot)
            graph_column.append(pn.layout.HSpacer())

    def update_dial(event):
        dial.value = dial_value_input.value
        dial.bounds = (dial_lower_bound_input.value, dial_upper_bound_input.value)

    submit_button = pn.widgets.Button(name="Agregar Gráfico", button_type="danger")
    submit_button.on_click(add_graph)

    update_dial_button = pn.widgets.Button(name="Actualizar Dial", button_type="primary")
    update_dial_button.on_click(update_dial)

    # Utilizar Unicode directamente para representar iconos de gráficos de FontAwesome
    button_group = pn.Row(
        pn.pane.HTML('<i class="fa-solid fa-2x">&#x42;</i>', width=30, height=30, style={"font-size": "24px"}),
        graph_type_select,
        submit_button
    )

    form_layout = pn.Column(
        frequency_input,
        phase_input,
        button_group,
    )

    dial_form_layout = pn.Column(
        pn.pane.HTML('<i class="fas fa-tachometer-alt"></i> Engine Speed', width=30, height=30),
        dial_value_input,
        dial_lower_bound_input,
        dial_upper_bound_input,
        update_dial_button,
        sizing_mode="stretch_width"
    )

    template.main[0:2, 0:3] = dial
    template.sidebar.append(form_layout)
    template.sidebar.append(dial_form_layout)
    template.main[0:6, 6:12] = graph_column  # Ajusta la posición según tus necesidades

    template.servable()

panelLog()
