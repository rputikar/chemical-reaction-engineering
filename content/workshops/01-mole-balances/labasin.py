#%%
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib
matplotlib.rcParams.update({'font.size': 13, 'lines.linewidth': 2.5})
from matplotlib.widgets import Slider, Button

A = 372176640000 # Total area of South CA Basin (ft2)
Cars = 10.8*(10**6) # Total number of vehicles in SoCAB
H = 2000 # Height of Basin (ft)
Cars1ppm = 2.5
Cars2ppm = 1.8
Cars3ppm = 2.2
PBasin = 1 # atm
vwind = 79200 # ft/h wind velocity
vemissions = 3000 # ft3/h STD vehicular emissions
Temissions = 491.67 # R eq. 0?C
COwind0 = 2.04*(10**-10) # lbmol CO / ft3

def ODEfun(Yfuncvec, t, A, Cars, H, Cars1ppm, Cars2ppm, Cars3ppm, 
          PBasin, vwind, vemissions, Temissions, COwind0): 
    CO1 = Yfuncvec[0]
    CO2= Yfuncvec[1]
    CO3=Yfuncvec[2]
    # Explicit equations
    A1 = A * .5 #Area of Los Angeles
    A2 = A * .5 * .2 # Area of Orange County
    A3 = A * .5 * .6 # Area of Riverside County
    Cars1 = Cars * .55 # Number of cars in LA
    Cars2 = Cars * .25 # Number of cars in Orange
    Cars3 = Cars * .20 # Number of cars in Riverside
    R = 0.7302 # ft3*atm/lbmol*R
    corridor = 105600 * 2000 # ft2 wind corridor
    ncars1 = PBasin * vemissions / (R * Temissions) * Cars1 # lbmol gas emissions from Cars-x
    ncars2 = PBasin * vemissions / (R * Temissions) * Cars2
    ncars3 = PBasin * vemissions / (R * Temissions) * Cars3
    COcars1 = Cars1ppm / 1000000 * ncars1 # lbmol CO emissions from cars
    COcars2 = Cars2ppm / 1000000 * ncars2
    COcars3 = Cars3ppm / 1000000 * ncars3
    Qo = vwind * corridor # vo
    Q1 = Qo + vemissions * Cars1
    Q2 = Q1 + vemissions * Cars2
    Q3 = Q2 + vemissions * Cars3
    COs0 = COwind0 * Qo # lbmol CO in wind
    COs1 = CO1 * Q1
    COs2 = CO2 * Q2
    # Differential equations
    dCO1dt = (COcars1 + COs0 - Q1 * CO1) / (A1 * H)
    dCO2dt = (COcars2 + COs1 - Q2 * CO2) / (A2 * H)
    dCO3dt = (COcars3 + COs2 - Q3 * CO3) / (A3 * H)
    return np.array([dCO1dt, dCO2dt, dCO3dt])


t = np.linspace(0, 72, 100) # Range for the independent variable
y0 = np.array([2.04*10**-8, 2.04*10**-8, 2.04*10**-8]) # Initial values for the dependent variables i.e. CO1;CO2;CO3

#%%
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.subplots_adjust(left  = 0.5)
fig.suptitle("""P1-2B Web Module : L.A.Basin""", fontweight='bold', x = 0.12, y=0.98)
p1, p2, p3 = ax.plot(t, odeint(ODEfun, y0, t, (A, Cars, H ,Cars1ppm, Cars2ppm ,
                                Cars3ppm ,PBasin ,vwind ,
                                vemissions  ,Temissions ,COwind0 )))


plt.legend([r'$CO_{1}$', r'$CO_{2}$', r'$CO_{3}$'], loc='upper right')
ax.set_xlabel('time(hr)', fontsize='medium')
ax.set_ylabel(r'$C_{co} (\dfrac{lbmol}{ft^3}$)', fontsize='medium')
plt.title('Concentration Profile')
plt.grid()
#plt.ylim(0, 12)
plt.xlim(0, 72)

ax.text(-85, -18e-10,'Differential Equations'
         '\n'
         r'$\dfrac{dCO_1}{dt} = \dfrac{CO_{cars1} + CO_{s0} - Q_1 * CO_1}{A_1 * H}$'
         '\n'
         r'$\dfrac{dCO_2}{dt} = \dfrac{CO_{cars2} + CO_{s1} - Q_2 * CO_2}{A_2 * H}$'
                  '\n'
         r'$\dfrac{dCO_3}{dt} = \dfrac{CO_{cars3} + CO_{s2} - Q_3 * CO_3}{A_3 * H}$'

         '\n'
         '\n'
         'Explicit Equations'
         '\n'
         r'$A_1 = A/2$'
                  '\n\n'
         r'$A_2 = A/10$'
                  '\n\n'
         r'$A_3 = A*0.3$'
                  '\n\n'
         r'$Cars_1 = Cars*0.55$'
                  '\n\n'
         r'$Cars_2 = Cars*0.25$'
                  '\n\n'
         r'$Cars_3 = Cars*0.2$'
                  '\n\n'
         r'$Corridor = 105600 * 2000$'
         '\n\n'
         r'$n_{cars1} = {(P_{Basin} * v_{emissions})*Cars_1} / (R * T_{emissions})$'
                  '\n\n'
         r'$n_{cars2} = {(P_{Basin} * v_{emissions})*Cars_2} / (R * T_{emissions})$'
                  '\n\n'
         r'$n_{cars3} = {(P_{Basin} * v_{emissions})*Cars_3} / (R * T_{emissions})$'
         '\n\n'
         r'$Q_o = v_{wind} * corridor$'
                  '\n\n'
         r'$Q_1 = Q_o + v_{emmissions} * Cars_1$'
                           '\n\n'
         r'$Q_2 = Q_o + v_{emmissions} * Cars_2$'
                           '\n\n'
         r'$Q_3 = Q_o + v_{emmissions} * Cars_3$'
                           '\n\n'
         r'$CO_{s0} = CO_{wind0} * Q_o$'
                           '\n\n'
         r'$CO_{s1} = CO_1 * Q_1$'
                           '\n\n'
         r'$CO_{s2} = CO_2 * Q_2$'
         , ha='left', wrap = True, fontsize=11,
        bbox=dict(facecolor='none', edgecolor='black', pad=10.0), fontweight='bold')

axcolor = 'black'
ax_A = plt.axes([0.3, 0.75, 0.1, 0.02], facecolor=axcolor)
ax_Cars = plt.axes([0.3, 0.7, 0.1, 0.02], facecolor=axcolor)
ax_H = plt.axes([0.3, 0.65, 0.1, 0.02], facecolor=axcolor)
ax_Cars1ppm = plt.axes([0.3, 0.60, 0.1, 0.02], facecolor=axcolor)
ax_Cars2ppm = plt.axes([0.3, 0.55, 0.1, 0.02], facecolor=axcolor)
ax_Cars3ppm = plt.axes([0.3, 0.5, 0.1, 0.02], facecolor=axcolor)
ax_PBasin = plt.axes([0.3, 0.45, 0.1, 0.02], facecolor=axcolor)
ax_vwind = plt.axes([0.3, 0.4, 0.1, 0.02], facecolor=axcolor)
ax_vemissions = plt.axes([0.3, 0.35, 0.1, 0.02], facecolor=axcolor)
ax_Temissions = plt.axes([0.3, 0.3, 0.1, 0.02], facecolor=axcolor)
ax_COwind0 = plt.axes([0.3, 0.25, 0.1, 0.02], facecolor=axcolor)

sA = Slider(ax_A, r'$A (ft^2)$', 1.71*10**11, 5.72*10**11, valinit=372176640000, valfmt="%1.2E")
sCars = Slider(ax_Cars, r'$Cars$', 1*10**6, 2.5*10**8, valinit=10.8*(10**6), valfmt="%1.2E")
sH= Slider(ax_H, r'$H (ft)$', 500, 3000, valinit=2000, valfmt="%1.0f")
sCars1ppm = Slider(ax_Cars1ppm, r'$CO_{Cars1} (ppm)$', 0.05, 50, valinit=2.5)
sCars2ppm = Slider(ax_Cars2ppm, r'$CO_{Cars2} (ppm)$', 0.05, 50, valinit=1.8)
sCars3ppm = Slider(ax_Cars3ppm, r'$CO_{Cars3} (ppm)$', 0.05, 50, valinit= 2.2)
sPBasin = Slider(ax_PBasin, r'$P_{Basin} (atm)$', 0.1, 20, valinit=1)
svwind = Slider(ax_vwind, r'$v_{wind} (\frac{ft}{hr})$', 49200, 95200, valinit=79200, valfmt="%1.2E")
svemissions = Slider(ax_vemissions, r'$v_{emissions} (\frac{ft^3}{hr})$', 1000, 12000, valinit=3000, valfmt="%1.2E")
sTemissions = Slider(ax_Temissions, r'$T_{emissions} (K)$', 273, 1000, valinit=491.67, valfmt="%1.2E")
sCOwind0 = Slider(ax_COwind0, r'$CO_{wind0} (\frac{lbmol CO}{ft^3})$', 4.*10**-11, 5.04*10**-10, valinit=2.04*(10**-10), valfmt="%1.2E")


def update_plot(val):
    A = sA.val
    Cars =sCars.val
    H =sH.val
    Cars1ppm = sCars1ppm.val
    Cars2ppm =sCars2ppm.val
    Cars3ppm = sCars3ppm.val
    PBasin = sPBasin.val
    vwind = svwind.val
    vemissions = svemissions.val
    Temissions = sTemissions.val
    COwind0 = sCOwind0.val
    x = odeint(ODEfun, y0, t, (A, Cars, H ,Cars1ppm, Cars2ppm ,
                                Cars3ppm,PBasin ,vwind ,
                                vemissions  ,Temissions,COwind0 ))
    p1.set_ydata(x[:, 0])
    p2.set_ydata(x[:, 1])
    p3.set_ydata(x[:, 2])
    fig.canvas.draw_idle()


sA.on_changed(update_plot)
sCars.on_changed(update_plot)
sH.on_changed(update_plot)
sCars1ppm.on_changed(update_plot)
sCars2ppm.on_changed(update_plot)
sCars3ppm.on_changed(update_plot)
sPBasin.on_changed(update_plot)
svwind.on_changed(update_plot)
svemissions.on_changed(update_plot)
sTemissions.on_changed(update_plot)
sCOwind0.on_changed(update_plot)

resetax = plt.axes([0.3, 0.8, 0.09, 0.04])
button = Button(resetax, 'Reset Variables', color='cornflowerblue', hovercolor='0.975')


def reset(event):
    sA.reset()
    sCars.reset()
    sH.reset()
    sCars1ppm.reset()
    sCars2ppm.reset()
    sCars3ppm.reset()
    sPBasin.reset()
    svwind.reset()
    svemissions.reset()
    sTemissions.reset()
    sCOwind0.reset()
button.on_clicked(reset)


plt.show()

