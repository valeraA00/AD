import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import numpy as np
import plotly.graph_objs as go

# Початкові параметри
INIT_AMPLITUDE = 1.0
INIT_FREQUENCY = 1.0
INIT_PHASE = 0.0
INIT_NOISE_MEAN = 0.0
INIT_NOISE_DISPERSION = 0.1
SHOW_NOISE = True
BASE_NOISE = np.random.normal(0, 1, 1000)

app = dash.Dash(__name__)

# Функція для генерації гармоніки з шумом
def generate_signal(amplitude, frequency, phase, noise_mean, noise_dispersion, show_noise):
    t = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        scaled_noise = noise_mean + np.sqrt(noise_dispersion) * BASE_NOISE
        y += scaled_noise
    return t, y

# Власний фільтр (наприклад, ковзне середнє)
def custom_filter(signal, window_size):
    filtered_signal = np.convolve(signal, np.ones(window_size) / window_size, mode='same')
    return filtered_signal

# Графіки
app.layout = html.Div([
    html.H1("Гармоніка з накладеним шумом"),
    dcc.Graph(id='graph1', style={'height': '300px'}),
    html.H1("Відфільтрована гармоніка"),
    dcc.Graph(id='graph2', style={'height': '300px'}),

    html.Label('Амплітуда'),
    dcc.Slider(id='amp-slider', min=0.1, max=5.0, step=0.1, value=INIT_AMPLITUDE),

    html.Label('Частота'),
    dcc.Slider(id='freq-slider', min=0.1, max=5.0, step=0.1, value=INIT_FREQUENCY),

    html.Label('Фаза'),
    dcc.Slider(id='phase-slider', min=-np.pi, max=np.pi, step=0.1, value=INIT_PHASE),

    html.Label('Шум (середнє)'),
    dcc.Slider(id='noise-mean-slider', min=-1.0, max=1.0, step=0.1, value=INIT_NOISE_MEAN),

    html.Label('Шум (дисперсія)'),
    dcc.Slider(id='noise-disp-slider', min=0.01, max=1.0, step=0.01, value=INIT_NOISE_DISPERSION),

    html.Button('Новий шум', id='new-noise-button', n_clicks=0),

    html.Label('Тип згладжування'),
    dcc.Dropdown(
        id='filter-dropdown',
        options=[
            {'label': 'Немає', 'value': 'none'},
            {'label': 'Ковзне середнє', 'value': 'moving_average'},
        ],
        value='none'
    )
])

@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure')],
    [Input('amp-slider', 'value'),
     Input('freq-slider', 'value'),
     Input('phase-slider', 'value'),
     Input('noise-mean-slider', 'value'),
     Input('noise-disp-slider', 'value'),
     Input('new-noise-button', 'n_clicks'),
     Input('filter-dropdown', 'value')]
)
def update_graphs(amplitude, frequency, phase, noise_mean, noise_dispersion, n_clicks, filter_type):
    global BASE_NOISE
    if n_clicks > 0:
        BASE_NOISE = np.random.normal(0, 1, 1000)
    
    t, y = generate_signal(amplitude, frequency, phase, noise_mean, noise_dispersion, SHOW_NOISE)

    fig1 = {
        'data': [go.Scatter(x=t, y=y, mode='lines', name='Original Signal')],
        'layout': {
            'title': 'Гармоніка з накладеним шумом',
            'xaxis': {'title': 'Час (с)'},
            'yaxis': {'title': 'Амплітуда'}
        }
    }

    if filter_type == 'moving_average':
        filtered_y = custom_filter(y, window_size=5)
    else:
        filtered_y = y
    
    fig2 = {
        'data': [go.Scatter(x=t, y=filtered_y, mode='lines', name='Filtered Signal')],
        'layout': {
            'title': 'Відфільтрована гармоніка',
            'xaxis': {'title': 'Час (с)'},
            'yaxis': {'title': 'Амплітуда'}
        }
    }

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
