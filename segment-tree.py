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
        index (int):        The node's position inside of the array that stores the segment tree.
        null_value (int):   This is the value that is returned when the node is completely outside
                            of the query interval. When merged with another node, it should leave
                            the other node's value unchanged. For example, in this implementation
                            of segment tree, a merge is the sum of two nodes' values. Therefore, 
                            null_value should be zero in order to leave another node's value
                            unchanged in a merge. 
    """
    
    def __init__(self, value, start, end, index):
        """
        This constructor performs the initialization of the tree node. 
        
        Args:
            value (int):    The value the node should hold.
            start (int):    The starting index of the query interval of the node.
            end (int):      The ending index of the query interval of the node.
            index (int):    The position inside of the segment tree where the node
                            is located.
        """
        self.value = value
        self.start = start
        self.end = end
        self.index = index
        self.null_value = 0
    
    # These are the operators that should be implemented in order to
    # allow Python standard algorithms to operate on tree nodes. For example,
    # sorted() depends on the less-than operator. The most important operators
    # to implement are __add__ which dictates the bahavior of a node merge, and
    # __str__ which governs how a node is printed to output.
    
    def __add__(self, other):
        return self.value + other
    
    def __radd__(self, other):
        return self.value + other
    
    def __lt__(self, other):
        return self.value < other

    def ___le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other
    
    def __str__(self):
        return str(self.value)

class SegmentTree:
    """
    This class implements the data structure as well as the algorithms associated with
    segment trees. In general, this class should not be extended as it operates on
    generic SegmentNode objects. In order to change the behavior of a node merge, the
    addition operator of the SegmentNode class should be overridden at which time, all
    algorithms implemented in this class will function as intended. A merge function is
    supplied for the cases where a node merge may depend on contextual data outside
    of the SegmentNode object. In those cases, the merge function can be overridden.
    
    Attributes:
        data (list):    The input data on which queries will be executed.
        tree (list):    The data structure that contains the constructed
                        segment tree.
    """
    
    def __init__(self, data):
        """
        This constructor performs the initial construction of the segment tree. It first
        allocates enough memory to hold the tree structure, and then delegates to the 
        recursive build() function to perform tree construction.
        
        Args:
            data (list): The input data to build the tree from.
        """
        # The space complexity of a segment tree is O(2^log(n)). Use math.ceil() 
        # to round decimal logarithms up to the nearest integer. 
        self.tree = [None]*2*int(math.pow(2, math.ceil(math.log(len(data), 2))))
        self.data = data
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
            (SegmentNode):  The node object that is placed inside of the segment tree. In 
                            practicality, the function behaves as a void function, but the node
                            is returned for convenience in case it is appropriate for future use
                            cases.
        """
        if start == end:
            self.tree[current_index] = SegmentNode(self.data[start], start, end, current_index)
            return self.tree[current_index]
        else:
            midpoint = int((start+end)/2)
            self.tree[current_index] = SegmentNode(self.merge(self.build(start, midpoint, current_index*2+1),
                                                   self.build(midpoint+1, end, current_index*2+2)), start, end, current_index)
            return self.tree[current_index]        

    def query(self, node, start, end):
        """
        This recursive function executes a query on the original data set. The purpose of a 
        segment tree is to improve performance of queries over aribtrary sub-intervals of the
        original data set. For example, in this implementation, a query over a sub-interval 
        returns the sum of all values over that sub-interval. Another example is finiding the
        minimum value over an arbitrary sub-interval. 
        
        With a segment tree, queries are executed in O(log(n)) time since the nodes of a segment
        tree contain the answer to a query over its associated interval. The root node contains 
        the answer to a query over the entire data set. The root's left child contains the answer
        to a query over the first half of the data set. The root's right child contains the answer
        to a query over the second half of the data set. Etc. 
        
        The merge() function is what dictates the answer to a query. In this implementation, a query
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
        value should not be included in the query, and the node's null value is returned.
        
        Otherwise, the current node's interval has a partial overlap with the sub-interval, so 
        the function will recurse on the left and right children until complete overlap of 
        intervals is reached.
        
        Args:
            node(SegmentNode):  The node inside of the segment tree to query.
            start (int):        The starting index of the sub-interval of the data set.
            end (int):          The ending index of the sub-interval of the data set.
        """
        if start <= node.start and end >= node.end:
            return node.value
        elif node.end < start or node.start > end:
            return node.null_value
        else:
            return self.merge(self.query(self.tree[node.index*2+1], start, end),
                              self.query(self.tree[node.index*2+2], start, end))
    
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
        return left_node + right_node
    
    def update_interval(self, node, start, end, updates):
        """
        I'M NOT SURE THIS IS POSSIBLE.
        
        This recursive function performs an update to the segment tree when values in the data
        set change. If the indices of the value changes are not contiguous, each needs to be
        treated as its own sub-interval of contiguous indices. For example, if [1,4] and [5,8]
        are updated, the entire update can be treated as the contiguous interval of [1,8]. However,
        if the updates are over the intervals [1,4] and [6,8], then the update() function needs to be
        called separately for both intervals.
        
        Updates are made in the following manner:
        
        NOTE: 'start' and 'end' are the beginning and ending indices of the sub-interval of the data set.
        
        If the current node's interval lies completely outside the sub-interval, it doesn't need to 
        be updated.
        
        Otherwise, if there is only one update to make (start == end), update the current node's value
        with the updated value.
        
        Otherwise, 
        """
        pass
#        if node.end < start or node.start > end:
#            return
#        elif start == end:
#            node.value = updates[start]
#            return node
#        else:
#            midpoint = (start + end) / 2
#            node.value = self.merge(self.update(self.tree[node.index*2+1], start, midpoint, updates[start:midpoint]),
#                                    self.update(self.tree[node.index*2+2], midpoint+1, end, updates[midpoint+1:end]))
    
    def update(self, node, data_index, difference):
        """
        This function updates the segment tree when a single data point is updated
        from the input set. The 'difference' value should be calculated outside of this
        function. For each node that contains the data point inside of its interval, 
        the difference value is added to the node's value. This function works well for
        merges such as sums where the change to each node's value can be predicted without
        knowing the node's value first. For merges such as minimum value of sub-intervals
        that depend on knowing the node's value, the update_interval function should be used
        since it utilizes the merge() function to re-build sections of the tree.
        
        Args:
            node (SegmentNode): The node to apply the update to.
            data_index (int):   The index in the data set that was updated.
            difference (int):   The value to be added to each node's value. This type may change
                                with different types of SegmentNodes.
        Returns:
            SegmentNode:    The current node of the tree. In practicality, this is a void function,
                            but the node is returned as a convenience for future use cases
        """
        
        # If the data_index is not within the node's interval, then the node does not need
        # to be updated.
        if data_index < node.start or data_index > node.end:
            return
        else:
            node.value = node.value + difference
            if not node.start == node.end:
                self.update(self.tree[node.index*2+1], data_index, difference)
                self.update(self.tree[node.index*2+2], data_index, difference)
            return node
    
if __name__ == "__main__":
    data = [-1, 3, 4, 0, 2, 1]
    tree = SegmentTree(data)
    print(list(map(str, tree.tree)))
    print(str(tree.query(tree.tree[0], 1, 4)))
    print(str(tree.query(tree.tree[0], 1, 1)))
    tree.update(tree.tree[0], 3, -1)
    print(list(map(str, tree.tree)))