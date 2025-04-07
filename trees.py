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
    
    
# ===== USUWANIE ELEMENTÓW =====
    def deleteValue(self, value):
        print(f"BST: Deleting {value}")
        self.root = self.deleteNode(self.root, value)

    def deleteNode(self, node, value):
        if node is None:
            print(f"{value} not found in BST.")
            return node

        if value < node.value:
            node.left = self.deleteNode(node.left, value)
        elif value > node.value:
            node.right = self.deleteNode(node.right, value)
        else:
            if node.left is None:
                temp = node.right
                print(f"Removing node {node.value}, replaced by right child")
                return temp
            elif node.right is None:
                temp = node.left
                print(f"Removing node {node.value}, replaced by left child")
                return temp

            temp = self.minValueNode(node.right)
            print(f"Removing node {node.value}, replaced by inorder successor {temp.value}")
            node.value = temp.value
            node.right = self.deleteNode(node.right, temp.value)

        return node
    
# Szukanie następcy in-order (successor)
    def minValueNode(self, node): 
        current = node
        while current.left is not None:
            current = current.left
        return current

        
# ===== USUWANIE DRZEWA =====
    def deleteTreePostOrder(self, node, deletedValues):
        if node is None:
            return
        
        self.deleteTreePostOrder(node.left, deletedValues) # lewe poddrzewo
        self.deleteTreePostOrder(node.right, deletedValues) # prawe poddrzewo

        deletedValues.append(str(node.value))
        node.left = None
        node.right = None
        node.value = None

    def delete(self):
        deletedValues = []
        self.deleteTreePostOrder(self.root, deletedValues)
        self.root = None  # Po usunięciu drzewa, root = None
        print(f"Deleting: {" ".join(deletedValues)}")
        print("BST tree succesfully removed")



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
    
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    

# ===== USUWANIE ELEMENTÓW =====
    def deleteValue(self, value):
        print(f"AVL: Deleting {value} with balancing")
        self.root = self.deleteNode(self.root, value)

    def deleteNode(self, node, value):
        if not node:
            print(f"{value} not found in AVL.")
            return node

        if value < node.value:
            node.left = self.deleteNode(node.left, value)
        elif value > node.value:
            node.right = self.deleteNode(node.right, value)
        else:
            if node.left is None:
                temp = node.right
                print(f"Removing node {node.value}, replaced by right child")
                return temp
            elif node.right is None:
                temp = node.left
                print(f"Removing node {node.value}, replaced by left child")
                return temp

            temp = self.minValueNode(node.right)
            print(f"Removing node {node.value}, replaced by inorder successor {temp.value}")
            node.value = temp.value
            node.right = self.deleteNode(node.right, temp.value)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node
    
#Szukanie następcy in-order (successor)
    def minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

# ===== USUWANIE DRZEWA =====
    def deleteTreePostOrder(self, node, deletedValues):
        if node is None:
            return

        self.deleteTreePostOrder(node.left, deletedValues)
        self.deleteTreePostOrder(node.right, deletedValues)

        deletedValues.append(str(node.value)) 
        node.left = None
        node.right = None
        node.value = None

    def delete(self):
        deletedValues = []
        self.deleteTreePostOrder(self.root, deletedValues)
        self.root = None  # Po usunięciu drzewa, root = None
        print(f"Deleting: {' '.join(deletedValues)}")
        print("AVL tree succesfully removed")
    
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