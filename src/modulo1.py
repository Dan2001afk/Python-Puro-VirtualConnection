import panel as pn
import numpy as np
import pandas as pd
import holoviews as hv
import hvplot.pandas as hvplot
from math import pi
import json
from jinja2 import Template

# Configuración para cargar FontAwesome
pn.config.sizing_mode = "stretch_width"
pn.extension(raw_css=[f'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'])

def panelLog():
    
    
    #carga de datos mediante archivo json
    
    # def load_parameters(file_path):
    #     with open(file_path, 'r') as file:
    #         parameters = json.load(file)
    #     return parameters

    # parameters = load_parameters('parametros.json')
     
    #configuracion de la grafica linear
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

    
    #modal1 graficas sine 
    frequency_input = pn.widgets.FloatInput(name="Frecuencia", value=2)
    phase_input = pn.widgets.FloatInput(name="Fase", value=0)
    submit_button = pn.widgets.Button(name="Agregar Gráfico", button_type="danger")
    
    template.modal.extend([frequency_input, phase_input,submit_button])

    modal_btn = pn.widgets.Button(name="Graficas seno con 2 parametros")
    
    def Modal1_callback(event):
        template.open_modal()
        
    modal_btn.on_click(Modal1_callback)
    template.sidebar.append(modal_btn)
    
    
    # modal2 graficas dial
    dial_value_input = pn.widgets.FloatInput(name="Valor del Dial", value=50)
    dial_lower_bound_input = pn.widgets.FloatInput(name="Límite Inferior del Dial", value=0)
    dial_upper_bound_input = pn.widgets.FloatInput(name="Límite Superior del Dial", value=100)
    update_dial_button = pn.widgets.Button(name="Actualizar Dial", button_type="primary")
    template.modal.extend([dial_value_input, dial_lower_bound_input,dial_upper_bound_input,update_dial_button])
    
    modal_btn2 = pn.widgets.Button(name="Graficas dial con 3 parametros")
    
    def Modal2_callback(event):
        template.open_modal()
        
    modal_btn2.on_click(Modal2_callback)
    template.sidebar.append(modal_btn2)
    
    #modal3 grafica linear 
    linear_gauge_value_input = pn.widgets.FloatInput(name="Valor del Linear Gauge", value=30)
    linear_gauge_lower_bound_input = pn.widgets.FloatInput(name="Límite Inferior del Linear Gauge", value=0)
    linear_gauge_upper_bound_input = pn.widgets.FloatInput(name="Límite Superior del Linear Gauge", value=100)
    update_linear_gauge_button = pn.widgets.Button(name="Actualizar Linear Gauge", button_type="primary")
    template.modal.extend([linear_gauge_value_input,linear_gauge_lower_bound_input,linear_gauge_upper_bound_input,update_linear_gauge_button])
    
    modal_btn3 = pn.widgets.Button(name="Graficas linear con 3 parametros")
    
    def Modal3_callback(event):
        template.open_modal()
        
    modal_btn3.on_click(Modal3_callback)
    template.sidebar.append(modal_btn3)


    linear_gauge_form_template = Template("""
<div>
    <i class="fas fa-tachometer-alt"></i>
    <input type="number" name="linear_gauge_value" step="0.1" value="{{ value }}" placeholder="Valor del Linear Gauge">
    <input type="number" name="linear_gauge_lower_bound" step="0.1" value="{{ lower_bound }}" placeholder="Límite Inferior del Linear Gauge">
    <input type="number" name="linear_gauge_upper_bound" step="0.1" value="{{ upper_bound }}" placeholder="Límite Superior del Linear Gauge">
    <button type="button" onclick="updateLinearGauge()">Actualizar Linear Gauge</button>
</div>
<script>
    function updateLinearGauge() {
        var value = parseFloat(document.getElementsByName("linear_gauge_value")[0].value);
        var lower_bound = parseFloat(document.getElementsByName("linear_gauge_lower_bound")[0].value);
        var upper_bound = parseFloat(document.getElementsByName("linear_gauge_upper_bound")[0].value);
        updateLinearGaugeCallback(value, lower_bound, upper_bound);
    }
</script>
""")
   
   
    
    graph_type_select = pn.widgets.RadioButtonGroup(
        name="Tipo de Gráfico",
        options=["\uf201"],  # Unicode para iconos de FontAwesome
        value="\uf201"
    )
    #configuracion de la grafica dial
    dial = pn.indicators.Dial(
        name='Temperatura', value=dial_value_input.value, format='{value} %',
        colors=[(0.2, 'green'), (0.8, 'gold'), (1, 'red')],
        sizing_mode="stretch_width"
    )

    
    #configuracion de la grafica linear
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
            plot = df.hvplot(title='Sine', **plot_opts).opts(responsive=True, min_height=300)
        

        if plot is not None:
            graph_column.append(plot)
            graph_column.append(pn.layout.HSpacer())

    def update_dial(event):
        dial.value = dial_value_input.value
        dial.bounds = (dial_lower_bound_input.value, dial_upper_bound_input.value)

    def update_linear_gauge(event):
        linear_gauge.value = linear_gauge_value_input.value
        linear_gauge.bounds = (linear_gauge_lower_bound_input.value, linear_gauge_upper_bound_input.value)

    
    submit_button.on_click(add_graph)

    
    update_dial_button.on_click(update_dial)

    
    update_linear_gauge_button.on_click(update_linear_gauge)

    # Utilizar Unicode directamente para representar iconos de gráficos de FontAwesome
    button_group = pn.Row(
        pn.pane.HTML('<i class="fa-solid fa-2x">&#x42;</i>', width=30, height=30, styles={"font-size": "24px"}),
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
        sizing_mode="stretch_width"
    )

    linear_gauge_form_layout = pn.Column(
        pn.pane.HTML('<i class="fas fa-tachometer-alt"></i>', width=30, height=30),
        linear_gauge_value_input,
        linear_gauge_lower_bound_input,
        linear_gauge_upper_bound_input,
        update_linear_gauge_button,
        sizing_mode="stretch_width"
    )

    template.main[0:2, 0:3] = dial
    template.main[2:5, 0:3] = linear_gauge
    template.main[0:6, 6:12] = graph_column  

    template.servable()

panelLog()
