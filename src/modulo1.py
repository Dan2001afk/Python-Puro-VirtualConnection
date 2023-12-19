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
        header_background="green",
        header_color="white",
    )

    frequency_input = pn.widgets.FloatInput(name="Frecuencia", value=2)
    phase_input = pn.widgets.FloatInput(name="Fase", value=0)
    dial_value_input = pn.widgets.FloatInput(name="Valor del Dial", value=50)
    dial_lower_bound_input = pn.widgets.FloatInput(name="Límite Inferior del Dial", value=0)
    dial_upper_bound_input = pn.widgets.FloatInput(name="Límite Superior del Dial", value=100)

    graph_type_select = pn.widgets.RadioButtonGroup(
        name="Tipo de Gráfico",
        options=["\uf201"],  # Unicode para iconos de FontAwesome
        value="\uf201"
    )

    dial = pn.indicators.Dial(
        name='Engine', value=dial_value_input.value, format='{value} %',
        colors=[(0.2, 'green'), (0.8, 'gold'), (1, 'red')],
        sizing_mode="stretch_width"
    )

   

    graph_column = pn.Column()

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
