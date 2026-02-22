def easy(array):
    sum = 0
    for i in array:
        sum += i
    print(sum)

myarray = [1,2,3,4,5,5,55,89,5,5,5,5,5,5,5,5]

easy(myarray)
        

#the time complexity of this solution is O(n) , because we loop through the array
#once and thats all