cd("C:/Users/jgfri/OneDrive/Desktop/Regent/Town (Julia)")
include("./ithaca.jl")

cultures = [createCulture() for i = 1:2]
pop_list = [createPop(c) for c = cultures for i = 1:100]
orig = getAverageCulture(pop_list)
for i = 1:100
    #applies cultural drift and assimilation and bounds
    culturalChangeRegion!(pop_list)
    #applies change to another culture group
    assimilateToAnotherCulture!(pop_list,cultures)
    #print statistics
    println(countCulture(pop_list))
end 
final = getAverageCulture(pop_list)
