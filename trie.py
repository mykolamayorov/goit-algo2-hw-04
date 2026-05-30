class TrieNode:
    __slots__ = ("children", "is_end", "value", "subtree_words")

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None
        self.subtree_words = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def put(self, key, value=None):
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        node = self.root
        created_new_word = False
        path = [node]
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            path.append(node)
        if not node.is_end:
            node.is_end = True
            self.size += 1
            created_new_word = True
            for item in path:
                item.subtree_words += 1
        node.value = value
        return created_new_word

    def contains(self, key):
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        node = self.root
        for char in key:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end