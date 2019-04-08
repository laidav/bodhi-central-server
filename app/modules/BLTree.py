class BLTree:
    def __init__(self, root_node):
        self.root_node = root_node

    def dfs_traversal(self, searcher):
        def __depth_traversal_recursive(node):
            nonlocal current_node
            current_node = node.first_child
            __check_siblings_recursive(current_node)

        def __check_siblings_recursive(node):
            searcher.compare(node)
            if searcher.search_done:
                return searcher

            if node is None:
                return

            if node.first_child is not None:
                __depth_traversal_recursive(node)

            node = node.right_sibling

            __check_siblings_recursive(node)

        current_node = self.root_node

        searcher.compare(current_node)

        __depth_traversal_recursive(current_node)

        searcher.search_done = True
        return searcher


class BLTreeSearcher:
    def __init__(self, results):
        self.results = results
        self.search_done = False


class DescendantSearcher(BLTreeSearcher):
    def __init__(self):
        BLTreeSearcher.__init__(self, [])

    def compare(self, node):
        if node is not None:
            self.results.append(node)
