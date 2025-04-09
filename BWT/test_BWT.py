import unittest
from BWT import BWT 

class TestBWT(unittest.TestCase):

    def setUp(self):
        self.seq = "TAGACAGAGA$"
        self.bwt_obj = BWT(self.seq, buildsufarray=True)
        self.bwt_result = "AGGGTCAAAA$"

    def test_build_bwt(self):
        self.assertEqual(self.bwt_obj.bwt, self.bwt_result)

    def test_inverse_bwt(self):
        # Testa se a sequência original pode ser reconstruída corretamente
        recovered = self.bwt_obj.inverse_bwt()
        self.assertEqual(recovered, self.seq)

    def test_get_first_col(self):
         # Testa se a primeira coluna da matriz BWT está correta
        first_col = self.bwt_obj.get_first_col()
        expected = sorted(self.bwt_result)
        self.assertEqual(first_col, expected)

    def test_find_ith_occ(self):
        # Testa a função que encontra a i-ésima ocorrência de um símbolo numa lista
        sample_list = ['A', 'C', 'A', 'A', 'G', 'A']
        self.assertEqual(self.bwt_obj.find_ith_occ(sample_list, 'A', 2), 2)
        self.assertEqual(self.bwt_obj.find_ith_occ(sample_list, 'G', 1), 4)
        self.assertEqual(self.bwt_obj.find_ith_occ(sample_list, 'T', 1), -1)

    def test_last_to_first(self):
        # Testa o mapeamento da última coluna para a primeira
        lf = self.bwt_obj.last_to_first()
        self.assertIsInstance(lf, list)
        self.assertEqual(len(lf), len(self.bwt_result))
        # Check if mapping values are within expected bounds
        for idx in lf:
            self.assertTrue(0 <= idx < len(self.bwt_result))

    def test_bw_matching(self):
         # Testa se a procura do padrão 'AGA' na BWT devolve os índices corretos
        matches = self.bwt_obj.bw_matching("AGA")
        self.assertIsInstance(matches, list)
        self.assertTrue(all(isinstance(i, int) for i in matches))

    def test_bw_matching_pos(self):
        # Testa se as posições dos padrões encontrados na sequência original estão corretas
        pattern = "AGA"
        matches = self.bwt_obj.bw_matching_pos(pattern)
        # Check positions from suffix array
        expected_positions = []
        for i in range(len(self.seq)):
            if self.seq[i:].startswith(pattern):
                expected_positions.append(i)
        self.assertEqual(matches, sorted(expected_positions))

    def test_set_bwt_and_reconstruct(self):
         # Testa se ao definir manualmente uma BWT é possível reconstruir a sequência original
        new_bwt_obj = BWT("", buildsufarray=False)
        new_bwt_obj.set_bwt(self.bwt_result)
        result = new_bwt_obj.inverse_bwt()
        self.assertEqual(result, self.seq)


if __name__ == "__main__":
    unittest.main()
