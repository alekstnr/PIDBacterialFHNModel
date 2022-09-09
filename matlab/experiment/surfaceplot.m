%% Prepare data
% clip time
truncTime = out(1).tout;
truncTime(1:2000) = [];

% build error matrix, maintain same length as first array.
% the long lines get the data part of the sample of the timeseries within
% our truncated time.
ErrorMatrix = [];
maxSamples = length(out(1).logsout{5}.Values.getsampleusingtime(truncTime(1), truncTime(end)).Data);

for i = 1:length(out)
    ErrorArray = out(i).logsout{5}.Values.getsampleusingtime(truncTime(1), truncTime(end)).Data;
    len = length(ErrorArray);
    if len > maxSamples
        sampleIndex = int64(linspace(1, len, maxSamples));
        samples = ErrorArray(sampleIndex);
        ErrorMatrix = [ErrorMatrix; samples'];
    else
        ErrorMatrix = [ErrorMatrix; ErrorArray'];
    end
end

absErrorMatrix = abs(ErrorMatrix);
plotTime = truncTime - 2;

%% Make graph
% plot using trunctime - 2 to start at 0.
s = surf(plotTime, SetPointArray, absErrorMatrix);
s.EdgeColor = "none";

xlabel("Time (s)", FontSize=16)
ylabel("Set point", FontSize=16)
zlabel("abs Error", FontSize=16)

fig = gcf;
ax = fig.CurrentAxes;
ax.TickDir = "out";
ax.Layer = "top";

axis tight

cb = colorbar;
ylabel(cb, "abs Error", FontSize=16)


view(2)
