import sys
import re

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        print(f"BST: Inserting {value}")
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_helper(self.root, value)
    
    def _insert_helper(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_helper(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_helper(node.right, value)
    
    def build_from_sorted_array(self, arr):
        self.root = self._build_bst(arr, 0, len(arr)-1)
    
    def _build_bst(self, arr, start, end):
        if start > end:
            return None
        
        mid = (start + end) // 2
        node = TreeNode(arr[mid])
        
        node.left = self._build_bst(arr, start, mid-1)
        node.right = self._build_bst(arr, mid+1, end)
        
        return node
    
    def delete(self, value):
        print(f"BST: Deleting {value}")
        # Do implementacji


# ======= WYPISANIE =======
# InOrder = lewo - korzen - prawo
# PostOrder = lewo - prawo - korzen
# PreOrder = korzen - lewo - prawo

    def printOrder(self):
        in_order = ', '.join(map(str, self.printInorder(self.root)))
        post_order = ', '.join(map(str, self.printPostorder(self.root)))
        pre_order = ', '.join(map(str, self.printPreorder(self.root)))
        
        print(f"In-order: {in_order}")
        print(f"Post-order: {post_order}")
        print(f"Pre-order: {pre_order}")

    def printInorder(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            return result
        self.printInorder(node.left, result)
        result.append(node.value)
        self.printInorder(node.right, result)
        return result

    def printPostorder(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            return result
        self.printPostorder(node.left, result)
        self.printPostorder(node.right, result)
        result.append(node.value)
        return result

    def printPreorder(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            return result
        result.append(node.value)
        self.printPreorder(node.left, result)
        self.printPreorder(node.right, result)
        return result


# ======= ZNAJDOWANIE MIN i MAX =======
    def findMin(self, node):
        if not node.left:
            return node.value
        return self.findMin(node.left)

    def findMax(self, node):
        if not node.right:
            return node.value
        return self.findMax(node.right)

    def findMinMax(self):
        if not self.root:
            print("Tree is empty!")
            return
        print(f"Max: {self.findMax(self.root)}")
        print(f"Min {self.findMin(self.root)}")


class AVL(BST):
    def __init__(self):
        super().__init__()
    
    def build_from_sorted_array(self, arr):
        arr = sorted(arr)
        self.root = self._build_avl(arr, 0, len(arr)-1)
    
    def _build_avl(self, arr, start, end):
        if start > end:
            return None
        
        mid = (start + end) // 2
        node = TreeNode(arr[mid])
        
        node.left = self._build_avl(arr, start, mid-1)
        node.right = self._build_avl(arr, mid+1, end)
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        return node
    
    def _get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def insert(self, value):
        print(f"AVL: Inserting {value} with balancing")
        self.root = self._insert_helper(self.root, value)

    def _insert_helper(self, node, value):
        if not node:
            return TreeNode(value)
        elif value < node.value:
            node.left = self._insert_helper(node.left, value)
        else:
            node.right = self._insert_helper(node.right, value)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)

        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)

        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node
    
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y
    
    def delete(self, value):
        print(f"AVL: Deleting {value} with balancing")
        # Do implementacji
    
# ======= WYPISANIE =======
    def printOrder(self):
        in_order = ', '.join(map(str, self.printInorder(self.root)))
        post_order = ', '.join(map(str, self.printPostorder(self.root)))
        pre_order = ', '.join(map(str, self.printPreorder(self.root)))
        
        print(f"AVL Tree Traversals:")
        print(f"In-order: {in_order}")
        print(f"Post-order: {post_order}")
        print(f"Pre-order: {pre_order}")


# ======= ZNAJDOWANIE MIN i MAX =======
    def findMinMax(self):
        if not self.root:
            print("Tree is empty!")
            return
        print(f"AVL Max: {self.findMax(self.root)}")
        print(f"AVL Min: {self.findMin(self.root)}")


def printMenu():
    print("================================")
    print("{}        {}".format("Help", "Show this message"))
    print("{}       {}".format("Print", "Print the tree using In-order, Pre-order, Post-order"))
    print("{}      {}".format("Remove", "Remove elements from the tree"))
    print("{}      {}".format("Delete", "Delete whole tree"))
    print("{}  {}".format("FindMinMax", "Find minimum and maximum"))
    print("{}      {}".format("Export", "Export the tree to tikzpicture"))
    print("{}   {}".format("Rebalance", "Rebalance the tree"))
    print("{}        {}".format("Exit", "Exits the program (or ctrl+D)"))
    print("================================")

# def cleanInput(raw_data):
#     data = []
#     for item in raw_data:
#         numbers = []
#         for num in item.split(","):
#             cleanedNum = num.strip()
#             if cleanedNum:
#                 numbers.append(cleanedNum)
#         data.extend(numbers)

#     return data

def cleanInput(raw_data):
    data = []
    if isinstance(raw_data, list):
        input_str = ' '.join(raw_data)
    else:
        input_str = raw_data
    
    numbers = re.split(r'[,\s]+', input_str.replace(',', ' ').strip())
    
    for num in numbers:
        if num:
            try:
                data.append(int(num))
            except ValueError:
                print(f"'{num}' is invalid ")
    
    return data

def readInputData():
    if not sys.stdin.isatty():
        return sys.stdin.read().split()

    if len(sys.argv) > 3:
        return cleanInput(sys.argv[3:])

def getInteractiveInput():
    while True:
        try:
            userInput = input("insert> ").strip()
            if userInput:
                return cleanInput(userInput)
        except EOFError:
            print("\nExiting...")
            sys.exit(0)

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--tree" or sys.argv[2] not in ["AVL", "BST"]:
        print("Usage: python3 main.py --tree [AVL|BST] [numbers...]")
        print("Or:    python3 main.py --tree [AVL|BST] <<< 'numbers'")
        print("Or:    python3 main.py --tree [AVL|BST] < file.txt")
        print("Or:    python3 main.py --tree [AVL|BST] num1, num2, num3")
        sys.exit(1)

    treeType = sys.argv[2]

    if treeType == "AVL":
        tree = AVL()
    else:
        tree = BST()
    
    print(f"Tree type: {treeType}")
    def showData(data):
        print(f"Initial data: {data}")

    if len(sys.argv) > 3:
        data = readInputData()
        showData(data)
        if treeType == "AVL":
            tree.build_from_sorted_array(data)
        else:
            for value in data:
                tree.insert(value)

    elif len(sys.argv) == 3:
        data = getInteractiveInput()
        showData(data)
        if treeType == "AVL":
            tree.build_from_sorted_array(data)
        else:
            for value in data:
                tree.insert(value)


    if sys.stdin.isatty():
        print("\nInteractive mode (type 'help' for commands)")
        while True:
            try:
                line = input("action> ").strip().lower()
                if not line:
                    continue
                if line == "help":
                    printMenu()
                elif line == "print":
                    tree.printOrder()
                    print()
                elif line == "remove":
                    print("Removing", treeType)
                elif line == "delete":
                    print("Someday tree will be deleted XXX")
                elif line == "findminmax":
                    tree.findMinMax()
                elif line == "export":
                    print("Export to tikzpicture XXX")
                elif line == "rebalance":
                    if treeType == "AVL":
                        print("AVL tree is always balanced XXX")
                    else:
                        print("BST someday will be rebalanced XXX ")
                elif line == "exit":
                    print("Exiting...")
                    break
                else:
                    print(f"Unknown command: {line}")
            
            except EOFError:
                print("\nExiting...")
                break
    else:
        print("\nProcessing input...")
        print("Done.")

if __name__ == "__main__":
    main()