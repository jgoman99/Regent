using JuMP, GLPK
m = Model(
    optimizer_with_attributes(GLPK.Optimizer, "tm_lim" => 60000, "msg_lev" => GLPK.MSG_OFF)
)



# Declaring variables
@variable(m, 0<= x1 <=10)
@variable(m, x2 >=0, Int)
@variable(m, x3 >=0, Bin)
@variable(m, x[1:3], Bin)

# Setting the objective
#@objective(m, Max, x1 + 2x2 + 5x3)
c = [1; 2; 5]
@objective(m, Max, sum( c[i]*x[i] for i=1:3))

# Adding constraints
#@constraint(m, constraint1, -x1 +  x2 + 3x3 <= -4)
#@constraint(m, constraint2,  x1 + 3x2 - 7x3 <= 10)
A = [-1  1  3;
      1  3 -7]
b = [-5; 10]
@constraint(m, constraint[j=1:2], sum(A[j,i]*x[i] for i=1:3) <= b[j])
@constraint(m, bound, x[1] <= 10)

print(m)

optimize!(m)


println("Optimal Solutions:")
for i=1:3
  println("x[$i] = ", getvalue(x[i]))
end

println("Dual Variables:")
for j=1:2
  println("dual[$j] = ", getdual(constraint[j]))
end

objective_value(m)