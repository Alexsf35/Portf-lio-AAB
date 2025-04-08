import pprint

class SuffixTree:
    """
    A class that implements a suffix tree for efficiently storing and searching substrings 
    across multiple words. This structure supports the insertion of new words and allows 
    for fast pattern searches by returning the positions where a given substring appears.

    Attributes
    ----------
    tree : dict
        The root of the suffix tree, implemented as a nested dictionary.
    origem : list
        A list that stores the words inserted into the tree.
    """
    
    def __init__(self):
        """
        Initializes a new instance of the SuffixTree with an empty tree and an empty list 
        for storing inserted words.
        """
        self.tree = {}
        self.origem = []  # Stores the inserted words

    def inserir_palavra(self, palavra: str) -> None:
        """
        Inserts a word into the suffix tree by breaking it into all of its suffixes.
        Each suffix is added to the tree along with its originating word's index and the 
        offset where the suffix begins.

        Parameters
        ----------
        palavra : str
            The word to be inserted into the suffix tree.
        """
        index = len(self.origem)  # Determine the index for the new word
        self.origem.append(palavra)

        for offset in range(len(palavra)):
            sufixo = palavra[offset:]
            self.adicionar_sufixo(sufixo, index, offset)

    def adicionar_sufixo(self, sufixo: str, index: int, offset: int) -> None:
        """
        Adds a single suffix to the suffix tree, associating it with metadata that indicates
        the word's index and the starting position of the suffix within that word.

        Parameters
        ----------
        sufixo : str
            The suffix to be added to the tree.
        index : int
            The index of the word from which the suffix originates.
        offset : int
            The starting offset of the suffix in the word.
        """
        nodulo = self.tree
        for letra in sufixo + "$":
            if letra not in nodulo:
                nodulo[letra] = {}
            nodulo = nodulo[letra]

        # Mark the end of the suffix with its metadata (word index, offset)
        nodulo['$'] = (index, offset)

    def encontra_padrao(self, padrao: str) -> list[tuple[int, int]]:
        """
        Searches the suffix tree for the specified pattern and returns a list of tuples
        indicating where the pattern occurs. Each tuple contains the index of the word and 
        the offset at which the pattern starts.

        Parameters
        ----------
        padrao : str
            The substring pattern to search for in the suffix tree.

        Returns
        -------
        list of tuple[int, int]
            A list of tuples where each tuple is (word_index, offset) indicating an occurrence 
            of the pattern.
        """
        nodulo = self.tree
        for letra in padrao:
            if letra not in nodulo:
                return []  # Pattern not found
            nodulo = nodulo[letra]

        return self._coleta_ocorrencias(nodulo)

    def _coleta_ocorrencias(self, nodulo: dict) -> list[tuple[int, int]]:
        """
        Recursively traverses the subtree from the current node to collect all occurrences 
        of a pattern. Occurrences are identified by the '$' marker and contain metadata about 
        the word index and offset.

        Parameters
        ----------
        nodulo : dict
            The current node in the tree from which to collect occurrence metadata.

        Returns
        -------
        list of tuple[int, int]
            A list of tuples containing the (word_index, offset) for each occurrence found.
        """
        resultados = []
        for chave, valor in nodulo.items():
            if chave == '$':
                resultados.append(valor)
            else:
                resultados.extend(self._coleta_ocorrencias(valor))
        return resultados

    def obter_estrutura(self) -> dict:
        """
        Returns the complete structure of the suffix tree as a nested dictionary.

        Returns
        -------
        dict
            The nested dictionary representing the suffix tree.
        """
        return self.tree


# Example usage:
t = SuffixTree()
t.inserir_palavra("banana")
t.inserir_palavra("bandana")
pprint.pprint(t.obter_estrutura())
print(t.encontra_padrao("ana"))
print(t.encontra_padrao("ban"))
