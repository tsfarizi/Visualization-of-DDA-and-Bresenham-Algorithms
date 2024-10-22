import tkinter as tk
from tkinter import ttk, messagebox
from algorithms import DDAAlgorithm, BresenhamAlgorithm
from plotting import PlotCanvas

class LineDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisasi Algoritma DDA dan Bresenham")

        self.root.state('zoomed')  

        self.coordinate_range = 50  

        self.initialize_algorithms()
        self.create_widgets()

    def initialize_algorithms(self):
        self.dda_algorithm = DDAAlgorithm()
        self.bresenham_algorithm = BresenhamAlgorithm()

    def create_widgets(self):

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.plot_canvas = self.create_plot_canvas(main_frame, "Visualisasi Algoritma DDA dan Bresenham")
        self.plot_canvas.canvas.get_tk_widget().pack(side=tk.TOP, padx=10, pady=10)

        self.create_legend(main_frame)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        sections_frame = ttk.Frame(bottom_frame)
        sections_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        input_frame = ttk.LabelFrame(sections_frame, text="Input Koordinat")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(input_frame, text="Titik Awal (x1, y1):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.x1_entry = ttk.Entry(input_frame, width=10)
        self.x1_entry.grid(row=0, column=1, padx=5, pady=5)
        self.y1_entry = ttk.Entry(input_frame, width=10)
        self.y1_entry.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(input_frame, text="Titik Akhir (x2, y2):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.x2_entry = ttk.Entry(input_frame, width=10)
        self.x2_entry.grid(row=1, column=1, padx=5, pady=5)
        self.y2_entry = ttk.Entry(input_frame, width=10)
        self.y2_entry.grid(row=1, column=2, padx=5, pady=5)

        self.draw_button = ttk.Button(input_frame, text="Gambar Garis", command=self.draw_line)
        self.draw_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.clear_button = ttk.Button(input_frame, text="Hapus Semua", command=self.clear_all)
        self.clear_button.grid(row=3, column=0, columnspan=3, pady=5)

        calculations_frame = ttk.LabelFrame(sections_frame, text="Perhitungan Persamaan Garis")
        calculations_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.equation_label = ttk.Label(calculations_frame, text="", justify=tk.LEFT, wraplength=500, font=("Courier", 10))
        self.equation_label.pack(side=tk.TOP, anchor='w', padx=5, pady=5)

        differences_frame = ttk.LabelFrame(sections_frame, text="Perbedaan Penggunaan Piksel")
        differences_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        dda_frame = ttk.Frame(differences_frame)
        dda_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        bresenham_frame = ttk.Frame(differences_frame)
        bresenham_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.unique_dda_label = ttk.Label(dda_frame, text="Piksel Unik DDA:")
        self.unique_dda_label.pack(anchor='w', padx=5, pady=2)

        self.dda_listbox = tk.Listbox(dda_frame, height=10, width=20, font=("Courier", 10))
        self.dda_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.dda_listbox.bind('<<ListboxSelect>>', lambda e: self.on_select_unique_pixel(e, 'DDA'))

        self.unique_bresenham_label = ttk.Label(bresenham_frame, text="Piksel Unik Bresenham:")
        self.unique_bresenham_label.pack(anchor='w', padx=5, pady=2)

        self.bresenham_listbox = tk.Listbox(bresenham_frame, height=10, width=20, font=("Courier", 10))
        self.bresenham_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.bresenham_listbox.bind('<<ListboxSelect>>', lambda e: self.on_select_unique_pixel(e, 'Bresenham'))

    def create_plot_canvas(self, parent_frame, title):
        plot_canvas = PlotCanvas(parent_frame, title)
        return plot_canvas

    def create_legend(self, parent_frame):
        legend_frame = ttk.Frame(parent_frame)
        legend_frame.pack(side=tk.TOP, pady=5)

        yellow_label = tk.Label(legend_frame, text="Common (DDA & Bresenham)", bg='yellow', width=40)
        yellow_label.pack(side=tk.LEFT, padx=5)

        blue_label = tk.Label(legend_frame, text="Unique to DDA", bg='blue', fg='white', width=40)
        blue_label.pack(side=tk.LEFT, padx=5)

        red_label = tk.Label(legend_frame, text="Unique to Bresenham", bg='red', fg='white', width=40)
        red_label.pack(side=tk.LEFT, padx=5)

    def clear_all(self):
        self.plot_canvas.clear()
        self.plot_canvas.refresh()
        self.dda_listbox.delete(0, tk.END)
        self.bresenham_listbox.delete(0, tk.END)
        self.equation_label.config(text="")

        self.x1_entry.delete(0, tk.END)
        self.y1_entry.delete(0, tk.END)
        self.x2_entry.delete(0, tk.END)
        self.y2_entry.delete(0, tk.END)

    def draw_line(self):
        
        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get())

            x1_limited = max(min(x1, self.coordinate_range), -self.coordinate_range)
            y1_limited = max(min(y1, self.coordinate_range), -self.coordinate_range)
            x2_limited = max(min(x2, self.coordinate_range), -self.coordinate_range)
            y2_limited = max(min(y2, self.coordinate_range), -self.coordinate_range)

            if (x1 != x1_limited or y1 != y1_limited or
                x2 != x2_limited or y2 != y2_limited):
                self.x1_entry.delete(0, tk.END)
                self.x1_entry.insert(0, f"{x1_limited:.2f}")
                self.y1_entry.delete(0, tk.END)
                self.y1_entry.insert(0, f"{y1_limited:.2f}")
                self.x2_entry.delete(0, tk.END)
                self.x2_entry.insert(0, f"{x2_limited:.2f}")
                self.y2_entry.delete(0, tk.END)
                self.y2_entry.insert(0, f"{y2_limited:.2f}")

        except ValueError:
            messagebox.showerror("Input Tidak Valid", "Harap masukkan nilai numerik yang valid.")
            return


        self.update_drawings(x1_limited, y1_limited, x2_limited, y2_limited)

    def update_drawings(self, x1, y1, x2, y2):
        
        self.dda_point_dict = {}
        self.bresenham_point_dict = {}
        self.dda_points = []
        self.bresenham_points = []

        self.plot_canvas.clear()

        self.plot_canvas.setup_axes(-self.coordinate_range, self.coordinate_range, -self.coordinate_range, self.coordinate_range)

        self.plot_canvas.draw_grid()
        self.plot_canvas.draw_axes()

        self.draw_line_segment(x1, y1, x2, y2)

        self.update_equations(x1, y1, x2, y2)

        self.plot_canvas.refresh()

    def draw_line_segment(self, x1, y1, x2, y2):

        dda_points = self.dda_algorithm.compute_line(x1, y1, x2, y2)
        bresenham_points = self.bresenham_algorithm.compute_line(x1, y1, x2, y2)

        for p in dda_points:
            key = (round(p['rounded_x'], 2), round(p['rounded_y'], 2))
            p['dx'] = x2 - x1
            p['dy'] = y2 - y1
            self.dda_point_dict[key] = p
            self.dda_points.append(p)

        for p in bresenham_points:
            key = (round(p['x'], 2), round(p['y'], 2))
            p['dx'] = x2 - x1
            p['dy'] = y2 - y1
            self.bresenham_point_dict[key] = p
            self.bresenham_points.append(p)

        dda_set = set(self.dda_point_dict.keys())
        bresenham_set = set(self.bresenham_point_dict.keys())

        common_points = dda_set & bresenham_set
        for x, y in common_points:
            self.plot_canvas.add_rectangle(x, y, 'yellow')

        dda_only = dda_set - bresenham_set
        for x, y in dda_only:
            self.plot_canvas.add_rectangle(x, y, 'blue')

        bresenham_only = bresenham_set - dda_set
        for x, y in bresenham_only:
            self.plot_canvas.add_rectangle(x, y, 'red')

        self.plot_canvas.draw_line([x1, x2], [y1, y2])

        self.update_difference_display(dda_only, bresenham_only)

    def update_equations(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        equation = ""

        if dx != 0:
            m = dy / dx
            c = y1 - m * x1
            equation = f"Persamaan Garis:\n"
            equation += f"dx = {x2:.2f} - {x1:.2f} = {dx:.2f}\n"
            equation += f"dy = {y2:.2f} - {y1:.2f} = {dy:.2f}\n"
            equation += f"m (Gradien) = dy / dx = {dy:.2f} / {dx:.2f} = {m:.2f}\n"
            equation += f"c (Intersep) = y1 - m * x1 = {y1:.2f} - ({m:.2f}) * {x1:.2f} = {c:.2f}\n"
            if c >= 0:
                equation += f"Persamaan: y = {m:.2f}x + {c:.2f}"
            else:
                equation += f"Persamaan: y = {m:.2f}x - {abs(c):.2f}"
        else:
            equation = f"Persamaan Garis Vertikal:\n"
            equation += f"x = {x1:.2f}"

        self.equation_label.config(text=equation)

    def update_difference_display(self, dda_only, bresenham_only):

        self.dda_listbox.delete(0, tk.END)
        self.bresenham_listbox.delete(0, tk.END)

        if dda_only:
            for point in sorted(dda_only):
                self.dda_listbox.insert(tk.END, str(point))
        else:
            self.dda_listbox.insert(tk.END, "Tidak ada")

        if bresenham_only:
            for point in sorted(bresenham_only):
                self.bresenham_listbox.insert(tk.END, str(point))
        else:
            self.bresenham_listbox.insert(tk.END, "Tidak ada")

    def on_select_unique_pixel(self, event, algorithm):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            value = widget.get(index)
            if value != "Tidak ada":
                point = eval(value)
                self.show_calculation(point, algorithm)

    def show_calculation(self, point, algorithm):
        x, y = point


        popup = tk.Toplevel(self.root)
        popup.title(f"Perhitungan {algorithm} untuk Piksel ({x}, {y})")
        popup.geometry("500x400")  


        frame = ttk.Frame(popup, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)


        calculation_text = tk.Text(frame, wrap=tk.WORD, font=("Courier", 12), state='disabled')
        calculation_text.pack(fill=tk.BOTH, expand=True)


        if algorithm == 'DDA':
            calc = self.dda_point_dict.get(point)
            if calc:
                x1 = calc['x1']
                y1 = calc['y1']
                x2 = calc['x2']
                y2 = calc['y2']
                dx = calc['dx']
                dy = calc['dy']
                steps = int(max(abs(dx), abs(dy)))
                x_inc = calc['x_inc']
                y_inc = calc['y_inc']

                calculations = f"""Perhitungan DDA pada Titik {point}:

Langkah ke-{calc['step']} dari total {steps} langkah

1. Menghitung Delta:
   - dx = x2 - x1 = {x2:.2f} - {x1:.2f} = {dx:.2f}
   - dy = y2 - y1 = {y2:.2f} - {y1:.2f} = {dy:.2f}

2. Menentukan Jumlah Langkah:
   - steps = max(|dx|, |dy|) = max({abs(dx):.2f}, {abs(dy):.2f}) = {steps}

3. Menghitung Increment:
   - x_inc = dx / steps = {dx:.2f} / {steps} = {x_inc:.2f}
   - y_inc = dy / steps = {dy:.2f} / {steps} = {y_inc:.2f}

4. Menghitung Posisi Titik:
   - x = x0 + step * x_inc = {x1:.2f} + {calc['step']} * {x_inc:.2f} = {calc['x']:.2f}
   - y = y0 + step * y_inc = {y1:.2f} + {calc['step']} * {y_inc:.2f} = {calc['y']:.2f}

5. Setelah Pembulatan:
   - x = {int(round(calc['x']))}
   - y = {int(round(calc['y']))}

Pixel yang Dipilih: ({int(round(calc['x']))}, {int(round(calc['y']))})
"""
            else:
                calculations = f"Titik {point} tidak ditemukan dalam hasil DDA."
        elif algorithm == 'Bresenham':
            calc = self.bresenham_point_dict.get(point)
            if calc:
                x1 = calc['x1']
                y1 = calc['y1']
                x2 = calc['x2']
                y2 = calc['y2']
                dx = calc['dx']
                dy = calc['dy']
                sx = calc['sx']
                sy = calc['sy']
                err = calc['err']
                step = calc['step']

                e2 = 2 * err

                calculations = f"""Perhitungan Bresenham pada Titik {point}:

Langkah ke-{step}

1. Menghitung Delta:
   - dx = |x2 - x1| = |{x2:.2f} - {x1:.2f}| = {dx:.2f}
   - dy = |y2 - y1| = |{y2:.2f} - {y1:.2f}| = {dy:.2f}

2. Menentukan Arah Pergerakan:
   - sx = {'1' if sx > 0 else '-1'}
   - sy = {'1' if sy > 0 else '-1'}

3. Menginisialisasi Error Term:
   - err = dx - dy = {dx:.2f} - {dy:.2f} = {dx - dy:.2f}

4. Menghitung e2:
   - e2 = 2 * err = 2 * {err:.2f} = {e2:.2f}

5. Keputusan Pergerakan:
   - Jika e2 > -dy ({e2:.2f} > -{dy:.2f}): {'Ya' if e2 > -dy else 'Tidak'}
     {'-> x bertambah menjadi x + sx = ' + f"{calc['x'] + sx:.2f}" if e2 > -dy else '-> x tetap'}
     {'-> err dikurangi dengan dy: err = err - dy = ' + f"{err - dy:.2f}" if e2 > -dy else ''}
   - Jika e2 < dx ({e2:.2f} < {dx:.2f}): {'Ya' if e2 < dx else 'Tidak'}
     {'-> y bertambah menjadi y + sy = ' + f"{calc['y'] + sy:.2f}" if e2 < dx else '-> y tetap'}
     {'-> err ditambah dengan dx: err = err + dx = ' + f"{err + dx:.2f}" if e2 < dx else ''}

6. Posisi Selanjutnya:
   - x = {calc['x']:.2f}
   - y = {calc['y']:.2f}

Error Term Selanjutnya: err = {err:.2f}

Pixel yang Dipilih: ({calc['x']:.2f}, {calc['y']:.2f})
"""
            else:
                calculations = f"Titik {point} tidak ditemukan dalam hasil Bresenham."
        else:
            calculations = "Algoritma tidak dikenal."

        calculation_text.configure(state='normal')  
        calculation_text.delete(1.0, tk.END)
        calculation_text.insert(tk.END, calculations)
        calculation_text.configure(state='disabled')  

        close_button = ttk.Button(frame, text="Tutup", command=popup.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')  

    root = tk.Tk()
    app = LineDrawingApp(root)
    root.mainloop()
