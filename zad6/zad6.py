class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1

class RedBlackTree:
    def __init__(self):
        self.nil = Node(0)
        self.nil.color = 0 
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insert(self, k):
        while k.parent and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.nil
        node.right = self.nil
        node.color = 1

        y = None
        x = self.root

        while x != self.nil:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def get_preorder(self, node, result):
        if node != self.nil:
            result.append(node.data)
            self.get_preorder(node.left, result)
            self.get_preorder(node.right, result)
        return result

def solve_rbt_preorder(input_numbers):
    rbt = RedBlackTree()
    for num in input_numbers:
        rbt.insert(num)
    
    preorder_list = []
    rbt.get_preorder(rbt.root, preorder_list)
    return preorder_list

# Example
# 8
# 20 5 6 40 25 16 12 7

n = int(input())
data = map(int, input().split())

result_order = solve_rbt_preorder(data)
print(f"Preorder: {result_order}")
