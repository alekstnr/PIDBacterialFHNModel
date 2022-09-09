for i = 1:length(out)
    plot(out(i).logsout{1}.Values.Time, out(i).logsout{5}.Values.Data, "DisplayName",num2str(SetPointArray(i)))
    hold on
end

legend