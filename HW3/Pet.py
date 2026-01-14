class Pet():
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def averageLifespan(self):
        if self.species == "Canis lupus familiaris":
            print("10-13 years")
        elif self.species == "Felis catus":
            print("13-17 years")
        elif self.species == "Oryctolagus cuniculus":
            print("8-12 years")
        else:
            print("That's not one of the 3 species that exist in the universe silly")

Bart = Pet("Bart", 5, "Canis lupus familiaris")
Chingle = Pet("Chingle", 10, "Felis catus")
Norticus = Pet("Norticus", 7, "Oryctolagus cuniculus")

Bart.averageLifespan()
Chingle.averageLifespan()
Norticus.averageLifespan()

#https://chatgpt.com/share/6967d7ef-a190-800b-af21-698a4b6b596b