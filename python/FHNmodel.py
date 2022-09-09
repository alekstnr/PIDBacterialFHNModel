import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os
import seaborn as sns
plt.ion()
# matplotlib inline

# parameters in the differential equation of w.
# While these parameters were included in the script,
# they are not effective in our simulations as they are multiplication terms set as 1.
a = 1.
b = 1.
c = 1.

# This parameter correponds to /alpha in the equation.
alpha = 10.

# This parameter corresponds to k_K in the equation.
k = 10.

# offset in Vm. Note that this parameter does not affect the dynamics.
vm0 = 1.5

# time step size
dt = 0.001

# time scale of the events
tscale = 60

# max time to simulate
Tmax = 10.

tvec = np.arange(0, Tmax, dt)

# duration of electrical stimulation
ees_duration = 2.5

# tvec for electrical stimulaiton
t_ees = np.arange(0, (ees_duration * (Tmax / dt) / (Tmax * tscale)) * dt, dt)
# initial parameter for v and w
vw0 = [-0.5, -0.5]

# external stimulation in v and w.
# v is membrane potential and w is recovery variables
Iv = 0.001
Iw = -0.075
I1 = np.array([Iv, Iw]) / dt
# parameter for I when no electrical field is applied
I0 = [0, 0]


# ODE
def f(vw, t):
    v, w = vw
    dvdt = k * ((v + vm0) - alpha * (v + vm0) ** 3 + w) + Iv
    dwdt = a * (-(v + vm0) + b - c * w) + Iw
    return np.array([dvdt, dwdt])


# parameter k_K for proliferative cells
k = 10

# calculation of beta
b1 = 1 - 0.1 * np.log(k)

b = b1

# simulation without electric field. This is to bring the system to equilibrium.
Iv, Iw = I0
vwout1p = odeint(f, vw0, tvec)
print(vwout1p)
# simulation with electric field.
Iv, Iw = I1
vwout1pe = odeint(f, vwout1p[-1, :], t_ees)
# simulation after removal of electric field.
Iv, Iw = I0
vwout2p = odeint(f, vwout1pe[-1, :], tvec)


# simulation result combining above.
vwoutp = np.concatenate([vwout1p, vwout1pe, vwout2p])

# All for inhibited cells
# parameter k_K for inhibited cells
#k = 0.1
#b2 = 1- 0.1* np.log(k)

#b = b2

#Iv, Iw = I0
#vwout1i = odeint(f, vw0, tvec)
#Iv, Iw = I1
#vwout1ie = odeint(f, vwout1i[-1,:], t_ees)
#Iv,Iw = I0
#vwout2i = odeint(f, vwout1ie[-1,:], tvec)
#vwouti = np.concatenate([vwout1i, vwout1ie, vwout2i])

# time
time = np.linspace(0, (t_ees.size + 2 * tvec.size) * dt * tscale, t_ees.size + 2 * tvec.size) - tvec.size * dt * tscale

# time frame for plotting. in order to equilibrate the system before stimulation

#frameq = int(tvec.size * 0.9)
frameq = 0

# make a figure
fig, ax = plt.subplots(figsize=(5, 4))

# indicate the electrical stimulation window
plt.fill_between([0, ees_duration], -4, 4, color='yellow', alpha=0.4)

# plot the simulation results
plt.plot(time, vwoutp.transpose()[0]*-1, '-', c='b', alpha=0.6)
#plt.plot(time[frameq:], vwoutp[frameq, 0] - vwoutp[frameq:, 0], '-', c='b', alpha=0.6)
# plt.plot(time[frameq:], vwouti[frameq, 0] - vwouti[frameq:, 0], '-', c='r', lw=4, alpha=0.6)

#plt.xticks(np.arange(0, 55, 10), size=16)
#plt.yticks(np.arange(-0.5, 1.2, 0.5), size=16)

#plt.ylim(-0.5, 1.3)
#plt.xlim(-5, 45)

plt.ylabel(r'$-\Delta V_m$', size=18)
plt.xlabel(r'time (sec)', size=18)

sns.despine()
plt.tight_layout()

# v = np.linspace(-3, 0, 100)

# nulc_v = alpha * (v + vm0) ** 3 - (v + vm0)
# nulc_w = (-a * (v + vm0) + a * b1) / (a * c)
#
# nulc_wi = (-a * (v + vm0) + a * b2) / (a * c)
#
# fig, ax = plt.subplots(2, 1, figsize=(5.3, 8), sharex=True, sharey=True)
#
# ax1 = ax[0]
# ax2 = ax[1]
#
# ax1.plot(v, nulc_v, '0.3', lw=2, ls='--')
# ax1.plot(v, nulc_w, '0.3', lw=2, ls='--')
# ax1.plot(vwoutp[9000:, 0], vwoutp[9000:, 1], c='b', lw=3, alpha=0.5)
#
# ax2.plot(v, nulc_v, '0.2', lw=2, ls='--')
# ax2.plot(v, nulc_wi, '0.2', lw=2, ls='--')
# ax2.plot(vwouti[9000:, 0], vwouti[9000:, 1], c='r', lw=3, alpha=0.5)
#
# plt.xlim(-2.45, -0.2)
# plt.ylim(-3, 2.1)
#
# # ax1.set_xlabel(r'$V_m$ (au)', size = 16)
# ax2.set_xlabel(r'$V_m$ (au)', size=16)
# ax1.set_ylabel(r'$W$ (au)', size=16)
# ax2.set_ylabel(r'$W$ (au)', size=16)

plt.tight_layout()
plt.ioff()
plt.show()
