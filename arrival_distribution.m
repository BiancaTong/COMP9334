n = 10000;
u = rand(n,1);
lambda = 0.35;
x = -log(1-u)/lambda;
nb = 50;
[n_hist,x_hist] = hist(x,nb);
bin_width = x_hist(2)-x_hist(1);
lower = x_hist - bin_width/2;
upper = x_hist + bin_width/2;
y_expected = n*(exp(-lambda*lower)-exp(-lambda*upper));

% plot the histogram
bar(x_hist,n_hist);
hold on
plot(x_hist,y_expected,'r-','Linewidth',3)
hold off
title('arrival time')

print -dpng hist_expon