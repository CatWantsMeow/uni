% ������������� ������� ������
t = 0:0.01:10;
y = sin(t .^ 2 - 12 * t);

% �������� � �������� ��������� ����
net = newff([0 10], [20 1], {'tansig', 'purelin'}, 'trainlm');
net.divideFcn = 'dividerand';
net = train(net, t, y);

% ������� ������� � �� �������������
out = sim(net, t);
plot(t, y, t, out);
legend('f(t)', 'Network out')