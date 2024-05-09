import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# constants

R = 8.314  # J/ (mol K)
RCAL = 1.987  # cal⋅/ mol K
RATM = 0.082  # atm dm^3/ (mol K)

# reaction
# 2 T -> B + X

# Components
# 0: Toluene
# 1: Benzene
# 2: Xylene

# Heats of formation at 298 K in J/mol
HF = np.array([50.1e3, 82.9e3, 17.4e3])

# Specific Heat Capacities J/mol K
CP = np.array([134, 136, 140])

# Stoichiometry
NU = np.array([-2, 0, 0])  # Reaction : 2T -> B + X

# Heat of reaction at reference temperature J/mol
DELTA_HR_TR = np.dot(NU, HF)

KT = 20  # g mol/h kg-cat atm  at 735K
KD = 1.6  # 1/h at 735K
ET = 25e3  # cal/mol
ED = 10e3  # cal/mol
TR = 735  # K reference temperature for KT and KD

# Functions
kt = lambda t: KT * np.exp((ET / RCAL) * ((1 / TR) - (1 / t)))
kd = lambda t: KD * np.exp((ED / RCAL) * ((1 / TR) - (1 / t)))

# rates
rd = lambda t, a: kd(t) * a**2
rt = lambda t, a, pt: a * kt(t) * pt  # this is -r_t


def batch_reactor(t, y, *args):

    # convert dependent variables
    x, a = y
    (w, pt0, nt0, T0) = args

    pt = pt0 * (1 - x)  # as delta = 0 (epsilon = 0)
    print(pt)

    rate = rt(T0, a, pt)

    dxdt = rate * w / nt0
    dadt = -rd(T0, a)

    dydw = [dxdt, dadt]
    return dydw


# Problem data

# pressure and temperature
T0 = 735  # K
pt0 = 1  # atm
v = 1  # dm^3
w = 5  # kg
nt0 = 1e3 * pt0 * v / (RATM * T0)  # g mol

# Differential equations
# 0: dX/dt
# 1: da/dt

initial_conditions = np.array([0, 1])
args = (w, pt0, nt0, T0)

t_final = 0.5

sol = solve_ivp(
    batch_reactor,
    [0, t_final],
    initial_conditions,
    args=args,
    method="LSODA",
    dense_output=True,
)

# Extract solution
time = np.linspace(0, t_final, 1000)

# conversion
x = sol.sol(time)[0]

# activity
a = sol.sol(time)[1]

print(x[-1], a[-1])

plt.plot(time, x, label="Conversion")
plt.plot(time, a, label="Activity")

plt.xlim(time[0], time[-1])
plt.ylim(0, 1)
plt.grid()
plt.legend()

plt.xlabel("time ($h$)")
plt.ylabel("Conversion")

plt.show()
