from OOPmodel import BacterialModel
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns

# expand colour palette for matplotlib
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["tab:blue", "tab:orange", "tab:pink", "tab:green", "tab:red", "tab:purple", "tab:gray", "tab:olive", "tab:cyan", 'darkgreen', 'tan', 'salmon', 'gold'])


# parameters in the differential equation of w.
# While these parameters were included in the script,
# they are not effective in our simulations as they are multiplication terms set as 1.
a = 1.
b = 1.
c = 1.
# This parameter corresponds to /alpha in the equation.
alpha = 10.
# This parameter corresponds to k_K in the equation.
# here we make a range of K's to see how the model behaves with different parameters
krange = np.array([10.0, 8, 6, 4, 2, 1, 0.75, 0.5, 0.4, 0.3, 0.2, 0.1])
# krange = np.array([0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01])
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

# create list of models
modellist = []
# populate with models
for i in range(0, len(krange)):
    modellist.append(BacterialModel(krange[i], alpha, a, b, c, vw0, vm0, dt))

# run each model with same shock. 2 secs eq, short shock, 4 secs run
for model in modellist:
    model.run(2, False)
    model.run(0.041, True, iv=iv)
    model.run(4, False)
    print("Model done")

# make a figure
fig, ax = plt.subplots(figsize=(5, 4))

# indicate the electrical stimulation window
plt.fill_between([2, 2.041], -4, 4, color='yellow', alpha=0.4)

# plot all models
for model in modellist:
    plt.plot(model.tseries, model.vseries * -1, label=model.k)

plt.ylabel(r'$-\Delta V_m$', size=18)
plt.xlabel(r'time (s)', size=18)

# plt.ylim(-0.5, 2.5)
# plt.xlim(-5, 45)
ax.relim()
plt.legend(loc="upper right", title="k value")
sns.despine()
# plt.tight_layout()
plt.show()
