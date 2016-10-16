def  chickens(p, q, r, m):
    
    generationHens = [1]
    generationDays = [0]
    eggGenerations = [0 for x in range(0, q)]
    hatchedGenerations = [0 for x in range(0, r)]

    numHens = 1
    numEggs = 0
    while(m > 0):
        numEggs = numHens*p
        hatching = eggGenerations[-1]
        counter = len(eggGenerations)-1
        while counter > 0:
            eggGenerations[counter] = eggGenerations[counter-1]
            counter-=1
        counter = len(hatchedGenerations)-1
        hens = hatchedGenerations[-1]
        while counter > 0:
            hatchedGenerations[counter] = hatchedGenerations[counter-1]
            counter-=1
        hatchedGenerations[0] =  hatching
        numHens += hens
        m-=1
    numHens += sum(hatchedGenerations)
    
    return numHens


print(chickens(4,5 ,6 ,10))