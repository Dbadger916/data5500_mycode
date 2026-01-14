class Rectangle():
    def __init__(self,width,length):
        self.width = width
        self.length = length

    def areaCalc(self):
        print(self.width*self.length)

rectangle = Rectangle(3,5)
rectangle.areaCalc()