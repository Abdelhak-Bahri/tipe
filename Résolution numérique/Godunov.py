# coding: utf8

from pylab import *

# Hamiltonien
def h_up(q):
    return 24*q
def h_down(q):
    return 0.24 - q

Dt = 0.1
Dp = 0.1

p_max = 1000
t_max = 10

# Conditions initiales
t0 = 0
p0 = 0

# Paramètres de la gaussienne
sigma = 100
mu = 500
A = 30
cste = 0.005
# q(t = t0, p)
def g(p):
    return exp(-(p-mu)**2/(2*sigma**2))/(sigma*2*pi) * A + cste

def p(j):
    return p0 + (j - 0.5)*Dp

def t(i):
    return t0 + i * Dt

def F(q1, q2):
    return min(h_up(q1), h_down(q2))

def q(i, j):
    return Resultat[i][j]

N_i = int((t_max - t0)/Dt) # Nombre de calculs pour le temps
N_j = int((p_max - p0)/Dp) # Nombre de calculs pour l'espace

print(N_i, N_j)

Resultat = []
Resultat.append([g(p(j)) for j in range(0, N_j+1)])
P = [p(j) for j in range(0, N_j+1)]

for i in range(0, N_i):
    Temp = [g(p0)] # Condition aux bords
    for j in range(1, N_j):
        Temp += [q(i, j) + (Dt/Dp)*(F(q(i, j-1), q(i, j)) - F(q(i, j), q(i, j+1)))]
    Temp += [g(p_max)]
    Resultat.append(Temp)

plot(P, Resultat[0])
plot(P, Resultat[-1])
xlim(0, 1000)
ylim(0, 0.30)
show()