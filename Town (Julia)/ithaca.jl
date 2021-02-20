using StatsBase, Distances

#Notes:
# check key order is right. Note: this is poss a hard error. we hope dict values in order as we use that for distance

#global variables
people_id = 1;
culture_id = 1;
cultures_global = []

# may want to add 'global'
cultures = ["red","blue","green","orange","brown","cyan","teal","lightblue","darkblue"];
foods = ["potato","rice","wheat"];
luxuries = ["tea","coffee"];
customs = ["xenophobia","tradition","foodCulture","luxuryCulture","curiosity"]

# creates a culture
# cultures are dynamic, and can recieve new keys from a list. So some customs matter for a culture, others do not... until they do.
# cultures have a name, a preferred food and bestLuxury
# cultures have customs, which change how they interact with the world
# xenophobia - how much a culture hates outsiders
# tradition - how much a culture resists assimiliation.
# curiosity - affects drift

function createCulture()
    global culture_id;
    name = cultures[culture_id];
    culture_id += 1;
    goodsDict = Dict("bestFood"=> foods[rand(1:length(foods))],"bestLuxury" => luxuries[rand(1:length(luxuries))]);
    # number of customs a culture can start with
    num_customs = length(customs);#rand(1:length(customs))
    culture = sample(customs, num_customs, replace=false);
    customsDict = Dict();
    for i = 1:num_customs
        customsDict[culture[i]] = rand(1:100);
    end
    culture = Dict("name"=> name, "goods" => goodsDict, "customs" => customsDict);
    global cultures_global
    append!(cultures_global,culture)
    return(culture)
end

function createPop(culture)
    #added her to hope that culture stops being overwritten
    culture_copy = deepcopy(culture);
    global people_id;
    popName = people_id;
    popCulture = culture_copy["name"];
    people_id += 1;
    goodsDict = Dict("bestFood"=> culture_copy["goods"]["bestFood"], "bestLuxury" => culture_copy["goods"]["bestLuxury"]);
    customsDict = culture_copy["customs"];
    #this may slow things down
    new_customs = customs[.![custom in keys(culture_copy["customs"]) for custom in customs]];
    for i = 1:length(new_customs)
        customsDict[new_customs[i]] = rand(1:100);
    end

    discontent = 0;
    pop = Dict("name"=> popName, "culture" => popCulture,"goods" => goodsDict, "customs" => customsDict,"discontent" => 0)
    return(pop)

end

#ways to increase speed here
function cultureDist(entity1,entity2)
    arr_1 = []
    arr_2 = []
    for key in keys(entity1["customs"])
        if key in keys(entity2["customs"])
            entity1_val = entity1["customs"][key]
            entity2_val = entity2["customs"][key]
            append!(arr_1,entity1_val)
            append!(arr_2,entity2_val)
        end

    end

    arr_1 = convert(Array{Float64,1}, arr_1)
    arr_2 = convert(Array{Float64,1}, arr_2)
    culture_dist = (-(arr_1-arr_2))/(length(keys(entity1["customs"])))
    return(culture_dist)
end

function cultureDistVec(entity1,vec)
    arr_1 = []
    arr_2 = []
    for (index,key) in enumerate(keys(entity1["customs"]))
        append!(arr_1,entity1["customs"][key])
        append!(arr_2,vec[index])
    end
    dist_vec = (-(arr_1-arr_2))/(length(keys(entity1["customs"])))
    return(dist_vec)
end


function culturalAssimilation!(entity1,distance)
    tradition = entity1["customs"]["tradition"]
    for (index,key) in enumerate(keys(entity1["customs"]))
        if (distance[index] > 0)
            entity1["customs"][key] += min(distance[index],1)*((100-tradition)/100)
        else
            entity1["customs"][key] += max(distance[index],-1)*((100-tradition)/100)
        end
    end
end

#hmmm law of large numbers may cause no drift...
function culturalDrift!(entity1)
    willingness_to_change = entity1["customs"]["curiosity"] + entity1["discontent"]
    for key in keys(entity1["customs"])
        entity1["customs"][key] += rand(-100:100)*(willingness_to_change/5000)
    end
end

function getAverageCulture(pop_list)
    sum_cultures = zeros(length(customs))
    num_people = length(pop_list)
    for pop in pop_list
        sum_cultures += collect(values(pop["customs"]))
    end
    return(sum_cultures/num_people)
end

function getStd(pop_list)
    pop_matrix = []
    i = 0
    for pop in pop_list
        if i == 0
            i = 1
            pop_matrix = reshape(collect(values(pop["customs"])),1,length(customs))
        end
        pop_matrix = [pop_matrix; reshape(collect(values(pop["customs"])),1,length(customs))] 
    end
    std_list = []
    for i = 1:size(pop_matrix,2)
        std_value = StatsBase.std(pop_matrix[:,i])
        append!(std_list,std_value)
    end

    return(std_list)
end

function boundValues!(entity1)
    for key in keys(entity1["customs"])
    entity1["customs"][key] = min(entity1["customs"][key],100)
    entity1["customs"][key] = max(entity1["customs"][key],0)
    end
end

function culturalChangeRegion!(pop_list)
    average_culture = getAverageCulture(pop_list)
    for pop in pop_list
        distance = cultureDistVec(pop,average_culture)
        culturalAssimilation!(pop,distance)
        culturalDrift!(pop)
        boundValues!(pop)
    end
end

function assimilateToAnotherCulture!(pop_list,cultures)
    for culture in cultures
        for pop in pop_list
            distance_abs = cultureDist(pop,culture)
            distance_total = sum([abs(i) for i = distance_abs])
            if distance_total < 10
                pop["culture"] = culture["name"]
            end
        end
    end
end

function countCulture(pop_list)
    culture_count = Dict()
    for pop in pop_list
        if pop["culture"] in keys(culture_count)
            culture_count[pop["culture"]] += 1
        else
            culture_count[pop["culture"]] = 1
        end
    end
    return(culture_count)
end