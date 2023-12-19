import panel as pn
import numpy as np
import pandas as pd
import holoviews as hv
import hvplot.pandas as hvplot
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
#con esta linea iniciamos el panel
pn.extension()

# con estas funciones generamos graficos con dos parametros
# [sine] ,[cosine], [tangent], [circle], [square] [exponential]

def sine(freq, phase):
    xs = np.linspace(0, np.pi, 100)
    ys = np.sin(xs * freq + phase)
    return pd.DataFrame({"X": xs, "Y": ys})

def cosine(freq, phase):
    xs = np.linspace(0, np.pi, 100)
    ys = np.cos(xs * freq + phase)
    return pd.DataFrame({"X": xs, "Y": ys})

def tangent(freq, phase):
    xs = np.linspace(0, np.pi, 100)
    ys = np.tan(xs * freq + phase)
    return pd.DataFrame({"X": xs, "Y": ys})

def circle(freq, phase):
    theta = np.linspace(0, 2*np.pi, 100)
    x = np.cos(theta * freq + phase)
    y = np.sin(theta * freq + phase)
    return pd.DataFrame({"X": x, "Y": y})


def square(freq, phase):
    xs = np.linspace(0, 2*np.pi, 100)
    ys = np.sign(np.sin(xs * freq + phase))  # Using sign function to create a square wave
    return pd.DataFrame({"X": xs, "Y": ys})

def exponential(freq, phase):
    xs = np.linspace(0, 2*np.pi, 100)
    ys = np.exp(np.sin(xs * freq + phase))
    return pd.DataFrame({"X": xs, "Y": ys})

# de esta forma definimos los estilos que van a tener los graficos
plot_opts = dict(
    width=400,
    height=400,
    responsive=True,
    min_height=400
    
)

# de esta forma agregamos mas cosas al sidebar [menu lateral]
sidebar_footer = pn.Column(
    pn.pane.Markdown("Información adicional"),
    pn.pane.HTML('<a href="#">podermos redireccionar a otra pagina</a>')
)

# Plantilla personalizada de Fast.Desing
template = pn.template.FastGridTemplate(
    site="Dashboard",
    title="Graficos",
    sidebar=[sidebar_footer],
    header_background="red",
    header_color="white",
)

# "Widgets" para el formulario
# podemos modificarlo y agregar otros tipos de graficos por el momentos estos
frequency_input = pn.widgets.FloatInput(name="Frecuencia", value=2)
phase_input = pn.widgets.FloatInput(name="Fase", value=0)
graph_type_select = pn.widgets.RadioButtonGroup(
    name="Tipo de Gráfico",
    options=["Seno", "Coseno", "Tangente", "Círculo", "Cuadrado", "Exponencial", "Tarta"],
    value="Seno"
)
# Crear una cuadrícula para contener los gráficos
grid = pn.GridSpec(
    sizing_mode="stretch_width", max_height=800
                   
                   )


# Índices para agregar gráficos a la cuadrícula
grid_index = [0, 0]

# Función para agregar nuevos gráficos al dashboard
def add_graph(event):
    #campos del formulario
    selected_graph = graph_type_select.value
    #frecuencia
    selected_frequency = frequency_input.value
    #fase
    selected_phase = phase_input.value

    if selected_graph == "Seno":
        df = sine(selected_frequency, selected_phase)
        plot = df.hvplot(title='Sine', **plot_opts).opts(responsive=True, min_height=300)
    elif selected_graph == "Coseno":
        df = cosine(selected_frequency, selected_phase)
        plot = df.hvplot(title='Cosine', **plot_opts).opts(responsive=True, min_height=300)
    elif selected_graph == "Tangente":
        df = tangent(selected_frequency, selected_phase)
        plot = df.hvplot(title='Tangent', **plot_opts).opts(responsive=True, min_height=300)
    elif selected_graph == "Círculo":
        df = circle(selected_frequency, selected_phase)
        plot = df.hvplot(title='Circle', **plot_opts).opts(responsive=True, min_height=300)
    elif selected_graph == "Cuadrado":
        df = square(selected_frequency, selected_phase)
        plot = df.hvplot(title='Square', **plot_opts).opts(responsive=True, min_height=300)
    elif selected_graph == "Exponencial":
        df = exponential(selected_frequency, selected_phase)
        plot = df.hvplot(title='Exponential', **plot_opts).opts(responsive=True, min_height=300)
    elif selected_graph == "Tarta":
        # Gráfico de tarta con Bokeh
        x = {
            'United States': 157,
            'United Kingdom': 93,
            'Japan': 89,
            'China': 63,
            'Germany': 44,
            'India': 42,
            'Italy': 40,
            'Australia': 35,
            'Brazil': 32,
            'France': 31,
            'Taiwan': 31,
            'Spain': 29
        }
        data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = Category20c[len(x)]
        p = figure(height=350, title="Pie Chart", toolbar_location=None,
                   tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))
        r = p.wedge(x=0, y=1, radius=0.4,
                    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                    line_color="white", fill_color='color', legend_field='country', source=data)
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        plot = pn.pane.Bokeh(p, theme="dark_minimal")

    # Esta cuadricula es la que almacenara los graficos que se van a generar luego de enviar el formulario
    grid[grid_index[0], grid_index[1]] = plot
    grid_index[1] += 1
    if grid_index[1] == grid.shape[1]:
        grid_index[0] += 1
        grid_index[1] = 0

# Este es el boton que va a enviar el formulario
submit_button = pn.widgets.Button(name="Agregar Gráfico", button_type="danger") #button_type = color del boton 
submit_button.on_click(add_graph) #al hacer click envial los datos

# De esta forma diseñamos el formulario
form_layout = pn.Column(
    frequency_input,
    phase_input,
    graph_type_select,
    submit_button)

# De esta forma agregamos el formulario al sidebar 
template.sidebar.append(form_layout)
template.main[0:5, :] = grid
# Muestra la aplicación
template.servable()


































































































































@with_request
def sea_surface_handler_with_template(doc: Document, request: Any) -> None:
    sea_surface_handler(doc)
    doc.template = """
{% block title %}Embedding a Bokeh Apps In Django{% endblock %}
{% block preamble %}
<style>
.bold { font-weight: bold; }
</style>
{% endblock %}
{% block contents %}
    <div>
    This Bokeh app below is served by a <span class="bold">Django</span> server for {{ username }}:
    </div>
    {{ super() }}
{% endblock %}
    """
    doc.template_variables["username"] = request.user


def sea_surface(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "embed.html", dict(script=script))