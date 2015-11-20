import math

class SegmentNode:
    """
    This class represents a node within the segment tree. The SegmentTree class
    operates on these SegmentNode objects. In order to extend the SegmentTree class's
    functionality to solve different types of data queries, the operators in this class
    should be overridden to supply the appropriate functionality. For example, when extending
    this class, the addition operator is used to represent a merge of two SegmentNode objects,
    so it should be overridden to preserve the algorithm functionality in SegmentTree. 
    
    Attributes:
        value (int):        The value represented by this tree node. This type may change
                            in subclasses.
        start (int):        The starting index of the interval associated with this node.
        end (int):          The ending index of the interval associated with this node.
    """
    
    def __init__(self, value, start, end):
        """
        This constructor performs the initialization of the tree node. 
        
        Args:
            value (int):    The value the node should hold.
            start (int):    The starting index of the query interval of the node.
            end (int):      The ending index of the query interval of the node.
        """
        self.value = value
        self.start = start
        self.end = end
    
    # These are the operators that should be implemented in order to
    # allow Python standard algorithms to operate on tree nodes. For example,
    # sorted() depends on the less-than operator. The most important operators
    # to implement are __add__ which dictates the bahavior of a node merge, and
    # __str__ which governs how a node is printed to output.
    
    def __add__(self, other):
        if other is None:
            return self
        
        if self.start < other.start:
            start = self.start
        else:
            start = other.start
            
        if self.end > other.end:
            end = self.end
        else:
            end = other.end
            
        value = self.value + other.value
        return SegmentNode(value, start, end)
    
    def __radd__(self, other):
        return self + other
    
    def __lt__(self, other):
        return self.value < other.value

    def ___le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value
    
    def __str__(self):
        return "\n".join(["Node","____","Value: ",str(self.value),"Start: ",str(self.start),"End: "+str(self.end)])

class SegmentTree:
    """
    This class implements the data structure as well as the algorithms associated with
    segment trees. In general, this class should not be extended as it operates on
    generic SegmentNode objects. In order to change the behavior of a node merge, the
    addition operator of the SegmentNode class should be overridden, at which time, all
    algorithms implemented in this class will function as intended. A merge function is
    supplied for the cases where a node merge may depend on contextual data outside
    of the SegmentNode object. In those cases, the merge function can be overridden.
    
    Attributes:
        data (list):            The input data on which queries will be executed.
        tree (list):            The data structure that contains the constructed
                                segment tree.
        node_type (function):   A reference to a SegmentNode constructor. This allows
                                different SegmentNode subclasses to be used with SegmentTree
    """
    
    def __init__(self, data, node_type):
        """
        This constructor performs the initial construction of the segment tree. It first
        allocates enough memory to hold the tree structure, and then delegates to the 
        recursive build() function to perform tree construction.
        
        Args:
            data (list):            The input data to build the tree from.
            node_type (function):   A reference to the SegmentNode constructor. This
                                    allows SegmentTree to operate on any subclass of
                                    SegmentNode.
        """
        # The space complexity of a segment tree is O(2^log(n)). Use math.ceil() 
        # to round decimal logarithms up to the nearest integer. 
        self.tree = [None]*2*int(math.pow(2, math.ceil(math.log(len(data), 2)))) #Check this math
        self.data = data
        self.node_type = node_type
        # The build function takes three parameters: the start and end indices of the 
        # interval, and the tree index of the next node to build. Since this is the
        # initialization, we are building the root node which contains the entire
        # data set as its interval, and the root node is always located at position zero.
        self.build(0, len(data)-1, 0)
    
    def build(self, start, end, current_index):
        """
        This recursive function contructs the nodes of the segment tree in the following manner:
        
        NOTE: 'start' and 'end' refer to the interval of the input data from which to construct a node.
        For example, the root node contains a merge of the entire input data set, so 'start' is zero,
        and 'end' is the length of the data set minus one (since it represents an index). The root node's
        left child is a merge on the first half of the input data, so 'start' is zero, and 'end' is the
        middle index of the data ((start + end) / 2).
        
        If the interval associated with the node only contains one data element (start == end), then
        the node is a leaf of the tree, so a new SegmentNode object should be created with that
        data value. 
        
        Otherwise, the data set needs to be split into two in order to recurse. The midpoint is
        calculated by taking the average of 'start' and 'end' to determine the index of the 
        input data that lies in the middle of 'start' and 'end'. Then, the current node is built
        by merging its left and right children, which are created via recursive build() calls. The
        left child is built using the interval from 'start' to 'midpoint', and the right child is
        built using the interval from 'midpoint+1' to 'end'.
        
        When segment trees are implemented using array (as is the case here), the left child
        of a node is located at index 2i+1, and the right child is located at index 2i+2 where
        i is the index of the node itself. This is identical behavior to standard binary trees.
        
        Args:
            start (int):            The starting index of the interval over the input data set.
            end (int):              The ending index of the interval over the input data set.
            current_index (int):    The location inside of the segment tree to place the node.
            
        Returns:
            (SegmentNode):  The node object that is placed inside of the segment tree.
        """
        if start == end:
            self.tree[current_index] = self.node_type(self.data[start], start, end)
            return self.tree[current_index]
        else:
            midpoint = int((start+end)/2)
            self.tree[current_index] = self.merge(self.build(start, midpoint, current_index*2+1),
                                                  self.build(midpoint+1, end, current_index*2+2))
            return self.tree[current_index]        

    def query(self, current_index, start, end):
        """
        This recursive function executes a query on the original data set. The purpose of a 
        segment tree is to improve performance of queries over aribtrary sub-intervals of the
        original data set. For example, in the default implementation, a query over a sub-interval 
        returns the sum of all values over that sub-interval. Another example is finiding the
        minimum value over an arbitrary sub-interval. 
        
        With a segment tree, queries are executed in O(log(n)) time since the nodes of a segment
        tree contain the answer to a query over its associated interval. The root node contains 
        the answer to a query over the entire data set. The root's left child contains the answer
        to a query over the first half of the data set. The root's right child contains the answer
        to a query over the second half of the data set. Etc. 
        
        The merge() function is what dictates the answer to a query. In the default SegmentNode, a query
        is the sum of a sub-interval, so the merge function adds two nodes' values together. If the
        query were to determine the minimum value of a sub-interval, the merge function would take
        the lesser of the two node values. For different types of queries, different types of SegmentNode
        objects should be used to build the tree. If two types of queries need to be answered, two instances
        of SegmentTree should be created. One should contain a SegmentNode type that represents a merge to
        answer query type A, and the other should contain a different SegmentNode type that represents a merge
        to answer query type B.
        
        Queries are answered in the following manner:
        
        NOTE: 'start' and 'end' are the beginning and ending indices of the sub-interval of the data set.
        
        If the indices of the sub-interval completely overlap the interval of the current node, then
        that node's value should be returned since it contains the answer for at least part of 
        the sub-interval (the other parts would be added as the values propogate up the recursive call
        stack). 
        
        Otherwise, if the sub-interval lies completely outside the node's interval, then the node's
        value should not be included in the query, and the a null value is returned.
        
        Otherwise, the current node's interval has a partial overlap with the sub-interval, so 
        the function will recurse on the left and right children until complete overlap of 
        intervals is reached.
        
        Args:
            start (int):         The starting index of the sub-interval of the data set.
            end (int):           The ending index of the sub-interval of the data set.
            current_index (int): The node's position inside of the tree array.
        """
        node = self.tree[current_index]
        if start <= node.start and end >= node.end:
            return node
        elif node.end < start or node.start > end:
            return None
        else:
            return self.merge(self.query(current_index*2+1, start, end),
                              self.query(current_index*2+2, start, end))
    
    def merge(self, left_node, right_node):
        """
        This function represents the combination of two nodes. The answer to a query is determined
        by the behavior of this function as it dictates the values of the nodes inside of the tree.
        In most cases, this function shouldn't need to be overwritten because the combination of
        two nodes can most often be represented by node addition, which is implemented by the addition
        operator inside of SegmentNode. Overriding this function is appropriate in cases where a merge
        of two nodes relies on contextual data stored outside of the segment tree.
        
        Args:
            left_node (SegmentNode):    The first node to merge. left_node would win any ties with right_node
            right_node (SegmentNode):   The second node to merge.
        """
#        print("Left Node is: "+str(left_node)+"\n")
#        print("Right Node is: "+str(right_node)+"\n\n")
#        if left_node is not None and right_node is None:
#            return left_node
#        elif left_node is None and right_node is not None:
#            return right_node
#        else:
        return left_node + right_node
    

    def update(self, current_index, start, end, functor, *args):
        """
        This function updates the segment tree when a range of indices in the data set
        should be updated. The actual update to perform is governed by the functor. When
        using SegmentTree, a function should be implemented and passed into the functor 
        parameter that will perform that actual update of the node. It could be as simple
        as incrementing the node's value, or it could be more complicated if the node's
        value is itself an object. 
        
        The way the tree is updated is as follows. It is very similar to the build function:
        
        If the node's interval is completely outside of the query interval, then no update
        needs to be performed, and the node is returned un-modified.
        
        Otherwise, if start == end, the node is a leaf node, and its value should be updated
        by running functor on the node. 
        
        Otherwise, recurse on the left and right children, which will propagate down to 
        the leaves, and then re-build the relevant nodes as it comes back up the
        recursion stack.
        
        This algorithm works well when the update is something relative to the current
        values of the nodes. E.g. subtract three from each value in between i and j where
        i and j represent a sub-interval of the original data set.
        
        Args:
            current_index (int): The node's position inside the tree array.
            start (int):         The starting index of the subset.
            end (int):           The ending index of the sebset.
            functor (function):  The function to run on the node to modify the value.
            args (placeholder):  This is a placeholder for the arguments to the functor.
        Returns:
            SegmentNode:    The current node of the tree. In practicality, this is a void function,
                            but the node is returned as a convenience for future use cases
        """
        node = self.tree[current_index]
        if end < node.start or start > node.end:
            return node
        elif start == end:
            # Test this to make sure it actually changes the tree index
            node = functor(node, args)
            return node
        else:
            midpoint = int((start+end)/2)
            node = self.merge(self.update(current_index*2+1, start, midpoint, functor),
                              self.update(current_index*2+2, midpoint+1, end, functor))
            return node
    
if __name__ == "__main__":
    data = [-1, 3, 4, 0, 2, 1]
    tree = SegmentTree(data, SegmentNode)
#    print(list(map(str, tree.tree)))
    print(str(tree.query(0, 1, 4)))
    print(str(tree.query(0, 1, 1)))
    tree.update(tree.tree[0], 3, -1)
    print(list(map(str, tree.tree)))