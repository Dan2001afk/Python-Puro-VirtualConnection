import panel as pn
import json
import numpy as np
import pandas as pd
import jinja2

# Configuración para cargar FontAwesome
pn.config.sizing_mode = "stretch_width"
pn.extension(raw_css=[f'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'])

def sine(freq, phase):
    xs = np.linspace(0, np.pi, 100)
    ys = np.sin(xs * freq + phase)
    return pd.DataFrame({"X": xs, "Y": ys})

def create_modal_form(title, widgets, button_callback):
    template = """
    <div>
        <h3>{{ title }}</h3>
        {% for widget in widgets %}
            {{ widget }}
        {% endfor %}
        <button onclick="{{ button_callback }}">Actualizar</button>
    </div>
    """
    return jinja2.Template(template).render(title=title, widgets=widgets, button_callback=button_callback)

def open_modal_callback(modal, widgets, button_callback):
    modal.content = create_modal_form(modal.title, widgets, button_callback)
    modal.param.trigger('content')
    modal.param.trigger('visible')

def panelLog():
    # Cargar datos desde archivos JSON
    with open("js/linear_gauge_data.json", "r") as linear_gauge_file:
        linear_gauge_data = json.load(linear_gauge_file)

    with open("js/dial_data.json", "r") as dial_file:
        dial_data = json.load(dial_file)

    template = pn.template.FastGridTemplate(
        site="Dashboard",
        title="Graficos",
        header_background="green",
        header_color="white",
    )

    frequency_input = pn.widgets.FloatInput(name="Frecuencia", value=2)
    phase_input = pn.widgets.FloatInput(name="Fase", value=0)
    
    # Crear widgets de selección para Linear Gauge y Dial
    linear_gauge_config_select = pn.widgets.Select(name="Configuración Linear Gauge", options=[config["name"] for config in linear_gauge_data])
    dial_config_select = pn.widgets.Select(name="Configuración Dial", options=[config["name"] for config in dial_data])

    dial_value_input = pn.widgets.FloatInput(name="Valor del Dial", value=50)
    dial_lower_bound_input = pn.widgets.FloatInput(name="Límite Inferior del Dial", value=0)
    dial_upper_bound_input = pn.widgets.FloatInput(name="Límite Superior del Dial", value=100)

    linear_gauge_value_input = pn.widgets.FloatInput(name="Valor del Linear Gauge", value=30)
    linear_gauge_lower_bound_input = pn.widgets.FloatInput(name="Límite Inferior del Linear Gauge", value=0)
    linear_gauge_upper_bound_input = pn.widgets.FloatInput(name="Límite Superior del Linear Gauge", value=100)

    graph_type_select = pn.widgets.RadioButtonGroup(
        name="Tipo de Gráfico",
        options=["\uf201"],  # Unicode para iconos de FontAwesome
        value="\uf201"
    )

    dial = pn.indicators.Dial(
        name='Temperatura', value=dial_value_input.value, format='{value} %',
        colors=[(0.2, 'green'), (0.8, 'gold'), (1, 'red')],
        sizing_mode="stretch_width"
    )

    linear_gauge = pn.indicators.LinearGauge(
        name='Temperatura', value=linear_gauge_value_input.value, bounds=(linear_gauge_lower_bound_input.value, linear_gauge_upper_bound_input.value),
        format='{value:.0f} %',
        colors=[(0.2, 'green'), (0.8, 'gold'), (1, 'red')], show_boundaries=True,
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
            plot = df.hvplot(title='Sine', width=400, height=400, responsive=True, min_height=300)
        # Resto de las condiciones

        if plot is not None:
            graph_column.append(plot)
            graph_column.append(pn.layout.HSpacer())

    def update_dial(event):
        dial.value = dial_value_input.value
        dial.bounds = (dial_lower_bound_input.value, dial_upper_bound_input.value)

    def update_linear_gauge(event):
        linear_gauge.value = linear_gauge_value_input.value
        linear_gauge.bounds = (linear_gauge_lower_bound_input.value, linear_gauge_upper_bound_input.value)

    def open_dial_modal(event):
        open_modal_callback(dial_modal,
                            [dial_value_input, dial_lower_bound_input, dial_upper_bound_input],
                            update_dial)

    def open_linear_gauge_modal(event):
        open_modal_callback(linear_gauge_modal,
                            [linear_gauge_value_input, linear_gauge_lower_bound_input, linear_gauge_upper_bound_input],
                            update_linear_gauge)

    def update_dial_button_callback(event):
        update_dial(event)

    def update_linear_gauge_button_callback(event):
        update_linear_gauge(event)

    submit_button = pn.widgets.Button(name="Agregar Gráfico", button_type="danger")
    submit_button.on_click(add_graph)

    # Botones para abrir modales
    open_dial_modal_button = pn.widgets.Button(name="Abrir Dial", button_type="primary")
    open_dial_modal_button.on_click(open_dial_modal)

    open_linear_gauge_modal_button = pn.widgets.Button(name="Abrir Linear Gauge", button_type="primary")
    open_linear_gauge_modal_button.on_click(open_linear_gauge_modal)

    # Botones de actualización
    update_dial_button = pn.widgets.Button(name="Actualizar Dial", button_type="primary")
    update_dial_button.on_click(update_dial_button_callback)

    update_linear_gauge_button = pn.widgets.Button(name="Actualizar Linear Gauge", button_type="primary")
    update_linear_gauge_button.on_click(update_linear_gauge_button_callback)

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
        pn.pane.HTML('<i class="fas fa-tachometer-alt"></i>', width=30, height=30),
        dial_value_input,
        dial_lower_bound_input,
        dial_upper_bound_input,
        update_dial_button,
        open_dial_modal_button,
        sizing_mode="stretch_width"
    )

    linear_gauge_form_layout = pn.Column(
        pn.pane.HTML('<i class="fas fa-tachometer-alt"></i>', width=30, height=30),
        linear_gauge_value_input,
        linear_gauge_lower_bound_input,
        linear_gauge_upper_bound_input,
        update_linear_gauge_button,
        open_linear_gauge_modal_button,
        sizing_mode="stretch_width"
    )

    dial_modal = pn.widgets.Dialog(
        content="",
        buttons=[],
        sizing_mode="stretch_width"
    )

    linear_gauge_modal = pn.widgets.Dialog(
        content="",
        buttons=[],
        sizing_mode="stretch_width"
    )

    template.main[0:2, 0:3] = dial
    template.main[2:5, 0:3] = linear_gauge
    template.sidebar.append(form_layout)
    template.sidebar.append(dial_form_layout)
    template.sidebar.append(linear_gauge_form_layout)
    template.main[0:6, 6:12] = graph_column

    template.servable()

panelLog()
