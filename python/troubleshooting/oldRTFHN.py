import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
from simple_pid import PID

# import seaborn as sns


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
# beta is based on k.
beta = 1 - 0.1 * np.log(k)
# offset in Vm. Note that this parameter does not affect the dynamics.
vm0 = 1.5

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

# time to start control
tstart = 1.1

# data holders
vseries = np.array([v0])
wseries = np.array([w0])
tseries = np.array([0])
ivseries = np.array([0])

# time step size in s
dt = 0.001

# target Vm
goalv = 2

# create PID controller and set sample time as dt. numbers are tunings for P, I, D terms.
pid = PID(0.052, 0.4, 0.6, setpoint=goalv)
pid.sample_time = dt
pid.output_limits = (-20, 20)
pid.set_auto_mode(False, 0)
onceFlag = True

# create plot
fig, ax = plt.subplots()
# ax2 = ax.twinx()

# FPS for sim
fps = 60
# number of times to sim during 1 frame
framescale = 15


def fstep():
    # get last v and w
    global vseries, wseries, tseries, ivseries, onceFlag
    v = vseries[-1]
    w = wseries[-1]

    # set iv and iw from control input after equilibrium reached

    iv = 0
    if tseries[-1] > tstart and onceFlag:
        onceFlag = False
        pid.set_auto_mode(True, 0)
    elif tseries[-1] > tstart:
        iv = pid(v)
    else:
        iv = 0

    iw = iv * -75

    # add test pulse
    # if  3.000 < tseries[-1] < 3.041:
    #    iv = 1
    #    iw = iv * -75
    #    print("STIM")

    # run differential eqs
    dvdt = k * ((v + vm0) - alpha * (v + vm0) ** 3 + w) + iv
    dwdt = a * (-(v + vm0) + beta - c * w) + iw

    # append data
    vseries = np.append(vseries, vseries[-1] + dvdt * dt)
    wseries = np.append(wseries, wseries[-1] + dwdt * dt)
    tseries = np.append(tseries, tseries[-1] + dt)
    ivseries = np.append(ivseries, iv)


def animate(i):
    # generate data
    for j in range(0, framescale):
        fstep()

    # display data
    ax.clear()
    ax.plot(tseries, vseries * -1)
    ax.plot(tseries, ivseries, alpha=0.5)
    plt.axhline(y=goalv, color='r', linestyle='-', alpha=0.5)
    plt.axvline(x=tstart, color='black', linestyle='-', alpha=0.2)
    plt.ylabel(r'$-\Delta V_m$', size=18)
    plt.xlabel(r'time (s)', size=18)
    ax.relim()


# animate and show
ani = anim.FuncAnimation(fig, animate, interval=1 / fps)
# ani.to_html5_video()


plt.show()
