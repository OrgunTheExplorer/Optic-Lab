import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

# Map wavelength (nm) to approximate RGB color
def wavelength_to_rgb(wavelength_nm):
    wavelength = float(wavelength_nm)
    if wavelength < 380 or wavelength > 780:
        return (0, 0, 0)

    if wavelength < 440:
        r, g, b = -(wavelength - 440) / (440 - 380), 0.0, 1.0
    elif wavelength < 490:
        r, g, b = 0.0, (wavelength - 440) / (490 - 440), 1.0
    elif wavelength < 510:
        r, g, b = 0.0, 1.0, -(wavelength - 510) / (510 - 490)
    elif wavelength < 580:
        r, g, b = (wavelength - 510) / (580 - 510), 1.0, 0.0
    elif wavelength < 645:
        r, g, b = 1.0, -(wavelength - 645) / (645 - 580), 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0

    # Intensity correction
    if wavelength < 420:
        factor = 0.3 + 0.7*(wavelength - 380)/(420 - 380)
    elif wavelength > 700:
        factor = 0.3 + 0.7*(780 - wavelength)/(780 - 700)
    else:
        factor = 1.0

    return (r * factor, g * factor, b * factor)

# --- Physics functions ---
def single_slit(x, λ, L, a):
    β = (np.pi * a * x) / (λ * L)
    return (np.sinc(β / np.pi))**2

def double_slit(x, λ, L, a, d):
    return single_slit(x, λ, L, a) * np.cos(np.pi * d * x / (λ * L))**2

def n_slit(x, λ, L, a, d, N):
    β = (np.pi * a * x) / (λ * L)
    δ = (np.pi * d * x) / (λ * L)
    envelope = (np.sinc(β / np.pi))**2
    interference = (np.sin(N * δ) / np.sin(δ))**2
    interference[np.isnan(interference)] = N**2  # handle division by zero
    return envelope * interference / N**2

# --- Update plot ---
def update_plot(val=None):
    slit_type = slit_mode.get()
    wavelength_nm = wavelength_slider.get()
    λ = wavelength_nm * 1e-9
    L = distance_slider.get()
    a = slit_slider.get() * 1e-6
    d = separation_slider.get() * 1e-6
    N = n_slider.get()

    x = np.linspace(-0.01, 0.01, 2000)
    if slit_type == "Single Slit":
        I = single_slit(x, λ, L, a)
    elif slit_type == "Double Slit":
        I = double_slit(x, λ, L, a, d)
    elif slit_type == "Triple Slit":
        I = n_slit(x, λ, L, a, d, 3)
    else:  # N-Slit
        I = n_slit(x, λ, L, a, d, N)

    ax.clear()
    color = wavelength_to_rgb(wavelength_nm)
    ax.plot(x * 1e3, I, color=color)
    title = f"{slit_type} Diffraction\nλ = {wavelength_nm} nm, L = {L:.2f} m, a = {int(slit_slider.get())} μm"
    if slit_type != "Single Slit":
        title += f", d = {int(separation_slider.get())} μm"
    if slit_type == "N-Slit":
        title += f", N = {N}"
    ax.set_title(title)
    ax.set_xlabel("Position on screen (mm)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.grid(True)
    ax.set_xlim(x[0] * 1e3, x[-1] * 1e3)
    ax.set_ylim(0, 1.05)
    canvas.draw()

# --- Slit type toggle handler ---
def on_mode_change(val):
    slit_type = slit_mode.get()
    if slit_type == "Single Slit":
        separation_slider.pack_forget()
        n_slider.pack_forget()
    elif slit_type == "Double Slit" or slit_type == "Triple Slit":
        separation_slider.pack(fill=tk.X, padx=10)
        n_slider.pack_forget()
    else:
        separation_slider.pack(fill=tk.X, padx=10)
        n_slider.pack(fill=tk.X, padx=10)
    update_plot()

# --- GUI ---
root = tk.Tk()
root.title("Multi-Slit Diffraction Simulator")

fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack()

slit_mode = tk.StringVar(value="Single Slit")
tk.Label(root, text="Select Slit Type:").pack()
tk.OptionMenu(root, slit_mode, "Single Slit", "Double Slit", "Triple Slit", "N-Slit", command=on_mode_change).pack()

wavelength_slider = tk.Scale(root, from_=380, to=780, resolution=1, orient=tk.HORIZONTAL, label="Wavelength (nm)", command=update_plot)
wavelength_slider.set(550)
wavelength_slider.pack(fill=tk.X, padx=10)

distance_slider = tk.Scale(root, from_=0.1, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, label="Distance to Screen (m)", command=update_plot)
distance_slider.set(1.0)
distance_slider.pack(fill=tk.X, padx=10)

slit_slider = tk.Scale(root, from_=5, to=100, resolution=1, orient=tk.HORIZONTAL, label="Slit Width (μm)", command=update_plot)
slit_slider.set(20)
slit_slider.pack(fill=tk.X, padx=10)

separation_slider = tk.Scale(root, from_=10, to=500, resolution=1, orient=tk.HORIZONTAL, label="Slit Separation (μm)", command=update_plot)

n_slider = tk.Scale(root, from_=2, to=10, resolution=1, orient=tk.HORIZONTAL, label="Number of Slits (N)", command=update_plot)

on_mode_change("Single Slit")
root.mainloop()
