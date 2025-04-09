import unittest
from BWT import BWT 

class TestBWTHardcoded(unittest.TestCase):

    def test_build_bwt_known_input(self):

        bwt_obj = BWT("abracadabra$", buildsufarray=True)
        self.assertEqual(bwt_obj.bwt, "ard$rcaaaabb")

    def test_inverse_bwt_from_known(self):

        bwt_obj = BWT("ard$rcaaaabb", encoded=True)
        self.assertEqual(bwt_obj.inverse_bwt(), "abracadabra$")


    def test_find_ith_occ_basic(self):
        # Lista simples com repetições
        bwt_obj = BWT()
        l = ['A', 'G', 'A', 'C', 'A']
        self.assertEqual(bwt_obj.find_ith_occ(l, 'A', 2), 2)
        self.assertEqual(bwt_obj.find_ith_occ(l, 'G', 1), 1)
        self.assertEqual(bwt_obj.find_ith_occ(l, 'C', 1), 3)
        self.assertEqual(bwt_obj.find_ith_occ(l, 'T', 1), -1)

    def test_last_to_first_hardcoded(self):
        bwt_obj = BWT("abracadabra$", buildsufarray=True)
        lf = bwt_obj.last_to_first()
        self.assertEqual(len(lf), len("ard$rcaaaabb"))
        self.assertTrue(all(0 <= i < len("ard$rcaaaabb") for i in lf))

    def test_bw_matching_present(self):
        # Procurar "abra" em "abracadabra$"
        bwt_obj = BWT("abracadabra$", buildsufarray=True)
        matches = bwt_obj.bw_matching("abra")
        self.assertTrue(isinstance(matches, list))
        self.assertGreater(len(matches), 0)

    def test_bw_matching_absent(self):
        # Procurar zzz 
        bwt_obj = BWT("abracadabra$", buildsufarray=True)
        self.assertEqual(bwt_obj.bw_matching("zzz"), [])

    def test_bw_matching_pos_example(self):
        bwt_obj = BWT("abracadabra$", buildsufarray=True)
        positions = bwt_obj.bw_matching_pos("abra")
        self.assertEqual(sorted(positions), [0, 7])

    def test_bw_matching_pos_not_found(self):
        # Padrão inexistente
        bwt_obj = BWT("abracadabra$", buildsufarray=True)
        positions = bwt_obj.bw_matching_pos("xyz")
        self.assertEqual(positions, [])

    def test_set_bwt_and_inverse_known(self):
        bwt_obj = BWT("s$nnaaa", encoded=True)
        self.assertEqual(bwt_obj.inverse_bwt(), "ananas$")

    def test_suffix_array_error_if_not_built(self):
        # Tentar usar bw_matching_pos sem buildsufarray
        bwt_obj = BWT("abracadabra$", buildsufarray=False)
        with self.assertRaises(ValueError):
            bwt_obj.bw_matching_pos("abra")

    def test_empty_sequence(self):
        # Testar sequência vazia
        bwt_obj = BWT("")
        self.assertEqual(bwt_obj.bwt, "")

    def test_bwt_only_dollar(self):
        # Testar string apenas com símbolo terminal
        bwt_obj = BWT("$", buildsufarray=True)
        self.assertEqual(bwt_obj.bwt, "$")
        self.assertEqual(bwt_obj.inverse_bwt(), "$")
        self.assertEqual(bwt_obj.bw_matching(""), [0])  # match vazio

    def test_show_bwt_matrix_runs(self):
        # Verifica se a função corre sem erro
        bwt_obj = BWT("abracadabra$", buildsufarray=True)
        try:
            bwt_obj.show_bwt_matrix()
        except Exception as e:
            self.fail(f"Erro ao mostrar matriz BWT: {e}")

if __name__ == "__main__":
    unittest.main()
