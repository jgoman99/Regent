using JuMP, GLPK

# creates a person as a dict
function createPerson()
        person = Dict("name"=> people_id, "food"=> 0, "money" => rand(1:10))
        global people_id += 1
        return(person)
end

function createTown(name)
    town = Dict("name"=> name, "people" => [createPerson() for i in 1:100],"money" => 0)
    return(town)
end


#market function. takes a reward_vec, and returns optimal solution
# seems very fast!
function market(reward_vec,num_goods)
    model = Model(
    optimizer_with_attributes(GLPK.Optimizer, "tm_lim" => 60000, "msg_lev" => GLPK.GLP_MSG_OFF)
    )
    num_people = size(reward_vec,1);
    @variable(model, x[1:num_people], Bin)
    @objective(model, Max, sum( reward_vec[i]*x[i] for i=1:num_people) )
    @constraint(model, constraint1, sum(1*x[i] for i=1:num_people) <= num_goods)

    optimize!(model)    

    variable_solutions = zeros(num_people)
    for i=1:num_people
        variable_solutions[i] = getvalue(x[i])
    end
    return(objective_value(model),variable_solutions)
end


# Different kind of functions

function townBuysFood!(town,num_goods, type)
    people = town["people"]
    if type == "ppd"
        reward_vec = [person["money"] for person in people]
        income, variable_solutions = market(reward_vec,num_goods)
        print(variable_solutions)
    end
end 
    

