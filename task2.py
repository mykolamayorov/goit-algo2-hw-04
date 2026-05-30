from trie import Trie, TrieNode


class Homework(Trie):
    def __init__(self):
        super().__init__()
        self.reverse_root = TrieNode()

    def put(self, key, value=None):
        is_new = super().put(key, value)
        if is_new:
            node = self.reverse_root
            node.subtree_words += 1
            for char in reversed(key):
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.subtree_words += 1
            node.is_end = True
            node.value = value
        return is_new

    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        node = self.reverse_root
        if pattern == "":
            return node.subtree_words
        for char in reversed(pattern):
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.subtree_words

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        node = self.root
        if prefix == "":
            return self.size > 0
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.subtree_words > 0


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    assert trie.count_words_with_suffix("e") == 1
    assert trie.count_words_with_suffix("ion") == 1
    assert trie.count_words_with_suffix("a") == 1
    assert trie.count_words_with_suffix("at") == 1

    assert trie.has_prefix("app") is True
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True
    assert trie.has_prefix("ca") is True

    try:
        trie.count_words_with_suffix(None)
    except TypeError:
        pass
    else:
        raise AssertionError("TypeError was not raised for count_words_with_suffix")

    try:
        trie.has_prefix(123)
    except TypeError:
        pass
    else:
        raise AssertionError("TypeError was not raised for has_prefix")

    print("All tests passed")