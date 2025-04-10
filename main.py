import sys
import re
from trees import BST, AVL

def printMenu():
    print("================================")
    print("{}        {}".format("Help", "Show this message"))
    print("{}       {}".format("Print", "Print the tree traversals: In-order, Pre-order, Post-order"))
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

def getInteractiveInput(data):
    while True:
        try:
            if data == "remove":
                userInput = input("delete> ").strip()
            else:
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
        data = getInteractiveInput(None)
        showData(data)
        if treeType == "AVL":
            tree.build_from_sorted_array(data)
        else:
            for value in data:
                tree.insert(value)


    if sys.stdin.isatty(): # is at terminal
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
                    elements = getInteractiveInput(line)
                    for value in elements: # Obsługa usuwania więcej niż 1 elementu
                        tree.deleteValue(value)  
                elif line == "delete":
                    tree.delete() 
                elif line == "findminmax":
                    tree.findMinMax()
                elif line == "export":
                    print("\nEnter filename with txt extension (Pattern: tree.txt)")
                    while True:
                        filename = input("filename> ").strip()
                        if filename == "exit":
                            break
                        elif "." in filename and filename.split(".")[-1] == "txt":
                            tree.exportToTikz(filename)
                            break
                        print('Enter a valid filename (name.txt) or type "exit" to leave')
                elif line == "rebalance":
                    if treeType == "AVL":
                        print("AVL tree is always balanced")
                    else:
                        tree.rebalanceDsw()                   
                elif line == "exit":
                    print("Exiting...")
                    break
                else:
                    print(f"Unknown command: {line}")
            
            except EOFError: # End Of File Error
                print("\nExiting...")
                break
    else:
        print("\nProcessing input...")
        print("Done.")

if __name__ == "__main__":
    main()