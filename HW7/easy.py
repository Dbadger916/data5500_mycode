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
    elif key < node: 
        node.left = insert(node.left,key)

    return node
