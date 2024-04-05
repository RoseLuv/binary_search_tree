class Node():
    def __init__(self, key) -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.key: int = key

class Tree():
    def __init__(self, node: Node) -> None:
        self.tree_root = node

def search(cur_node: Node | None, value) -> bool:
    if cur_node == None:
        return False 
    return search(cur_node.left) if value < cur_node.key else\
           search(cur_node.right)
    
def input(cur_node: Node, value: int, tree: Tree | None) -> Tree | None:
    if tree == None:
        tree = Tree(cur_node)
        return tree

    if cur_node.key == value:
        print("Invalid input, key already in tree.")
        return

    if cur_node.key < value:
        if cur_node.left == None:
            cur_node.left = Node(value)
            return

        input(cur_node.left, value)
        return

    if cur_node.right == None:
        cur_node.right = Node(value)
        return

    input(cur_node.right, value)
    return

def find_min(cur_node: Node) -> Node | None:
    if cur_node == None:
        return None
    return cur_node if cur_node.left == None else find_min(cur_node.left)

def find_max(cur_node: Node) -> Node:
    if cur_node == None:
        return None
    return cur_node if cur_node.right == None else find_max(cur_node.right)

def find_succ(cur_node: Node) -> Node | None:
    if cur_node == None:
        return None
    return find_min(cur_node.right)

def find_pred(cur_node: Node) -> Node | None:
    if cur_node == None:
        return None
    return find_max(cur_node.left)


