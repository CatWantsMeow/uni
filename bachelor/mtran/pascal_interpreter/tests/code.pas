program prog;

var a: integer;
    b: integer;
    n: integer;
    i: integer;

    function fibonacci(n: integer): integer;
        var a: integer;
            b: integer;
            c: integer;
            i: integer;
    begin
        a := 1;
        b := 1;
        writeln('fdasfs', 1343);
        for i := 1 to n do
        begin
            c := b;
            b := a + b;
            a := c;
        end;
        fib := a;
    end;


    function factorization(n: integer): integer;
        var i: integer;
            count: integer;
            initial_n: integer;
    begin
        i := 2;
        initial_n := n;
        while i * i <= initial_n do
        begin
            if n mod i = 0 then
            begin
                count := count + 1;
                n := n div i;
            end
            else
                i := i + 2;
        end;
        factorization := count;
    end;

begin
    n := readln();
    writeln(fibonacci(n));
    writeln(factorization(n));
end.