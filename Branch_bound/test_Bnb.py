import unittest

from Branch_bound import *


class TestBNB(unittest.TestCase) :

#Testa um caso que sabemos o resultao esperado 
    def test_bnb1(self):
        seqs = "ACTGACTAGTTATA ACTGCGATAGATTG AATGATCTAGTGCA CATGCTGCACTGCA".split()
        tam_seqs = len(seqs[0])
        num_seqs = len(seqs)
        tam_motif = 4

        self.assertEqual(branch_and_bound(seqs, num_seqs, tam_seqs, tam_motif), ([[0, 0, 0, 8], [0, 0, 8, 8]], 15))
    
    def test_bnb7(self):                    #no do prof tinha apenas um mas será que a função dele dá qpenas um resultado enquanto a nossa dá dois ???
        seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
        num_seqs = 3
        tam_seqs = 8
        tam_motif = 3

        self.assertEqual(branch_and_bound(seqs, num_seqs, tam_seqs, tam_motif), ([[3, 2, 2],[3,2,5]] , 8))


#Teste para seqs com len diferentes 
    def test_bnb2(self):
        seqs = "ACTGACTAGTTATA ACTGCGATAGATTG AATGATCTAGTGCA CATGCTGCACTGC".split() #apenas 1 de diferenca
        tam_seqs = len(seqs[0])
        num_seqs = len(seqs)
        tam_motif = 4

        with self.assertRaises(AssertionError):
            branch_and_bound(seqs, num_seqs, tam_seqs, tam_motif)

    def test_bnb3(self):
        seqs = "ACTGACTTA ACTTG AATGATCGCA CATGCTGCACTGC".split()   #tamanhos variados 
        tam_seqs = len(seqs[0])
        num_seqs = len(seqs)
        tam_motif = 4

        with self.assertRaises(AssertionError):
            branch_and_bound(seqs, num_seqs, tam_seqs, tam_motif)



#Teste para seqs com caracateres que não são bases de DNA 
    def test_bnb4(self):
        seqs = "ACTG ACT_ SADA *FHA".split() 
        tam_seqs = len(seqs[0])
        num_seqs = len(seqs)
        tam_motif = 4

        with self.assertRaises(ValueError):
            branch_and_bound(seqs, num_seqs, tam_seqs, tam_motif)

    def test_bnb5(self):
        seqs = "ACTGACTAGTTATA ACTGCGATAGATTG AATGATCTAGTGCA CATGCTGCACTG_A".split() #apenas um caracter de diferença
        tam_seqs = len(seqs[0])
        num_seqs = len(seqs)
        tam_motif = 4

        with self.assertRaises(ValueError):
            branch_and_bound(seqs, num_seqs, tam_seqs, tam_motif)


#Teste para ver se o input precisa ser maiuscula
    def test_bnb6(self):
        seqs = "ACTGACTAGTTATA ACTGCGATAGATTG AATGATCTAGTGCA CATGCTGCACTGCA".lower().split()
        tam_seqs = len(seqs[0])
        num_seqs = len(seqs)
        tam_motif = 4
        
        self.assertEqual(branch_and_bound(seqs, num_seqs, tam_seqs, tam_motif), ([[0, 0, 0, 8], [0, 0, 8, 8]], 15))


#Testes para a função score

    def test_empty_offsets(self):
        seqs = ["ACTG", "TGCA", "GATC", "CTAG"]
        offsets = []
        tam_motif = 4
        self.assertEqual(score(seqs, offsets, tam_motif), 0)

    def test_single_base_motif(self):
        seqs = ["ACTG", "TGCA", "GATC", "CTAG"]
        offsets = [0, 1, 2, 3]
        tam_motif = 1
        self.assertEqual(score(seqs, offsets, tam_motif), 2)

    def test_full_motif(self):
        seqs = ["ACTGACTAGTTATA", "ACTGCGATAGATTG", "AATGATCTAGTGCA", "CATGCTGCACTGCA"]
        offsets = [0, 1, 2, 3]
        tam_motif = 4
        self.assertEqual(score(seqs, offsets, tam_motif), 7)

if __name__ == '__main__':
    unittest.main()