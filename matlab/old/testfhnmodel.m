function [dvdt, dwdt] = testfhnmodel(inputmatrix)
%FHNmodel takes inout array of v and w and returns the next dvdt and dwdt
%in the model.

v = inputmatrix(1);
w = inputmatrix(2);
Iv = inputmatrix(3);

alpha = 10;
k = 10;

a = 1;
beta = 1 - 0.1 * log(k);
c = 1;

vm0 = 1.5;

Iw = Iv * -75;


dvdt = k * ((v + vm0) - alpha * (v + vm0) ^ 3 + w) + Iv;

dwdt = a * (-(v + vm0) + beta - c * w) + Iw;

end

