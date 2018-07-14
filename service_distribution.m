n = 10000;
u = rand(n,1);
v = rand(n,1);
w = rand(n,1);
nb = 50;
miu = 1;
q = -log(1-u)/miu;
[nq_hist,q_hist] = hist(q,nb);
r = -log(1-v)/miu;
[nr_hist,r_hist] = hist(r,nb);
e = -log(1-w)/miu;
[ne_hist,e_hist] = hist(e,nb);
x = q+r+e;
[n_hist,x_hist] = hist(x,nb);

% plot the histogram
figure
subplot(2,2,1)
bar(q_hist,nq_hist,'facecolor',[0.3 0.7 0.2])
title('first random number')
subplot(2,2,2)
bar(r_hist,nr_hist,'facecolor',[0.7 0.3 0.2])
title('second random number')
subplot(2,2,3)
bar(e_hist,ne_hist,'facecolor',[0.2 0.3 0.1])
title('third random number')
subplot(2,2,4)
bar(x_hist,n_hist)
title('service time')

print -dpng hist_expon