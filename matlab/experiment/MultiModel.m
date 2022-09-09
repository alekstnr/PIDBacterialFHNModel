clc; clear
model = "aggressivefhn";
load_system(model);

SetPointArray = linspace(-1, 5, 100);


for i = length(SetPointArray):-1:1
    in(i) = Simulink.SimulationInput(model);
    in(i) = in(i).setBlockParameter("aggressivefhn/set point","Value", num2str(SetPointArray(i)));
end

out = parsim(in, "ShowSimulationManager","on","ShowProgress","on");