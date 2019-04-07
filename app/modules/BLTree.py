class BLTree:
    def __init__(self, root_node):
        self.root_node = root_node

    def dfs_traversal(self):

        def __depth_traversal_recursive(node):
            nonlocal current_node
            current_node = node.first_child
            __check_siblings_recursive(current_node)

        def __check_siblings_recursive(node):
            if node is not None:
                print(node.name, node.id)

            if node is None:
                return

            if node.first_child is not None:
                __depth_traversal_recursive(node)

            node = node.right_sibling

            __check_siblings_recursive(node)

        current_node = self.root_node

        print(current_node.name, current_node.id)

        __depth_traversal_recursive(current_node)

        return
