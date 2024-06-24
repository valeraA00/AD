import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons, RadioButtons
from scipy import signal

# Початкові значення параметрів
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.5
initial_noise_mean = 0.0
initial_noise_variance = 0.1
initial_sigma = 2
t = np.linspace(0, 10, 1000)
noise_array = np.random.normal(initial_noise_mean, initial_noise_variance, size=1000)

# Функція для генерації гармоніки з шумом
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_variance, show_noise):
    clean_harmonic = amplitude * np.sin(frequency * t + phase)
    if show_noise:
        return clean_harmonic + noise_array
    else:
        return clean_harmonic

# Функція для фільтрації сигналу
def filter_signal(signal_data, filter_type, sigma, window_size):
    if filter_type == 'gaussian':
        window = signal.windows.gaussian(window_size, sigma)
        filtered_signal = signal.convolve(signal_data, window / window.sum(), mode='same')
    elif filter_type == 'uniform':
        window = np.ones(window_size) / window_size
        filtered_signal = np.convolve(signal_data, window, mode='same')
    else:
        filtered_signal = signal_data
    return filtered_signal

# Функція для оновлення графіків
def update(val):
    amplitude = amplitude_slider.val
    frequency = frequency_slider.val
    phase = phase_slider.val
    show_noise = noise_checkbox.get_status()[0]
    sigma = sigma_slider.val
    window_size = window_size_slider.val
    filter_type = smoothing_buttons.value_selected

    y_data = harmonic_with_noise(amplitude, frequency, phase, noise_mean_slider.val, noise_variance_slider.val, show_noise)
    line_original.set_ydata(y_data)
    line_filtered.set_ydata(filter_signal(y_data, filter_type, sigma, window_size))
    fig.canvas.draw_idle()

# Функція для оновлення шуму
def update_noise(val):
    global noise_array
    noise_array = np.random.normal(noise_mean_slider.val, noise_variance_slider.val, size=1000)
    update(None)

# Функція для скидання параметрів
def reset(event):
    amplitude_slider.reset()
    frequency_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_variance_slider.reset()
    sigma_slider.reset()
    window_size_slider.reset()
    noise_checkbox.set_active(0)
    smoothing_buttons.set_active(0)

# Створення фігури та осей для двох графіків
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plt.subplots_adjust(left=0.2, bottom=0.4, right=0.75, top=0.9, hspace=0.4)

# Початковий графік чистої гармоніки
y_data = harmonic_with_noise(initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_variance, True)
line_original, = ax1.plot(t, y_data, color='navy')
ax1.set_title('Гармонічний сигнал з шумом')
ax1.set_xlabel('Час')
ax1.set_ylabel('Амплітуда')
ax1.grid(True)

# Початковий графік фільтрованої гармоніки
filtered_data = filter_signal(y_data, 'gaussian', initial_sigma, 50)
line_filtered, = ax2.plot(t, filtered_data, color='darkred')
ax2.set_title('Фільтрований гармонічний сигнал')
ax2.set_xlabel('Час')
ax2.set_ylabel('Амплітуда')
ax2.grid(True)

# Створення слайдерів
slider_color = 'lightblue'

amplitude_ax = plt.axes([0.2, 0.30, 0.55, 0.03], facecolor=slider_color)
amplitude_slider = Slider(amplitude_ax, 'Амплітуда', 0.1, 10.0, valinit=initial_amplitude)
amplitude_slider.on_changed(update)

frequency_ax = plt.axes([0.2, 0.25, 0.55, 0.03], facecolor=slider_color)
frequency_slider = Slider(frequency_ax, 'Частота', 0.1, 10.0, valinit=initial_frequency)
frequency_slider.on_changed(update)

phase_ax = plt.axes([0.2, 0.20, 0.55, 0.03], facecolor=slider_color)
phase_slider = Slider(phase_ax, 'Фаза', 0, 2*np.pi, valinit=initial_phase)
phase_slider.on_changed(update)

noise_mean_ax = plt.axes([0.2, 0.15, 0.55, 0.03], facecolor=slider_color)
noise_mean_slider = Slider(noise_mean_ax, 'Середнє шуму', -1.0, 1.0, valinit=initial_noise_mean)
noise_mean_slider.on_changed(update_noise)

noise_variance_ax = plt.axes([0.2, 0.10, 0.55, 0.03], facecolor=slider_color)
noise_variance_slider = Slider(noise_variance_ax, 'Дисперсія шуму', 0.0, 1.0, valinit=initial_noise_variance)
noise_variance_slider.on_changed(update_noise)

sigma_ax = plt.axes([0.2, 0.05, 0.55, 0.03], facecolor=slider_color)
sigma_slider = Slider(sigma_ax, 'Сігма', 0, 10, valinit=initial_sigma)
sigma_slider.on_changed(update)

window_size_ax = plt.axes([0.2, 0.00, 0.55, 0.03], facecolor=slider_color)
window_size_slider = Slider(window_size_ax, 'Розмір вікна', 3, 101, valinit=50, valstep=2)
window_size_slider.on_changed(update)

# Створення чекбоксу для відображення шуму
checkbox_ax = plt.axes([0.82, 0.6, 0.14, 0.1])
noise_checkbox = CheckButtons(checkbox_ax, ['Показати шум'], [True])
noise_checkbox.on_clicked(update)

# Створення кнопки для скидання параметрів
reset_ax = plt.axes([0.82, 0.55, 0.14, 0.04])
reset_button = Button(reset_ax, 'Скинути', color='lightcoral')
reset_button.on_clicked(reset)

# Створення кнопок для вибору типу згладжування
smoothing_ax = plt.axes([0.82, 0.40, 0.14, 0.1], facecolor='lightgoldenrodyellow')
smoothing_buttons = RadioButtons(smoothing_ax, ['none', 'gaussian', 'uniform'], active=0)
smoothing_buttons.on_clicked(update)

plt.show()
