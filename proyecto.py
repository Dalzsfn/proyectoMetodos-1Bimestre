# simulador_interes_secante_gui_with_table_final.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def interes_compuesto(i, V0, A, n, Vf):
    if abs(i) < 1e-14:
        return V0 + A * (n - 1) - Vf
    return V0 * (1 + i)**n + A * (((1 + i)**n - (1 + i)) / i) - Vf

# =======================================================
def secante(f, p0, p1, TOL, N0):
    q0 = f(p0)
    q1 = f(p1)

    for _ in range(N0):
        if (q1 - q0) == 0:
            return None
        p = p1 - q1 * (p1 - p0) / (q1 - q0)
        if not math.isfinite(p):
            return None
        if abs(p - p1) < TOL:
            return p
        p0, q0 = p1, q1
        p1, q1 = p, f(p)
    return None

# =======================================================
def generar_serie_detallada(i, V0, A, n):
    """
    Devuelve lista de tuplas (periodo, aporte, capital, ganancia, total)
    donde:
      - aporte: V0 en periodo 1, A en los siguientes
      - capital: saldo antes de aplicar ganancia (prev_total + aporte)
      - ganancia: capital * i
      - total: capital + ganancia
    """
    rows = []
    prev_total = 0.0
    for periodo in range(1, n + 1):
        aporte = V0 if periodo == 1 else A
        capital = prev_total + aporte
        ganancia = capital * i
        total = capital + ganancia
        rows.append((periodo, aporte, capital, ganancia, total))
        prev_total = total
    return rows

# =======================================================
class SimuladorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Interés (Secante)")
        self.geometry("1000x640")
        self.configure(bg="#FFB7C5")

        self.freq_map = {
            "diaria": 365,
            "semanal": 52,
            "mensual": 12,
            "bimestral": 6,
            "trimestral": 4,
            "anual": 1
        }

        self._build_ui()

    def _build_ui(self):
        left = tk.Frame(self, bg="#e6f2ff", bd=0)
        left.place(x=12, y=12, width=340, height=616)

        title = tk.Label(left, text="Simulador de Ahorro", font=("Segoe UI", 16, "bold"),
                         bg="#e6f2ff", fg="#DB7093")
        title.pack(pady=(12,6))

        
        self.entry_V0 = self._labeled_entry(left, "Depósito inicial (V0):", "100")
        self.entry_A = self._labeled_entry(left, "Aporte periódico (A):", "5")
        self.entry_n = self._labeled_entry(left, "Número de periodos (n):", "52")
        self.entry_Vf = self._labeled_entry(left, "Valor final deseado (Vf):", "373.79")

    
        lbl_freq = tk.Label(left, text="Periodo de aportes:", bg="#e6f2ff")
        lbl_freq.pack(pady=(6,0))
        self.freq_var = tk.StringVar(value="semanal")
        freq_combo = ttk.Combobox(left, textvariable=self.freq_var, values=list(self.freq_map.keys()), state="readonly")
        freq_combo.pack(pady=4)

    
        btn_frame = tk.Frame(left, bg="#e6f2ff")
        btn_frame.pack(pady=10)
        calc_btn = tk.Button(btn_frame, text="ñCalcular", bg="#C74375", fg="white",
                             relief="flat", command=self.on_calcular)
        calc_btn.grid(row=0, column=0, padx=6)
        clear_btn = tk.Button(btn_frame, text="Limpiar", bg="#FF00FF", fg="white",
                              relief="flat", command=self.on_limpiar)
        clear_btn.grid(row=0, column=1, padx=6)
        
        self.lbl_i_periodo = tk.Label(left, text="Tasa por periodo: -", bg="#e6f2ff")
        self.lbl_i_periodo.pack(pady=(12,0))
        self.lbl_i_nominal = tk.Label(left, text="Tasa nominal anual (i*factor): -", bg="#e6f2ff")
        self.lbl_i_nominal.pack()
        self.lbl_i_effective = tk.Label(left, text="Tasa efectiva anual (1+i)^m - 1: -", bg="#e6f2ff")
        self.lbl_i_effective.pack()

        
        right = tk.Frame(self, bg="#ffffff", bd=0)
        right.place(x=364, y=12, width=624, height=616)

        hdr = tk.Label(right, text="Tabla de evolución", bg="#ffffff", font=("Segoe UI", 12, "bold"))
        hdr.pack(anchor="nw", padx=12, pady=(8,0))

        
        self.cols = ("Periodo", "Aporte ($)", "Capital ($)", "Ganancia ($)", "Total ($)")
        self.tree = ttk.Treeview(right, columns=self.cols, show="headings", height=12)
        for c in self.cols:
            self.tree.heading(c, text=c)
            
            if c == "Periodo":
                self.tree.column(c, width=80, anchor="center")
            else:
                self.tree.column(c, width=120, anchor="e")
        self.tree.pack(anchor="nw", padx=12, pady=(4,8), fill="x")


        plot_frame = tk.Frame(right, bg="#ffffff")
        plot_frame.pack(fill="both", expand=True, padx=12, pady=8)
        self.fig = plt.Figure(figsize=(6,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Evolución del ahorro")
        self.ax.set_xlabel("Periodo")
        self.ax.set_ylabel("Saldo")
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _labeled_entry(self, parent, label, default=""):
        lbl = tk.Label(parent, text=label, bg="#e6f2ff", anchor="w")
        lbl.pack(fill="x", padx=12, pady=(6,0))
        ent = tk.Entry(parent, bd=1, relief="solid")
        ent.pack(fill="x", padx=12, pady=(4,4))
        ent.insert(0, default)
        return ent

    def on_limpiar(self):
        self.entry_V0.delete(0, tk.END)
        self.entry_A.delete(0, tk.END)
        self.entry_n.delete(0, tk.END)
        self.entry_Vf.delete(0, tk.END)
        self.tree.delete(*self.tree.get_children())
        self.ax.clear()
        self.ax.set_title("Evolución del ahorro")
        self.ax.set_xlabel("Periodo")
        self.ax.set_ylabel("Saldo")
        self.canvas.draw()
        self.lbl_i_periodo.config(text="Tasa por periodo: -")
        self.lbl_i_nominal.config(text="Tasa nominal anual (i*factor): -")
        self.lbl_i_effective.config(text="Tasa efectiva anual (1+i)^m - 1: -")
        self._last_series = None

    def export_csv(self):
        if not hasattr(self, "_last_series") or self._last_series is None:
            messagebox.showinfo("Exportar", "No hay datos para exportar.")
            return

        first_col_name = self._period_name_for(self.freq_var.get())
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not file:
            return
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([first_col_name, "Aporte ($)", "Capital ($)", "Ganancia ($)", "Total ($)"])
            for periodo, aporte, capital, ganancia, total in self._last_series:
                writer.writerow([periodo, f"{aporte:.2f}", f"{capital:.2f}", f"{ganancia:.2f}", f"{total:.2f}"])
        messagebox.showinfo("Exportar", f"Datos exportados a:\n{file}")

    def _period_name_for(self, key):
        return {
            "diaria": "Día",
            "semanal": "Semana",
            "mensual": "Mes",
            "bimestral": "Bimestre",
            "trimestral": "Trimestre",
            "anual": "Año"
        }.get(key, "Periodo")

    def on_calcular(self):
        try:
            V0 = float(self.entry_V0.get())
            A = float(self.entry_A.get())
            n = int(float(self.entry_n.get()))
            Vf = float(self.entry_Vf.get())
        except Exception:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos.")
            return

        entrada = self.freq_var.get()
        if entrada not in self.freq_map:
            messagebox.showerror("Error", "Selecciona un periodo válido.")
            return

        f = lambda x: interes_compuesto(x, V0, A, n, Vf)

        p0, p1 = 0.001, 0.01
        i_root = secante(f, p0, p1, 1e-12, 500)


        if entrada == "semanal":
            i_anual_nominal = i_root * 52
        elif entrada == "mensual":
            i_anual_nominal = i_root * 12
        elif entrada == "bimestral":
            i_anual_nominal = i_root * 6
        elif entrada == "trimestral":
            i_anual_nominal = i_root * 4
        elif entrada == "diaria":
            i_anual_nominal = i_root * 365
        elif entrada == "anual":
            i_anual_nominal = i_root * 1
        else:
            i_anual_nominal = i_root * self.freq_map[entrada]

        periods_per_year = self.freq_map[entrada]
        i_anual_efectiva = (1 + i_root)**periods_per_year - 1

        self.lbl_i_periodo.config(text=f"Tasa por periodo: {i_root:.10f}  ({i_root*100:.6f}% por periodo)")
        self.lbl_i_nominal.config(text=f"Tasa nominal anual (i*m): {i_anual_nominal*100:.6f}%")
        self.lbl_i_effective.config(text=f"Tasa efectiva anual: {i_anual_efectiva*100:.6f}%  (m={periods_per_year})")


        serie_det = generar_serie_detallada(i_root, V0, A, n)
        self._last_series = serie_det
        
        first_col_name = self._period_name_for(entrada)
        self.tree.heading(self.cols[0], text=first_col_name)

    
        self.tree.delete(*self.tree.get_children())
        xs = []
        ys = []
    
        for periodo, aporte, capital, ganancia, total in serie_det:
            self.tree.insert("", "end", values=(periodo, f"{aporte:.2f}", f"{capital:.2f}", f"{ganancia:.2f}", f"{total:.2f}"))
            xs.append(periodo)
            ys.append(total)

    
        self.ax.clear()
        self.ax.plot(xs, ys, linewidth=2.5, color="#E25098")
        self.ax.set_title(f"Evolución del ahorro (i_por_periodo={i_root:.6f})")
        self.ax.set_xlabel(first_col_name)
        self.ax.set_ylabel("Saldo acumulado")
        self.ax.grid(alpha=0.35, linestyle="--")
        self.canvas.draw()

if __name__ == "__main__":
    app = SimuladorApp()
    app.mainloop()
