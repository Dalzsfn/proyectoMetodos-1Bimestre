
import math
import matplotlib.pyplot as plt

V0 =100
A = 5
n= 52
Vf= 373.79

def interes_compuesto(i, V0, A, n, Vf):
    return V0 * (1 + i)**n + A * (((1 + i)**n - (1 + i)) / i) - Vf



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
    
entrada=input("Ingrese el tipo de interes (semanal, mensual, bimestral, trimestral): ")
if entrada=="semanal":
    i=secante(interes_compuesto,0.01,0.02,10**-3,15)
    i_anual=i*52
    print(i_anual)
    print(i)
    

if entrada=="mensual":
    i=secante(interes_compuesto,0.01,0.02,10**-3,15)
    i_anual=i*12
    
if entrada=="bimestral":
    i=secante(interes_compuesto,0.01,0.02,10**-3,15)
    i_anual=i*6

if entrada=="trimestal":
    i=secante(interes_compuesto,0.01,0.02,10**-3,15)
    i_anual=i*4
    

def interes(i):
    return V0*(1+i)**n-Vf
plt.figure(figsize=(10,6))

plt.plot(i_vals, f_vals, linewidth=2, color="blue", label="f(i)")

plt.axhline(0, color="black", linestyle="--") 
plt.title("Gráfica de la función f(i)")
plt.xlabel("i (tasa por período)")
plt.ylabel("f(i)")
plt.grid(alpha=0.3)
plt.legend()

plt.show()