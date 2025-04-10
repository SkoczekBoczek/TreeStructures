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
        # print(f"BST: Inserting {value}")
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
        if not node:
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

            # Gdy element ma 2 potokmków 
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


# ===== RÓWNOWAŻENIE ===== ZMIENNNNNNNNEEEEE
    def rebalanceDsw(self):
        print("BST: Rebalancing using DSW algorithm")
        currentTail = tempRoot = TreeNode(None)
        tempRoot.right = self.root
        currentNode = self.root

        while currentNode:
            if currentNode.left:
                tmp = currentNode.left
                currentNode.left = tmp.right # prawe dziecko tmp staje sie lewym dzieckiem currentNode
                tmp.right = currentNode  # prawe dziecko tmp to currnetNode
                currentNode = tmp # currentNode = 6
                currentTail.right = tmp 
            else:
                currentTail = currentNode
                currentNode = currentNode.right


        # Faza 2
        n = self.countNodes()  # Liczba węzłów w drzewie
        m = self.calculateM(n)  # Ile poziomów ma mieć drzewo.
    
        self.compress(tempRoot, n - m)
    
        # Kolejne kompresje: stopniowo balansuj drzewo
        while m > 1:
            m = m // 2
            self.compress(tempRoot, m)
    
        self.root = tempRoot.right  # Ustaw nowy korzeń

    def countNodes(self):
        count = 0
        node = self.root
        while node:
            count += 1
            node = node.right
        return count

    def calculateM(self, n):
        m = 1
        while m * 2 <= n + 1:
            m *= 2
        return m - 1

    def compress(self, root, count):
        currentParent = root
        for _ in range(count):
            if not currentParent.right:
                break
            child = currentParent.right
            grandchild = child.right
            
            # Child staje się lewym dzieckiem grandchild
            currentParent.right = grandchild
            child.right = grandchild.left if grandchild else None
            if grandchild:
                grandchild.left = child
            
            currentParent = currentParent.right  # Przejdź do następnego węzła

# ===== RYSOWANIE DRZEWA W TICKZPICTURE =====
    def exportToTikz(self, filename='tree.tex'):
        tikzLines = [
            r"\begin{tikzpicture}[",
            r"    level distance=10mm,",
            r"    every node/.style={fill=red!60,circle,inner sep=1pt, minimum size=6mm},",
            r"    level 1/.style={sibling distance=20mm,nodes={fill=red!45}},",
            r"    level 2/.style={sibling distance=10mm,nodes={fill=red!30}},",
            r"    level 3/.style={sibling distance=5mm,nodes={fill=red!25}}",
            r"]",
            ""
        ]

        if self.root is not None:
            tikzBody = self.generateTikzNode(self.root)
            tikzLines.append(f"\\node {tikzBody};")
        else:
            tikzLines.append("% Tree is empty")

        tikzLines.append(r"\end{tikzpicture}")

        with open(filename, 'w') as f:
            f.write('\n'.join(tikzLines))
        
        print(f"TikZ tree exported to {filename}")

    def generateTikzNode(self, node):
        if node is None:
            return ""

        line = f"{{{node.value}}}"
        left = self.generateTikzNode(node.left)
        right = self.generateTikzNode(node.right)

        if node.left or node.right:
            line += "\n"
            if node.left:
                line += f"child {{node {left}}}\n"
            else:
                line += "child[missing]{}\n"
            if node.right:
                line += f"child {{node {right}}}"
            else:
                line += "child[missing]{}"
        return line


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
            return 0   # jeśli nie ma dziecka h = 0
        return node.height
    
    
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

        # lewy podwęzeł jest zbyt wysoki (rotacja w prawo)
        if balance > 1 and self._get_balance(node.left) >= 0: 
            return self._right_rotate(node)

        # lewy podwęzeł, ale jego prawy jest wyższy
        if balance > 1 and self._get_balance(node.left) < 0:  # dziecko pochyla się w prawo
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # prawy podwęzeł jest zbyt wysoki (rotacja w lewo)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        
        # prawy podwęzeł, ale jego lewy jest wyższy
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _left_rotate(self, z):
        y = z.right
        tempSubtree = y.left

        # Rotacja
        y.left = z
        z.right = tempSubtree

        # Aktualizacja wysokości
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, y):
        x = y.left
        tempSubtree = x.right

        # Rotacja
        x.right = y
        y.left = tempSubtree

        # Aktualizacja wysokości
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    
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