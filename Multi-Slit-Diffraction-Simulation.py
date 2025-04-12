import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

# --- Color mapping for wavelengths ---
def wavelength_to_rgb(wavelength_nm):
    w = wavelength_nm
    if w < 380 or w > 780: return (0, 0, 0)
    if w < 440: r, g, b = -(w - 440) / 60, 0.0, 1.0
    elif w < 490: r, g, b = 0.0, (w - 440) / 50, 1.0
    elif w < 510: r, g, b = 0.0, 1.0, -(w - 510) / 20
    elif w < 580: r, g, b = (w - 510) / 70, 1.0, 0.0
    elif w < 645: r, g, b = 1.0, -(w - 645) / 65, 0.0
    else: r, g, b = 1.0, 0.0, 0.0
    factor = 1 if 420 <= w <= 700 else 0.3
    return tuple(min(max(i * factor, 0), 1) for i in (r, g, b))

# --- Physics ---
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
    interference[np.isnan(interference)] = N**2
    return envelope * interference / N**2

# --- UI logic ---
def update_plot(_=None):
    slit_type = slit_mode.get()
    λ = wavelength_slider.get() * 1e-9
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
    else:
        I = n_slit(x, λ, L, a, d, N)

    ax.clear()
    color = wavelength_to_rgb(wavelength_slider.get())
    ax.plot(x * 1e3, I, color=color, lw=2)
    ax.set_xlim(x[0] * 1e3, x[-1] * 1e3)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Position (mm)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_title(f"{slit_type} Diffraction", fontsize=14)
    ax.grid(True)
    canvas.draw()

def toggle_sliders(*_):
    st = slit_mode.get()
    if st == "Single Slit":
        separation_slider_frame.pack_forget()
        n_slider_frame.pack_forget()
    elif st in ("Double Slit", "Triple Slit"):
        separation_slider_frame.pack(fill='x', padx=5, pady=2)
        n_slider_frame.pack_forget()
    else:
        separation_slider_frame.pack(fill='x', padx=5, pady=2)
        n_slider_frame.pack(fill='x', padx=5, pady=2)
    update_plot()

# --- App Init ---
root = tk.Tk()
root.title("Diffraction Simulator")
root.geometry("800x700")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")

# --- Plot ---
fig, ax = plt.subplots(figsize=(6, 3.5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

# Toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack()

# --- Controls Frame ---
controls = ttk.Frame(root, padding=10)
controls.pack(fill='x')

# Slit Type
slit_mode = tk.StringVar(value="Single Slit")
ttk.Label(controls, text="Slit Type:").pack(anchor='w')
slit_menu = ttk.Combobox(controls, textvariable=slit_mode, values=["Single Slit", "Double Slit", "Triple Slit", "N-Slit"])
slit_menu.pack(fill='x')
slit_menu.bind("<<ComboboxSelected>>", toggle_sliders)

# Wavelength
wavelength_slider = tk.Scale(controls, from_=380, to=780, label="Wavelength (nm)", orient=tk.HORIZONTAL, resolution=1, command=update_plot)
wavelength_slider.set(550)
wavelength_slider.pack(fill='x', pady=2)

# Distance
distance_slider = tk.Scale(controls, from_=0.1, to=2.0, label="Screen Distance (m)", orient=tk.HORIZONTAL, resolution=0.01, command=update_plot)
distance_slider.set(1.0)
distance_slider.pack(fill='x', pady=2)

# Slit Width
slit_slider = tk.Scale(controls, from_=5, to=100, label="Slit Width (μm)", orient=tk.HORIZONTAL, resolution=1, command=update_plot)
slit_slider.set(20)
slit_slider.pack(fill='x', pady=2)

# Slit Separation
separation_slider_frame = ttk.Frame(controls)
separation_slider = tk.Scale(separation_slider_frame, from_=10, to=500, label="Slit Separation (μm)", orient=tk.HORIZONTAL, resolution=1, command=update_plot)
separation_slider.set(100)
separation_slider.pack(fill='x')

# N-Slit Count
n_slider_frame = ttk.Frame(controls)
n_slider = tk.Scale(n_slider_frame, from_=2, to=10, label="Number of Slits (N)", orient=tk.HORIZONTAL, resolution=1, command=update_plot)
n_slider.set(4)
n_slider.pack(fill='x')

toggle_sliders()
root.mainloop()
