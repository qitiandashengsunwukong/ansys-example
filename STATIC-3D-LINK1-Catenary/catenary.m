 L = 888;
C = -80;
q_y = 60;
Tx = 99549.7776;
beta = q_y*L/(2*Tx);
c1 = asinh((beta*C/L)/sinh(beta))-beta;
c2 = -Tx/q_y*cosh(c1);
cat = @(x) Tx/q_y*cosh(q_y/Tx*x+c1)+c2;
x = 0:L;
y = cat(x);
mid_def = cat(L/2)
plot(x,y)
hold on
axis equal
 