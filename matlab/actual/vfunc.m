function dvdt = vfunc(inputmatrix)
%v part of ODE system

v = inputmatrix(1);
w = inputmatrix(2);
iv = inputmatrix(3);

alpha = 10;
k = 10;

a = 1;
beta = 1 - 0.1 * log(k);
c = 1;

vm0 = 1.5;

iw = iv * -75;


dvdt = k * ((v + vm0) - alpha * (v + vm0) ^ 3 + w) + iv;

end