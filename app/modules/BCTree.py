class BCTree:
    def __init__(self, root_node):
        self.root_node = root_node

    @staticmethod
    def __dfs_traversal(searcher, start_node):
        def __depth_traversal_recursive(node):
            node = node.first_child
            __check_siblings_recursive(node)

        def __check_siblings_recursive(node):
            searcher.compare(node)
            if searcher.search_done:
                return searcher.results

            if node is None:
                return

            if node.first_child is not None:
                __depth_traversal_recursive(node)

            node = node.right_sibling

            __check_siblings_recursive(node)

        searcher.compare(start_node)

        __depth_traversal_recursive(start_node)

        searcher.search_done = True
        return searcher.results

    @classmethod
    def get_descendants(cls, node):
        searcher = DescendantSearcher()

        return cls.__dfs_traversal(searcher, node)


class DescendantSearcher:
    def __init__(self):
        self.results = []
        self.search_done = False

    def compare(self, node):
        if node is not None:
            self.results.append(node.id)
