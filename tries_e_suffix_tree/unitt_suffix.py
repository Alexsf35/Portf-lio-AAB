from suffix_tree import *
import unittest

class TestSuffixTree(unittest.TestCase):

    def setUp(self):
        # Este método é executado antes de cada teste.
        # Inicializamos a árvore com duas palavras conhecidas para testar os padrões depois.
        self.st = SuffixTree()
        self.st.inserir_palavra("banana")
        self.st.inserir_palavra("bandana")

    def test_inserir_palavra(self):
        # Verifica se as palavras foram armazenadas corretamente
        self.assertEqual(self.st.origem[0], "banana")
        self.assertEqual(self.st.origem[1], "bandana")

        # A árvore deve conter os sufixos terminados com '$'
        estrutura = self.st.obter_estrutura()
        self.assertIn('b', estrutura)  # A raiz deve conter a letra inicial de ambas as palavras

    def test_encontra_padrao_existente(self):
        # Testa padrões que devem existir nas palavras inseridas

        resultados = self.st.encontra_padrao("ana")
        # 'ana' aparece em 'banana' (duas vezes) e 'bandana' (uma vez)
        esperados = [{'$': (0, 1)}, {'$': (0, 3)}, {'$':(1, 4)}]
        self.assertCountEqual(resultados, esperados)


        resultados = self.st.encontra_padrao("ban")
        # 'ban' aparece no início de ambas as palavras
        esperados = [{'$': (0, 0)},  {'$': (1, 0)}]
        self.assertCountEqual(resultados, esperados)

    def test_encontra_padrao_inexistente(self):
        # Testa padrões que não existem nas palavras
        self.assertEqual(self.st.encontra_padrao("xyz"), [])
        self.assertEqual(self.st.encontra_padrao("naan"), [])
        self.assertEqual(self.st.encontra_padrao("091"), [])

    def test_encontra_padrao_no_fim(self):
        # Testa se um padrão no fim da palavra é identificado corretamente
        resultados = self.st.encontra_padrao("a")
        # 'a' aparece várias vezes nas duas palavras
        esperados = [{'$': (0, 1)}, {'$': (0, 3)}, {'$': (0, 5)}, {'$': (1, 1)}, {'$': (1, 4)}, {'$': (1, 6)}]

        self.assertCountEqual(resultados, esperados)

    def test_estrutura_completa(self):
        # Testa se a estrutura interna é um dicionário com a formatação esperada
        estrutura = self.st.obter_estrutura()
        self.assertIsInstance(estrutura, dict)


if __name__ == '__main__':
    unittest.main()
