def medium(array):
    Large = -10101100100100100010010101001001001010101001010
    secondLarge = -10101010011000111010101010010101010011
    for i in array:
        if i > Large:
            secondLarge = Large
            Large = i
        if i > secondLarge and i < Large:
            secondLarge = i
    print("Largest number is: ", Large,"\nSecond largest is:", secondLarge)

myArray = [4,8,7,9,10,14,3,5,6,7,0,12,-12,78,90]

medium(myArray)

#This solution is O(n), because you only loop through the array once.