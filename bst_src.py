import tkinter as tk
from math import sqrt
from random import randint
LEFT = False
RIGHT = True

#TODO IF DEPTH % 3 INCREASE THE DIFFERENCE IN X AND REDRAW

class Node():
    def __init__(self, key: int | None, x: int, y: int) -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.key: int | None = key
        self.coord: tuple[int,int] | None = (x, y)
        self.depth: int | None = 0
        self.parent: Node | None = None

class Tree():
    def __init__(self, node: Node | None) -> None:
        self.tree_root = node

def calc_coord(coord, direction: bool, depth:int):
    if direction:
        return (coord[0] + 250 / depth, coord[1] +(50 + (depth * 12)))
    return (coord[0] - 250 / depth, coord[1] + (50 + (depth * 12)))

def draw_node(canvas: tk.Canvas, x, y, value: int, depth:int) -> None:
    canvas.create_oval(x-20+depth, y-20+depth, x+20-depth, y+20-depth)
    canvas.create_text(x, y, text = str(value), font=("Arial", 14 - depth))

def search(cur_node: Node | None, value) -> Node | None:
    if cur_node.key == value:
        return cur_node

    if cur_node == None:
        return None

    return search(cur_node.left, value) if value < cur_node.key else\
           search(cur_node.right, value)

def input(cur_node: Node, value: int, tree: Tree, canvas: tk.Canvas) -> None:
    if cur_node.key == None:
        tree.tree_root.key = value
        tree.tree_root.depth = 0
        draw_node(canvas, tree.tree_root.coord[0],tree.tree_root.coord[1], value, 0)
        return

    if cur_node.key == value:
        print("Invalid input, key already in tree.")
        return 

    
    if cur_node.key > value:
        if cur_node.left == None:
            x, y = calc_coord(cur_node.coord, LEFT, cur_node.depth + 1)
            cur_node.left = Node(value, x, y)
            cur_node.left.depth = cur_node.depth + 1
            cur_node.left.parent = cur_node
            canvas.create_line(x + 20/sqrt(2) - cur_node.depth, y - 20/sqrt(2) + cur_node.depth, cur_node.coord[0] - 20/sqrt(2) + cur_node.depth, cur_node.coord[1] + 20/sqrt(2) - cur_node.depth)
            draw_node(canvas, cur_node.left.coord[0], cur_node.left.coord[1], value, cur_node.left.depth)
            return

        input(cur_node.left, value, tree, canvas)
        return

    if cur_node.right == None:
        x, y = calc_coord(cur_node.coord, RIGHT, cur_node.depth + 1)
        cur_node.right = Node(value, x, y)
        cur_node.right.depth = cur_node.depth + 1
        cur_node.right.parent = cur_node
        canvas.create_line(x - 20/sqrt(2) + cur_node.depth, y - 20/sqrt(2) + cur_node.depth, cur_node.coord[0] + 20/sqrt(2) - cur_node.depth, cur_node.coord[1] + 20/sqrt(2) - cur_node.depth)
        draw_node(canvas, cur_node.right.coord[0], cur_node.right.coord[1], value, cur_node.right.depth)
        return

    input(cur_node.right, value, tree, canvas)
    return

def find_min(cur_node: Node) -> Node | None:
    if cur_node == None:
        return None
    return cur_node if cur_node.left == None else find_min(cur_node.left)

def find_max(cur_node: Node) -> Node:
    if cur_node == None:
        return None
    if cur_node.right.right == None:
        return cur_node
    if cur_node == None:
        return None
    return cur_node if cur_node.right == None else find_max(cur_node.right)

""" Find_succ/pred used for the deletion of nodes, not for user to find them"""
def find_succ(cur_node: Node) -> Node | None:
    if cur_node == None: # Does not have a successor
        return None
    return find_min(cur_node.right)

def find_pred(cur_node: Node) -> Node | None:
    if cur_node == None: # Does not have a predecessor
        return None
    return find_max(cur_node.left)

def redraw(cur_node: Node, canvas: tk.Canvas) -> None:
    if cur_node.left != None:
        x, y = calc_coord(cur_node.coord, LEFT, cur_node.depth + 1)
        cur_node.left.coord = (x, y)
        cur_node.left.depth = cur_node.depth + 1
        canvas.create_line(x + 20/sqrt(2) - cur_node.depth, y - 20/sqrt(2) + cur_node.depth, cur_node.coord[0] - 20/sqrt(2) + cur_node.depth, cur_node.coord[1] + 20/sqrt(2) - cur_node.depth)
        draw_node(canvas, cur_node.left.coord[0], cur_node.left.coord[1], cur_node.left.key, cur_node.left.depth)
        redraw(cur_node.left, canvas)
    
    if cur_node.right != None:
        x, y = calc_coord(cur_node.coord, RIGHT, cur_node.depth + 1)
        cur_node.right.coord = (x, y)
        cur_node.right.depth = cur_node.depth + 1
        canvas.create_line(x - 20/sqrt(2) + cur_node.depth, y - 20/sqrt(2) + cur_node.depth, cur_node.coord[0] + 20/sqrt(2) - cur_node.depth, cur_node.coord[1] + 20/sqrt(2) - cur_node.depth)
        draw_node(canvas, cur_node.right.coord[0], cur_node.right.coord[1], cur_node.right.key, cur_node.right.depth)
        redraw(cur_node.right, canvas)

    return

def transplant(tree: Tree, u: Node, v: Node) -> None:
    if u.parent == None:
        tree.tree_root = v
        tree.tree_root.coord = (650, 50)
    else:
        if u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
    if v != None:
        v.parent = u.parent
    return

def delete(value: int, tree: Tree, canvas: tk.Canvas) -> None:
    """
        This is a really expensive function with O(n^2),
        due to needing to remove all objects on the canvas,
        and then redrawing them.

        Solution: "move" the nodes and change their x y coords and depth.
        Problem: after moving and deleting the node, it also needs to delete the line connecting it.
                       It can be fixed with creating a list that has tuples with the node.key and the line connecting it.
                       TODO ^^^ 
    """
    to_delete: Node = search(tree.tree_root, value)
    if to_delete == None:
        # Nothing to delete
        print("Invalid input, value not in tree")
        return None

    canvas.delete("all")
    if to_delete.left == None:
        transplant(tree, to_delete, to_delete.right)
    else:
        if to_delete.right == None:
            transplant(tree, to_delete, to_delete.left)
        else:
            replacer = find_min(to_delete.right)
            if replacer.parent != to_delete:
                transplant(tree, replacer, replacer.right)
                replacer.right = to_delete.right
                to_delete.right.parent = replacer
            transplant(tree, to_delete, replacer)
            replacer.left = to_delete.left
            to_delete.left.parent = replacer
    
    destroy_node(to_delete)
    draw_node(canvas, 650, 50, tree.tree_root.key, 0)
    redraw(tree.tree_root, canvas)

def destroy_node(cur_node: Node) -> None:
    cur_node.left = None
    cur_node.right = None
    cur_node.key = None
    cur_node.coord = None
    cur_node.depth = None
    cur_node.parent = None


def list_to_int(input_str:str) -> int | None:
    if input_str == '':
        return 
    if input_str[0] == '-':
        return to_int(input_str[:1])
    input_str = input_str[::-1]
    return to_int(input_str)

def to_int(input_str):
    result = 0
    for i in range(len(input_str) - 1, -1 ,-1):
        result += int(input_str[i]) * (10 ** i)
    return result

def random_input(canvas: tk.Canvas, tree: Tree) -> None:
    reps = randint(20,40)
    for i in range(reps):
        x = randint(0,100)
        input(tree.tree_root, x, tree, canvas)

def main_func():
    tree = Tree(Node(None, 650, 50))
    root = tk.Tk()
    root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))

    top_frame = tk.Frame(root, width=400, height=200, background="white", borderwidth=2, relief="solid")
    top_frame.place(x=0,y=0)
    tk.Label(top_frame, text="Input key:", font=("Arial",20), relief="solid", borderwidth=2, height=1, width=10).grid(padx=15, pady=15, row=0, column=0)

    input_box = tk.Text(top_frame, font=("Arial", 20), borderwidth=2, relief="solid", height=1, width=15)
    input_box.grid(padx=15, pady=15, column=1, row=0, columnspan=5)

    main_canvas = tk.Canvas(root, height=800, width=1300, relief="solid", background="white", borderwidth=2)
    main_canvas.place(x=500,y=0)


    tk.Button(top_frame, text="Input", font=("Arial", 20), relief="solid",borderwidth=2,height= 1, width=10, command=lambda :input(tree.tree_root,list_to_int(input_box.get("1.0","end-1c")),tree, main_canvas)).grid( row=1, column=0, sticky="w", padx=15, pady=15)
    tk.Button(top_frame, text="Search", font=("Arial", 20), relief="solid",borderwidth=2,height= 1, width=10, command=lambda :search(tree.tree_root,list_to_int(input_box.get("1.0","end-1c")), main_canvas)).grid(row=1, column=1, sticky="w", padx=15, pady=15)
    tk.Button(top_frame, text="Delete", font=("Arial", 20), relief="solid",borderwidth=2,height= 1, width=10, command=lambda :delete(list_to_int(input_box.get("1.0","end-1c")), tree, main_canvas)).grid(row=2, column=0, sticky="w", padx=15, pady=15)
    tk.Button(top_frame, text="Random", font=("Arial", 20), relief="solid",borderwidth=2,height= 1, width=10, command=lambda :random_input(main_canvas, tree)).grid(row=2, column=1, sticky="w", padx=15, pady=15)
    
    root.mainloop()

main_func()