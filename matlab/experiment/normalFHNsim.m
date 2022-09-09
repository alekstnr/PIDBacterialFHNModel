% pr23_5

% FitzHugh-Nagumo Model Simulation

% Input current I consists of a set of impulses

% showing the nonlinear behavior (i.e. deviation

% from superposition) of the model

clear;

close all;

% parameters

dt=0.1;

ww(1)=0;VV(1)=.1;T(1)=0;

a=.139;b=.008;

c=2.54*.008;

% input current

I=zeros(1,6000);

I(1000)=1;I(2000)=1.5;

I(3000)=1.85;I(4000)=2;I(5000)=3.5;

% loop to simulate the F-N behavior

for i=1:length(I) - 1

 T(i+1)=i*dt;

 ww(i+1)=ww(i)+(b*VV(i)-c*ww(i))*dt;

 VV(i+1)=VV(i)+(VV(i)*(a-VV(i))*(VV(i)-1)-ww(i)+I(i))*dt;

end;

% plot the result

figure;hold;

subplot(211),plot(T,I,'r')

ylabel('Input Current', 'FontSize',13)

subplot(212),plot(T,VV,'k');

xlabel('Time (s)', 'FontSize',13)

ylabel('Membrane Potential', 'FontSize',13)
