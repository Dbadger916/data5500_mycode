def hard(array):
    difference = 0
    for i in array:
        for j in array:
            thing = i - j
            if thing > difference:
                difference = thing
    print(difference)

myArray = [1,2,5,6,9,1,0,2,4,6,7,8]
hard(myArray)

#this formula is O(n^2) because we loop through the array one whole time for every
#variable that is in the array