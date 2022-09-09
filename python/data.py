from OOPmodel import BacterialModel
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# parameters in the differential equation of w.
# While these parameters were included in the script,
# they are not effective in our simulations as they are multiplication terms set as 1.
a = 1.
b = 1.
c = 1.
# This parameter corresponds to /alpha in the equation.
alpha = 10.
# This parameter corresponds to k_K in the equation.
k = 10.
# offset in Vm. Note that this parameter does not affect the dynamics.
vm0 = 1.5
# time step size. irrelevant with solve_ivp, unless using t_eval kwarg
dt = 0.001
# time scale of the events
tscale = 60
# iv and iw currents to stimulate. iw is somewhat arbitrary
iv = 1
iw = iv * -75
# initial v and w
vw0 = np.array([-0.5, -0.5])

model = BacterialModel(k, alpha, a, b, c, vw0, vm0, dt)
model.run(2, False)
model.run(0.041, True, iv=iv)
model.run(4, False)

# make a figure
fig, ax = plt.subplots(figsize=(5, 4))

# indicate the electrical stimulation window
plt.fill_between([5, 7.5], -4, 4, color='yellow', alpha=0.4)

plt.plot(model.tseries, model.vseries * -1, "-b")
# plt.xticks(np.arange(0, 55, 10), size=16)
# plt.yticks(np.arange(-0.5, 1.2, 0.5), size=16)

# plt.ylim(-0.5, 1.3)
# plt.xlim(-5, 45)

plt.ylabel(r'$-\Delta V_m$', size=18)
plt.xlabel(r'time (sec)', size=18)

sns.despine()
# plt.tight_layout()
plt.show()
