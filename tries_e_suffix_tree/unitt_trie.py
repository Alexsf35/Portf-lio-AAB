from trie import *  
import unittest
from pprint import pformat

class TestTrie(unittest.TestCase):

    def setUp(self):
        self.words = ['casa', 'casal', 'casco', 'casta']
        self.trie = Trie(self.words)

    def test_inserir(self):
        # Testa se a inserção de uma nova palavra funciona corretamente.
        self.trie.inserir('casinha')  # Insere 'casinha' na Trie
        self.assertTrue(self.trie.procurar('casinha'))  # Deve encontrar a palavra completa
        self.assertFalse(self.trie.procurar('casinh'))  # Não deve encontrar o prefixo sem o marcador de fim ('$')

    def test_procurar_existente(self):
        # Testa se todas as palavras originais realmente existem na Trie
        for word in self.words:
            self.assertTrue(self.trie.procurar(word), f"Expected '{word}' to be found in trie")

    def test_procurar_inexistente(self):
        # Testa palavras que não estão na Trie
        self.assertFalse(self.trie.procurar('cas'), "Prefix 'cas' should not be considered a full word")
        self.assertFalse(self.trie.procurar('cascata'))  # Palavra completamente nova
        self.assertFalse(self.trie.procurar('casamento'))  # Outra palavra nova com prefixo similar

    def test_apagar_palavra(self):
        # Testa a exclusão de uma palavra existente da Trie
        self.assertTrue(self.trie.apagar_palavra('casta'))  # Deve retornar True porque 'casta' está presente
        self.assertFalse(self.trie.procurar('casta'))  # Após exclusão, 'casta' não deve mais existir

        # Confirma que outras palavras semelhantes **ainda existem**
        self.assertTrue(self.trie.procurar('casa'))
        self.assertTrue(self.trie.procurar('casal'))

    def test_apagar_inexistente(self):
        # Testa a exclusão de uma palavra que **não** está na Trie
        self.assertFalse(self.trie.apagar_palavra('cachorro'))  # Deve retornar False porque 'cachorro' não foi inserida

        # Confirma que nenhuma palavra existente foi afetada
        for word in self.words:
            self.assertTrue(self.trie.procurar(word))

    def test_trie_string_representation(self):
        # Testa se o método __str__ da Trie retorna uma string formatada corretamente
        trie_str = str(self.trie)
        self.assertIsInstance(trie_str, str)  # Deve ser uma string
        self.assertIn("'c'", trie_str)  # O primeiro nível da Trie deve conter a letra 'c'
        self.assertIn("'a'", trie_str)  # O segundo nível (filho de 'c') deve conter 'a'

if __name__ == '__main__':
    # Executa todos os testes quando o script for rodado diretamente
    unittest.main()
