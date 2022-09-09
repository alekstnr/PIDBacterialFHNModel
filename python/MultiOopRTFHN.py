import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from OOPmodel import BacterialModel
from simple_pid import PID

# import seaborn as sns
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["tab:blue", "tab:orange", "tab:pink", "tab:green", "tab:red", "tab:purple", "tab:gray", "tab:olive", "tab:cyan", 'darkgreen', 'tan', 'salmon', 'gold'])

# input parameters in the differential equation of v and w.
# While these parameters were included in the script,
# they are not effective in our simulations as they are multiplication terms set as 1.
# apart from b which is replaced by beta.
a = 1.
b = 1.
c = 1.
# This parameter corresponds to /alpha in the equation.
alpha = 10.
# This parameter corresponds to k_K in the equation.
k = 10.

# offset in Vm. Note that this parameter does not affect the dynamics.
vm0 = 1.5
# time step size in s
dt = 0.001
# max time to simulate in s
tmax = 3000
# time scale of the events
tscale = 60
# iv and iw currents to stimulate. iw is somewhat arbitrary
# iv = 1
# iw = iv*-75
# initial v and w
v0 = -0.5
w0 = -0.5
vw0 = [v0, w0]

# target Vm
goalv = 1.5

# time to start control
tstart = 1.1

# data holders
vseries = np.array([v0])
wseries = np.array([w0])
tseries = np.array([0])
ivseries = np.array([0])

# create plot
fig, ax = plt.subplots(figsize=(7, 7))
# ax2 = ax.twinx()

# FPS for sim
fps = 144
# number of times to sim during 1 frame
framescale = 3

# here we make a range of K's to see how the model behaves with different parameters
krange = np.array([10.0, 8, 6, 4, 2, 1, 0.75, 0.5, 0.4, 0.3, 0.2, 0.1])

# dict of models and paired PIDS
modelPIDdict = {}
# create model list
modellist = []

# populate with models and PIDS
for i in range(0, len(krange)):
    modellist.append(BacterialModel(krange[i], alpha, a, b, c, vw0, vm0, dt, tstart=tstart))
    modelPIDdict[modellist[i]] = PID(0.052, 0, 0.6, setpoint=goalv)
    modelPIDdict[modellist[i]].sample_time = dt
    modelPIDdict[modellist[i]].output_limits = (-20, 20)


def animate(i):
    # generate data
    for j in range(0, framescale):
        for model in modellist:
            model.fstep(modelPIDdict[model])

    # display data
    ax.clear()
    for model in modellist:
        ax.plot(model.tseries, model.vseries * -1, label=model.k)
        ax.plot(model.tseries, model.ivseries, alpha=0.5)
    plt.axhline(y=goalv, color='r', linestyle='-', alpha=0.5)
    plt.axvline(x=tstart, color='black', linestyle='-', alpha=0.2)
    plt.ylabel(r'$-\Delta V_m$', size=18)
    plt.xlabel(r'time (s)', size=18)
    plt.legend(loc="upper right", title="k value")
    ax.relim()


# animate and show
ani = anim.FuncAnimation(fig, animate, interval=1/fps)
# ani.to_html5_video()

plt.show()
