import tkinter as tk
import turtle as trl

class Node():
    def __init__(self, key: int | None) -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.key: int | None = key
        self.coord: tuple[int,int] | None = None

class Tree():
    def __init__(self, node: Node | None) -> None:
        self.tree_root = node

def search(cur_node: Node | None, value) -> bool:
    if cur_node == None:
        return False

    if cur_node.key == value:
        return True

    return search(cur_node.left) if value < cur_node.key else\
           search(cur_node.right)
    
def input(cur_node: Node, value: int, tree: Tree) -> None:
    if cur_node.key == None:
        tree.tree_root = Node(value)
        return

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

#TODO FINISH DELETE
def delete(cur_node: Node, value: int, tree: Tree | None,) -> None:
    if tree.tree_root == None:
        print("Invalid, nothing to delete")
        return
    if cur_node.left.key == value:
        cur_node.left = find_succ(cur_node.left)
        return
    if cur_node.right.key == value:
        cur_node.right = find_pred(cur_node.right)
        return
    if cur_node.key == value:
        tree.tree_root = find_succ(cur_node)


def list_to_int(input_str:str) -> int | None:
    if input_str == '':
        return 
    # Mypy: cannot access local variable 'i' where it is not associated with a value
    i = 0
    result = 0
    input_str = input_str[::-1]
    for i in range(len(input_str) - 1):
        result += int(input_str[i]) * (10 ** i)
    print(i)
    return (result * (-1)) if input_str[i] == '-' else (result + int(input_str[i]) * (10 ** i))


def main_func():
    tree = Tree(Node(None))
    root = tk.Tk()
    root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))

    top_frame = tk.Frame(root, width=400, height=200, background="white", borderwidth=2, relief="solid")
    top_frame.place(x=0,y=0)
    tk.Label(top_frame, text="Input key:", font=("Arial",20), relief="solid", borderwidth=2, height=1, width=10).grid(padx=15, pady=15, row=0, column=0)

    input_box = tk.Text(top_frame, font=("Arial", 20), borderwidth=2, relief="solid", height=1, width=15)
    input_box.grid(padx=15, pady=15, column=1, row=0, columnspan=5)

    tk.Button(top_frame, text="Input", font=("Arial", 20), relief="solid",borderwidth=2,height= 1, width=10, command=lambda :input(tree.tree_root,(list_to_int(input_box.get("1.0","end-1c"))),tree)).grid( row=1, column=0, sticky="w", padx=15, pady=15)
    tk.Button(top_frame, text="Search", font=("Arial", 20), relief="solid",borderwidth=2,height= 1, width=10, command=lambda :search(tree.tree_root,(list_to_int(input_box.get("1.0","end-1c"))))).grid(row=1, column=1, sticky="w", padx=15, pady=15)
    tk.Button(top_frame, text="Delete", font=("Arial", 20), relief="solid",borderwidth=2,height= 1, width=10, command=lambda :delete(tree.tree_root,(list_to_int(input_box.get("1.0","end-1c"))), tree)).grid(row=2, column=0, sticky="w", padx=15, pady=15)

    main_canvas = tk.Canvas(root, height=800, width=1000, relief="solid", background="white", borderwidth=2)
    main_canvas.place(x=500,y=0)
    
    root.mainloop()

main_func()