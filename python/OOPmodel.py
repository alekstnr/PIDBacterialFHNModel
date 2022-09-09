from scipy.integrate import solve_ivp
import numpy as np


class BacterialModel:
    class InvalidDurationError(Exception):
        def __init__(self) -> None:
            super().__init__("Duration cannot be smaller than time step")

    def __init__(self, k, alpha, a, b, c, vw0, vm0, dt, iviwrel=-75, tstart=2) -> None:
        # input vars and parameters
        self.k = k
        self.alpha = alpha
        self.beta = 1 - 0.1 * np.log(k)
        self.a = a
        self.b = b
        self.c = c
        self.iw = 0.
        self.iv = 0.
        self.iviwrel = iviwrel
        self.vw0 = vw0
        self.v0 = vw0[0]
        self.w0 = vw0[1]
        self.vm0 = vm0
        self.dt = dt
        self.tstart = tstart

        # output vars
        self.vseries = np.array([self.v0])
        self.wseries = np.array([self.w0])
        self.tseries = np.array([0])
        self.ivseries = np.array([0])

    def setstim(self, iv) -> None:
        self.iv = iv
        self.iw = iv * self.iviwrel

    def f(self, t, vw):
        v, w = vw
        dvdt = self.k * ((v + self.vm0) - self.alpha * (v + self.vm0) ** 3 + w) + self.iv
        dwdt = self.a * (-(v + self.vm0) + self.beta - self.c * w) + self.iw
        return np.array([dvdt, dwdt])

    def run(self, duration, stimbool=bool, iv=float) -> None:
        # check duration and tstep
        if int(duration/self.dt) <= 0:
            raise self.InvalidDurationError()

        # create time span and time points for integration
        tspan = np.array([self.tseries[-1], self.tseries[-1] + duration])
        vw0 = np.array([self.vseries[-1], self.wseries[-1]])
        tpoints = np.linspace(tspan[0], tspan[1], int(duration / self.dt))

        # set stimulation if stim is true
        if stimbool:
            self.setstim(iv)
        else:
            self.setstim(0)

        out = solve_ivp(self.f, tspan, vw0, t_eval=tpoints, method="LSODA")

        # add results
        self.vseries = np.concatenate((self.vseries, out.y[0]), axis=0)
        self.wseries = np.concatenate((self.wseries, out.y[1]), axis=0)
        self.tseries = np.concatenate((self.tseries, out.t))

    # below for real time model
    def fstep(self, controller):
        # get last v and w
        v = self.vseries[-1]
        vw = [self.vseries[-1], self.wseries[-1]]

        # set iv and iw from control input after equilibrium reached. controller object must be passed in
        self.setstim(0)
        if self.tseries[-1] > self.tstart:
            self.setstim(controller(v))

        # run differential eqs using self method
        dvdt, dwdt = self.f(None, vw)

        # append data
        self.vseries = np.append(self.vseries, self.vseries[-1] + dvdt * self.dt)
        self.wseries = np.append(self.wseries, self.wseries[-1] + dwdt * self.dt)
        self.tseries = np.append(self.tseries, self.tseries[-1] + self.dt)
        self.ivseries = np.append(self.ivseries, self.iv)
