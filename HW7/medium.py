class Node():
    def __init__(self,key):
        self.left = None
        self.right = None
        self.key = key

def insert(node, key):
    if node is None:
        return Node(key)
    
    if key > node.key:
        node.right = insert(node.right,key)
    elif key < node.key: 
        node.left = insert(node.left,key)

    return node


def search(root, value):
    if root is None:
        print("not here!")
        return False
    if value > root.key:
        search(root.right,value)
    elif value < root.key:
        search(root.left,value)
    else:
        print("Found it!")
        return True

def main():
    # creating a Tree with root variable "root"
    root = None
    root = insert(root, 50)
    root = insert(root, 30)
    root = insert(root, 20)
    root = insert(root, 40)
    root = insert(root, 70)
    root = insert(root, 60)
    root = insert(root, 80)
    search(root, 50)
    search(root, 54)
    search()

main()
