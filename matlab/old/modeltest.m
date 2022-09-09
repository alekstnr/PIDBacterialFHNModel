clear all; close all; clc;

t = linspace(0,10);
input = [-0.5, -0.5, 0];

out = ode45(@(input)fhnmodel(input),t,-0.5);

plot(out.x, out.y)