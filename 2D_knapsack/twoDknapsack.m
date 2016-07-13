m = 100;
n = 101;

n_var = m*(m+1)/2;
f = ones(n_var,1);
intcon = 1:n_var;
lb = zeros(n_var,1);
Aeq = [];
for i = 1:m
    temp = zeros(m,m-i+1);
    for j = 1:m-i+1
        for k = 1:i
            temp(j+k-1,j)=i;
        end 
    end
    temp
    Aeq = [Aeq temp];
end

beq = n*ones(m,1);
    
        

x = intlinprog(f,intcon,[],[],Aeq,beq,lb,[]);
x