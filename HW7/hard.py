# When you delete a node, you search through the tree for the node you need, 
# constantly making updates setting the node that you're searching for to be equal
# to the result of the delete function. Once you find the value you want to delete,
# you check to see which scenario you're in
#no children
#if you have no children on that node, you simply return None, and the node above
# that now recognizes its node.right or node.left as none, which means  its been
# deleted
# 1 child
# if you have one child, you return that child to the one above you. Now the one 
# above recognizes your child as its child, and that node has been removed
# 2 children
# with two children, you simply find the smallest value on the right or the 
# largest value on the left, and set the node.key to be equal to that. Since
# the largest on the right or the smallest on the left will always have one or
# no children, you just run delete node on the that value from your 
# node.right or node.left respectively, and you're done