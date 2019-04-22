% инициализация исходных данных
p = 1;
t = 1 + sin(p * pi / 4);
w1 = [-0.270 -0.410];
b1 = [-0.480 -0.130];
w2 = [0.090 -0.170];
b2 = 0.48;
lr = 0.1;

% вызов функции обратного распространения ошибки
[out1, w1, b1, w2, b2] = ...
    backpropagate(p, t, w1, b1, w2, b2, lr);

% вывод результата
fprintf('out = '); disp(out1);
fprintf('w1 = '); disp(w1);
fprintf('b1 = '); disp(b1);
fprintf('w2 = '); disp(b1);
fprintf('b2 = '); disp(b1);


% инициализация исходных данные
p = -10:0.1:10;
t = 1 + sin(p * pi / 4);
out = zeros(length(p));

% цикл по количеству эпох
for epoch = 1:100
    % цикл по вектору сигналов и значений функции
    for i = 1:length(p)
        % вызов функции обратного распространения ошибки
        [out(i), w1, b1, w2, b2] = ...
            backpropagate(p(i), t(i), w1, b1, w2, b2, lr);
    end
end

% построение графиков функции и ее аппроксимации
plot(p, t, p, out)


function [out, w1, b1, w2, b2] = ...
    backpropagate(p, t, w1, b1, w2, b2, lr)
        % вычисление прямого распространения сигнала
        n1 = w1 * p + b1;
        a1 = logsig(n1);
        n2 = dot(w2, a1) + b2;
        a2 = purelin(n2);

        % вычисление обратного распространения сигнала
        e = t - a2;
        s2 = -2 * dpurelin(n2, a2) * e;
        s1 = dlogsig(n1, a1) .* w2 .* s2;

        % вычисление новых весов и задержек 
        w1 = w1 - lr * s1 * p;
        b1 = b1 - lr * s1;
        w2 = w2 - lr * s2 * a1;
        b2 = b2 - lr * s2;
        
        out = a2;
end
