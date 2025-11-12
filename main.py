import math, queue
from collections import Counter

####### Problem 1 #######

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return(dict(C.most_common()))
# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))
    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        # TODO
        x=p.get()
        y=p.get()
        z=TreeNode(data=(x.data[0]+y.data[0],""))
        ## Enforcing rightest tree or heap not compulsary step
        if(x.children() == (None,None) and y.children() == (None,None)):
            z.left,z.right=x,y 
        else:
            if(x.children()!= (None,None)):
                z.left,z.right=y,x 
            elif(y.children()!= (None,None)):
                z.left,z.right=x,y 
        p.put(z)
    # return root of the tree
    return p.get()        
# perform a traversal on the prefix code tree to collect all encodings
def get_code(node, prefix="", code={}):
    # TODO - perform a tree traversal and collect encodings for leaves in code
    ## Base Case
    if(node.left == None and node.right == None):
        charecter=node.data[1]
        code[charecter]=prefix
    else:
        ## Checking for data nodes on left branch
        if node.left:
            get_code(node.left,prefix+'0',code)
        ## Checking for data nodes on right branch
        if node.right:
            get_code(node.right,prefix+'1',code)
    return code
# given an alphabet and frequencies, compute the cost of a fixed length encoding
def fixed_length_cost(f):
    TF=0
    f1=math.ceil(math.log2(len(f)))
    for i in f.keys():
        TF+=f[i]
    return f1*TF    

# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
    # TODO
    Sum=0
    for i in C.keys():
        Sum+=(len(C[i])*f[i])
    return Sum


f = get_frequencies('fields.c')
print("Fixed-length cost:  %d" % fixed_length_cost(f))
T = make_huffman_tree(f)
C = get_code(T)
print("Huffman cost:  %d" % huffman_cost(C, f))
print("Huffman cost vs Fixed Encoding cost:  %f" % (huffman_cost(C, f)/fixed_length_cost(f)))


