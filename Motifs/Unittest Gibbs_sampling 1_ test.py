import unittest
import random
from Gibbs_sampling import (pos_init, choose_seq, matriz_oc, pwm, consenso, prob_p, normalize_probabilities, roulette_wheel, gibbs_sampler)

class TestMotifSelection(unittest.TestCase):
    def setUp(self):
        '''
        Configuração inicial dos dados de teste.
        Define as sequências de DNA e o tamanho do motif para serem usados em todos os testes.
        '''
        self.seqs = [
            "GTAAACAATATTTATAGC",
            "AAAATTTACCTCGCAAGG", 
            "CCGTACTGTCAAGCGTGG",
            "TGAGTAAACGACGTCCCA", 
            "TACTTAACACCCTGTCAA"
        ]
        self.tam_motif = 8  #Tamanho fixo do motif para os testes

    def test_pos_init(self):
        '''
        Teste para a função pos_init (posições iniciais).
        Verifica se:
        1. O número de posições geradas corresponde ao número de sequências
        2. Cada posição está dentro dos limites válidos da sequência
        '''
        #Chama a função para gerar posições iniciais
        posicoes = pos_init(self.seqs, self.tam_motif)
        
        #Verifica se o número de posições é igual ao número de sequências
        self.assertEqual(len(posicoes), len(self.seqs))
        
        #Verifica se cada posição está dentro dos limites da sequência correspondente
        for seq, pos in zip(self.seqs, posicoes):
            #Posição deve ser maior ou igual a 0 e menor ou igual ao comprimento da sequência menos o tamanho do motif
            self.assertTrue(0 <= pos <= len(seq) - self.tam_motif)

    def test_choose_seq(self):
        '''
        Teste para a função choose_seq (escolha de sequência).
        Verifica se:
        1. A sequência escolhida pertence à lista original
        2. Uma sequência é removida corretamente
        3. O número de posições e motifs corresponde ao número de sequências restantes
        '''
        #Gera posições iniciais
        posicoes = pos_init(self.seqs, self.tam_motif)
        
        #Chama a função para escolher uma sequência
        chosen_seq, seqs2, motifs, random_index = choose_seq(self.seqs, posicoes, self.tam_motif)
        
        #Verifica se a sequência escolhida está na lista original
        self.assertIn(chosen_seq, self.seqs)
        
        #Verifica se o número de sequências restantes diminuiu
        self.assertEqual(len(seqs2), len(self.seqs) - 1)
    
        

    def test_matriz_oc(self):
        '''
        Teste para a função matriz_oc (matriz de ocorrências).
        Verifica se:
        1. A matriz contém todos os nucleotídeos
        2. Cada nucleotídeo tem valores para todas as posições do motif
        '''
        #Escolhe uma sequência e gera motifs
        _, seqs2, motifs, random_index = choose_seq(self.seqs, pos_init(self.seqs, self.tam_motif), self.tam_motif)
        
        #Cria matriz de ocorrências com pseudocontagem
        matriz = matriz_oc(motifs, pseudocont=0.5) # 0.5 é o valor padrão para pseudocont, se estiver a influenciar os resultados podemos mudar o valor para 0.1
        
        #Verifica se a matriz contém todos os nucleotídeos
        self.assertEqual(set(matriz.keys()), {'A', 'C', 'G', 'T'})
        
        #Verifica se cada nucleotídeo tem valores para todas as posições
        for values in matriz.values():
            self.assertEqual(len(values), self.tam_motif)

    def test_pwm(self):
        '''
        Teste para a função pwm (Position Weight Matrix).
        Verifica se:
        1. A matriz contém todos os nucleotídeos
        2. Cada nucleotídeo tem valores para todas as posições do motif
        '''
        #Escolhe uma sequência e gera motifs
        _, seqs2, motifs, random_index = choose_seq(self.seqs, pos_init(self.seqs, self.tam_motif), self.tam_motif)
        
        #Cria matriz de ocorrências
        matriz = matriz_oc(motifs, pseudocont=0.5) #mais uma vez 0.5.. se bla bla bla 0.1
        
        #Gera matriz de probabilidades
        pwm_matrix = pwm(matriz)
        
        #Verifica se a matriz contém todos os nucleotídeos
        self.assertEqual(set(pwm_matrix.keys()), {'A', 'C', 'G', 'T'})
        
        #Verifica se cada nucleotídeo tem valores para todas as posições
        for values in pwm_matrix.values():
            self.assertEqual(len(values), self.tam_motif)

    def test_consenso(self):
        '''
        Teste para a função consenso.
        Verifica se:
        1. A sequência consenso tem o tamanho correto
        2. A sequência contém apenas nucleotídeos válidos
        '''
        #Escolhe uma sequência e gera motifs
        _, seqs2, motifs,random_index = choose_seq(self.seqs, pos_init(self.seqs, self.tam_motif), self.tam_motif)
        
        #Cria matriz de ocorrências
        matriz = matriz_oc(motifs, pseudocont=0.5) #bla bla bla 0.1
        
        #Gera matriz de probabilidades
        pwm_matrix = pwm(matriz)
        
        #Gera sequência consenso
        seq_consenso = consenso(pwm_matrix)
        
        #Verifica o tamanho da sequência consenso
        self.assertEqual(len(seq_consenso), self.tam_motif)
        
        #Verifica se a sequência contém apenas nucleotídeos válidos
        self.assertTrue(all(n in 'ACGT' for n in seq_consenso))

    def test_prob_p(self):
        '''
        Teste para a função prob_p (probabilidades).
        Verifica se:
        1. O número de probabilidades corresponde ao número de possíveis motifs
        2. Todas as probabilidades estão no intervalo [0, 1]
        '''
        #Escolhe uma sequência e gera motifs
        _, seqs2, motifs,random_index = choose_seq(self.seqs, pos_init(self.seqs, self.tam_motif), self.tam_motif)
        
        #Cria matriz de ocorrências
        matriz = matriz_oc(motifs, pseudocont=0.5) #bla 0.1
        
        #Gera matriz de probabilidades
        pwm_matrix = pwm(matriz)
        
        #Calcula probabilidades para a primeira sequência
        prob_dict = prob_p(self.seqs[0], self.tam_motif, pwm_matrix)
        
        #Verifica se o número de probabilidades está correto
        self.assertEqual(len(prob_dict), len(self.seqs[0]) - self.tam_motif + 1)
        
        #Verifica se todas as probabilidades estão no intervalo [0, 1]
        for value in prob_dict.values():
            self.assertTrue(0 <= value <= 1)


    def test_normalize_probabilities(self):
        '''
        Teste para a função normalize_probabilities.
        Verifica se:
        1. A soma das probabilidades normalizadas é próxima de 1
        2. Todas as probabilidades estão no intervalo [0, 1]
        '''
        #Dicionário de probabilidades de teste
        prob_dict = {'A': 0.2, 'B': 0.3, 'C': 0.5}
        
        #Normaliza as probabilidades
        normalized = normalize_probabilities(prob_dict)
        
        #Verifica se a soma das probabilidades é próxima de 1
        self.assertAlmostEqual(sum(normalized.values()), 1.0, places=5)
        
        #Verifica se todas as probabilidades normalizadas estão no intervalo [0, 1]
        for value in normalized.values():
            self.assertTrue(0 <= value <= 1)



    def test_gibbs_sampler_output(self):
        """
        Testa se os motifs têm o tamanho certo e se as posições iniciais estão dentro dos limites possíveis.
        """
        num_iterations = 1000
        result = gibbs_sampler(self.seqs, self.tam_motif, num_iterations)
        
        for motif, position in result: #
            self.assertEqual(len(motif), self.tam_motif) # Verifica se os motifs têm o tamanho certo

        for i, (motif, position) in enumerate(result): # Verifica se as posições iniciais estão dentro dos limites possiveis.
            self.assertGreaterEqual(position, 0)
            self.assertLessEqual(position, len(self.seqs[i]) - self.tam_motif)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMotifSelection)
    unittest.TextTestRunner(verbosity=3).run(suite)