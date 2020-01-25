import ctypes

"""In Python garbage collector collect nodes and decrese reference count of the object
of node when the object of node is XORed, Python thinks there is no any way to access
the node so we used a list in which we store objects of node just for preventing to 
become garbage."""

class Node:
    def __init__(self, value):
        self.value = value
        self.npx = 0


class XorLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.__nodes = []

    def InsertAtStart(self, value):
        node = Node(value)
        if self.head is None: #If list is empty
            self.head = node
            self.tail = node
        else:
            self.head.npx = id(node) ^ self.head.npx
            node.npx = id(self.head)
            self.head = node
        self.__nodes.append(node)

    def InsertAtEnd(self, value):
        node = Node(value)
        if self.head is None: #If list is empty
            self.head = node
            self.tail = node
        else:
            self.tail.npx = id(node) ^ self.tail.npx
            node.npx = id(self.tail)
            self.tail = node
        self.__nodes.append(node)

    def DeleteAtStart(self):
        if self.isEmpty():#If list is empty
            return "List is empty !"
        elif self.head == self.tail: #If list has 1 node
            self.head=self.tail=None
        elif (0^self.head.npx) == id(self.tail): #If list has 2 nodes
            self.head=self.tail
            self.head.npx=self.tail.npx=0
        else: #If list has more than 2 nodes
            res=self.head.value
            x=self.__type_cast(0^self.head.npx) # Address of next node
            y=(id(self.head) ^ x.npx) # Address of next of next node
            self.head=x
            self.head.npx=0^y
            return res
        
    def DeleteAtEnd(self):
        if self.isEmpty(): #If list is empty
            return "List is empty !"
        elif self.head == self.tail: #If list has 1 node
            self.head=self.tail=None
        elif self.__type_cast(0^self.head.npx) == (self.tail): #If list has 2 nodes
            self.tail=self.head
            self.head.npx=self.tail.npx=0
        else: #If list has more than 2 nodes
            prev_id = 0
            node = self.head
            next_id=1
            while next_id:
                next_id = prev_id ^ node.npx
                if next_id:
                    prev_id = id(node)
                    node = self.__type_cast(next_id)
            res=node.value
            x=self.__type_cast(prev_id).npx^id(node)
            y=self.__type_cast(prev_id)
            y.npx=x^0
            self.tail=y
            return res

    def Print(self):

        """We are printing values rather than returning it bacause
        for returning we have to append all values in a list
        and it takes extra memory to save all values in a list."""

        if self.head != None:
            prev_id = 0
            node = self.head
            next_id = 1
            print(node.value)
            while next_id:
                next_id = prev_id ^ node.npx
                if next_id:
                    prev_id = id(node)
                    node = self.__type_cast(next_id)
                    print(node.value)
                else:
                    return
        else:
            print("List is empty !")
            
    def ReversePrint(self):

        #Print Values is reverse order.
        
        """We are printing values rather than returning it bacause
        for returning we have to append all values in a list
        and it takes extra memory to save all values in a list."""

        if self.head != None:
            prev_id = 0
            node = self.tail
            next_id = 1
            print(node.value)
            while next_id:
                next_id = prev_id ^ node.npx
                if next_id:
                    prev_id = id(node)
                    node = self.__type_cast(next_id)
                    print(node.value)
                else:
                    return
        else:
            print("List is empty !")

    def Length(self):
        if not self.isEmpty():
            prev_id = 0
            node = self.head
            next_id=1
            count=1
            while next_id:
                next_id = prev_id ^ node.npx
                if next_id:
                    prev_id = id(node)
                    node = self.__type_cast(next_id)
                    count+=1
                else:
                    return count
        else:
            return 0
        
    def PrintByIndex(self, index):
        prev_id = 0
        node = self.head
        for i in range(index):
            next_id = prev_id ^ node.npx

            if next_id:
                prev_id = id(node)
                node = self.__type_cast(next_id)
            else:
                return "Value dosn't found index out of range."
        return node.value
    
    def isEmpty(self):
        if self.head is None:
            return True
        return False


    def __type_cast(self,id):
        return ctypes.cast(id, ctypes.py_object).value

#Driver Code
a = XorLinkedList()
a.InsertAtEnd(2)
a.InsertAtEnd(3)
a.InsertAtEnd(4)
a.InsertAtStart(0)
a.InsertAtStart(6)
a.InsertAtEnd(55)
print("Print by index: ",a.PrintByIndex(2))
print("Length is:",a.Length())
print("Printing values:")
a.Print()
print("Printing values in reverse order:")
a.ReversePrint()
print("*****************")
print("Delete Last Node: ",a.DeleteAtEnd())
print("Delete First Node: ",a.DeleteAtStart())
print("*****************")
print("Length is:",a.Length())
print("Printing values:")
a.Print()
print("Printing values in reverse order:")
a.ReversePrint()