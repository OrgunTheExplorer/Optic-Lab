import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

# Intensity calculation function for double slit
def double_slit_intensity(x, wavelength, L, slit_width, slit_distance):
    a = slit_width * 1e-6      # Slit width in meters
    d = slit_distance * 1e-6   # Slit separation in meters

    beta = (np.pi * a * x) / (wavelength * L)
    delta = (np.pi * d * x) / (wavelength * L)

    envelope = (np.sinc(beta / np.pi))**2
    interference = (np.cos(delta))**2

    return envelope * interference

# Update function
def update_plot(val=None):
    wavelength = wavelength_slider.get() * 1e-9  # nm to m
    L = distance_slider.get()  # m
    slit_width = slit_slider.get()  # μm
    slit_distance = separation_slider.get()  # μm

    x = np.linspace(-0.01, 0.01, 1000)  # screen position in meters
    I = double_slit_intensity(x, wavelength, L, slit_width, slit_distance)

    ax.clear()
    ax.plot(x * 1e3, I, color='green')
    ax.set_title(f"Double Slit Diffraction\nλ = {int(wavelength_slider.get())} nm, "f"L = {L:.2f} m, a = {slit_width} μm, d = {slit_distance} μm")
    ax.set_xlabel("Position on screen (mm)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.grid(True)

    ax.set_xlim(x[0] * 1e3, x[-1] * 1e3)
    ax.set_ylim(0, 1.05)

    canvas.draw()

# Tkinter GUI
root = tk.Tk()
root.title("Double Slit Diffraction Simulator")

# Matplotlib figure
fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Toolbar for zoom/pan
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack()

# Wavelength slider
wavelength_slider = tk.Scale(root, from_=380, to=700, resolution=1, orient=tk.HORIZONTAL, label="Wavelength (nm)", command=update_plot)
wavelength_slider.set(550)
wavelength_slider.pack(fill=tk.X, padx=10)

# Distance slider
distance_slider = tk.Scale(root, from_=0.1, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, label="Distance to Screen (m)", command=update_plot)
distance_slider.set(1.0)
distance_slider.pack(fill=tk.X, padx=10)

# Slit width slider
slit_slider = tk.Scale(root, from_=5, to=100, resolution=1, orient=tk.HORIZONTAL, label="Slit Width (μm)", command=update_plot)
slit_slider.set(20)
slit_slider.pack(fill=tk.X, padx=10)

# Slit separation slider
separation_slider = tk.Scale(root, from_=10, to=500, resolution=1, orient=tk.HORIZONTAL, label="Slit Separation (μm)", command=update_plot)
separation_slider.set(100)
separation_slider.pack(fill=tk.X, padx=10)

update_plot()
root.mainloop()
