class TreeNode:
    def __init__(self, score=None):
        self.score = score
        self.children = []
        self.parent = None
        self.size = 1 # number of leaves in the subtree
    
    def update_size(self, delta):
        self.size += delta
        if self.parent:
            self.parent.update_size(delta)

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)
        if len(self.children) > 1: # adding the first child to a node does not increase the leaf count
            self.update_size(1)
    
    def delete_child(self, child_node):
        if child_node in self.children:
            self.update_size(-child_node.size)
            self.children.remove(child_node)
            child_node.parent = None
        else:
            raise ValueError("Child node not found in children list")

    def subtree_to_list(self):
        result = []
        queue = [(self, [])]
        while queue:
            node, path = queue.pop(0)
            result.append((path, round(node.score, 2), node.size))
            for i, child in enumerate(node.children):
                new_path = path + [i]
                queue.append((child, new_path))
        return result[1:]
    
    def get_path(self, index, depth):
        if depth == 0:
            return self
        total = 0
        for child in self.children:
            if total + child.size >= index:
                if depth == 1:
                    return child
                else:
                    return child.get_path(index - total, depth - 1)
            total += child.size
        raise ValueError("Index or depth out of bounds")

class DynamicTree:
    def __init__(self, tree_choices=None, lr=0.1, default_score=0.5, split_thresh=1, max_degree=4):
        self.root = TreeNode(score=default_score)
        self.size = 1 # number of nodes in the tree
        if tree_choices:
            node_dict = {(): self.root}
            for node_path in tree_choices:
                parent_path = tuple(node_path[:-1])
                parent_node = node_dict[parent_path]
                child_node = TreeNode(score=default_score)
                parent_node.add_child(child_node)
                self.size += 1
                node_dict[tuple(node_path)] = child_node
        self.lr = lr
        self.split_thresh = split_thresh
        self.max_degree = max_degree
    
    def to_list(self):
        return [node for node, _, _ in self.root.subtree_to_list()]
    
    def print_tree(self, verbose=True):
        if verbose:
            print(self.root.subtree_to_list())
        else:
            print(self.to_list())
    
    def depth(self):
        return len(self.root.subtree_to_list()[-1][0])
    
    def num_leaves(self):
        return self.root.size
    
    def num_nodes(self):
        return self.size
    
    def dfs(self):
        result = []
        stack = [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            result.append((node, depth))
            for child in node.children:
                stack.append((child, depth + 1))
        return result
    
    def tree_decay(self, total_decay):
        # for every node, decay its score by total_decay / num_nodes
        queue = self.dfs()
        num_nodes = self.num_nodes()
        while queue:
            node, _ = queue.pop()
            node.score -= total_decay / num_nodes
            if node.score <= 0:
                # try to borrow score from its last children
                while node.score <= 0 and node.children:
                    last_child = node.children[-1]
                    node.score += last_child.score
                    last_child.score = 0
                    # node.delete_child(last_child)
                if node.score <= 0:
                    node.parent.delete_child(node)
                    self.size -= 1
    
    def reorder_children(self):
        # keep the leftmost branch the biggest (contains the most leaves)
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if node.children:
                node.children.sort(key=lambda x: x.size, reverse=True)
                queue.extend(node.children)
    
    # index starts from 1
    # depth of root is 0
    def visit_node(self, index, depth):
        try:
            node = self.root.get_path(index, depth)
        except ValueError:
            print("Got a very rare value error. Skipping...")
            return
        # increase the score of all nodes on the path to the root
        total_added_score = 0
        while node:
            if len(node.children) >= self.max_degree:
                node = node.parent
                continue
            rate = self.lr / (2 * len(node.children) + 1)
            node.score += rate
            total_added_score += rate
            # split the node if its score exceeds the threshold
            if node.score >= self.split_thresh:
                node.add_child(TreeNode(score=(node.score / 2)))
                self.size += 1
                node.score /= 2
            node = node.parent
        self.tree_decay(total_added_score)
        self.reorder_children()


# class DynamicTree:
#     def __init__(self, tree_choices=None, lr=0.05, default_score=0.5, split_thresh=1, max_degree=4):
#         self.root = TreeNode(score=default_score)
#         self.size = 1 # number of nodes in the tree
#         if tree_choices:
#             node_dict = {(): self.root}
#             for node_path in tree_choices:
#                 parent_path = tuple(node_path[:-1])
#                 parent_node = node_dict[parent_path]
#                 child_node = TreeNode(score=default_score)
#                 parent_node.add_child(child_node)
#                 self.size += 1
#                 node_dict[tuple(node_path)] = child_node
#         self.lr = lr
#         self.split_thresh = split_thresh
#         self.max_degree = max_degree
    
#     def to_list(self):
#         return [node for node, _, _ in self.root.subtree_to_list()]
    
#     def print_tree(self, verbose=True):
#         if verbose:
#             print(self.root.subtree_to_list())
#         else:
#             print(self.to_list())
    
#     def depth(self):
#         return len(self.root.subtree_to_list()[-1][0])
    
#     def num_leaves(self):
#         return self.root.size
    
#     def num_nodes(self):
#         return self.size
    
#     def leaf_decay(self, rate):
#         # for every leaf, decay its score by rate / num_leaves
#         queue = [self.root]
#         while queue:
#             node = queue.pop(0)
#             if not node.children:
#                 node.score -= rate / self.num_leaves()
#                 if node.score <= 0:
#                     node.parent.delete_child(node)
#                     self.size -= 1
#             else:
#                 queue.extend(node.children)
    
#     # index starts from 1
#     # depth of root is 0
#     def visit_node(self, index, depth):
#         try:
#             node = self.root.get_path(index, depth)
#         except ValueError:
#             print("Got a very rare value error. Skipping...")
#             return
#         if len(node.children) >= self.max_degree:
#             return
#         node.score += self.lr
#         if node.score >= self.split_thresh:
#             node.add_child(TreeNode(score=(node.score / 2)))
#             self.size += 1
#             node.score /= 2
#         self.leaf_decay(self.lr)