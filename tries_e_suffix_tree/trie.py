from pprint import pformat

class Trie:
    """
    A class that implements a prefix tree (Trie) for efficient storage and retrieval of words.
    The Trie is built from a list of words, allowing fast word insertion, lookup, and deletion.
    
    Attributes
    ----------
    trie : dict
        The underlying nested dictionary that represents the Trie structure.
    """

    def __init__(self, palavras: list[str]) -> None:
        """
        Initializes the Trie with a list of words. Each word is inserted into the Trie upon initialization.
        
        Parameters
        ----------
        palavras : list of str
            A list of words to be stored in the Trie.
        """
        self.trie = {}
        for palavra in palavras:
            self.inserir(palavra)
    
    def inserir(self, palavra: str) -> None:
        """
        Inserts a single word into the Trie by creating a chain of nodes corresponding to each character.
        A special end-of-word marker ('$') is added at the end of the word.
        
        Parameters
        ----------
        palavra : str
            The word to be inserted into the Trie.
        """
        nodulo = self.trie
        for letra in palavra:
            if letra not in nodulo:
                nodulo[letra] = {}
            nodulo = nodulo[letra]
        # Insert the end-of-word marker
        nodulo['$'] = {}
        
    def procurar(self, palavra: str) -> bool:
        """
        Searches for an exact word in the Trie.
        It traverses the Trie following the sequence of characters in the word and verifies the presence
        of the end-of-word marker to confirm that the full word exists.
        
        Parameters
        ----------
        palavra : str
            The word to search for.
        
        Returns
        -------
        bool
            True if the word is found in the Trie; otherwise, False.
        """
        nodulo = self.trie
        for letra in palavra:
            if letra in nodulo:
                nodulo = nodulo[letra]
            else:
                return False
        return '$' in nodulo
    
    def _apagar_recursivo(self, nodulo: dict, palavra: str, idx: int) -> bool:
        """
        Recursively deletes a word from the Trie by traversing the Trie along the characters of the word.
        When the end of the word is reached, the end-of-word marker is removed.
        If a node becomes empty as a result, it is pruned from the Trie.
        
        Parameters
        ----------
        nodulo : dict
            The current node in the Trie.
        palavra : str
            The word to be deleted.
        idx : int
            The current index in the word being processed.
        
        Returns
        -------
        bool
            True if the current node becomes empty after deletion (allowing it to be removed), else False.
        """
        if idx == len(palavra):
            if '$' in nodulo:
                del nodulo['$']
                return len(nodulo) == 0  # Node can be removed if it is empty
            else:
                return False  # Word not found
        
        letra = palavra[idx]
        if letra not in nodulo:
            return False  # Word not found
        
        # Recursively attempt to delete in the next node
        limpar = self._apagar_recursivo(nodulo[letra], palavra, idx + 1)
        if limpar:
            del nodulo[letra]
            return len(nodulo) == 0
        return False
    
    def apagar_palavra(self, palavra: str) -> bool:
        """
        Deletes a specific word from the Trie.
        
        Parameters
        ----------
        palavra : str
            The word to be removed.
        
        Returns
        -------
        bool
            True if the word was successfully deleted, otherwise False.
        """
        return self._apagar_recursivo(self.trie, palavra, 0)

    def __str__(self):
        """
        Returns a pretty-formatted string representation of the Trie.
        
        Returns
        -------
        str
            A formatted string showing the structure of the Trie.
        """
        return pformat(self.trie)


# Example usage:
if __name__ == "__main__":
    t = Trie("casa casal casco casta".split())
    print(t)
    print(t.procurar('casa'))
    t.apagar_palavra('casta')
    print(t.procurar('casta'))
