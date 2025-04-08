import unittest
from AF import Automata
from unittest.mock import patch, MagicMock

class TestAutomatosFinitos(unittest.TestCase):
    
    def setUp(self):
        # Configuração inicial para os testes
        # Exemplos simples para teste
        self.pattern1 = "ACA"
        self.sequence1 = "CACAACAAACA"
        
        # Exemplos mais complexos
        self.pattern2 = "ACGT"
        self.sequence2 = "ACGTACGTACGTACGT"
        
        # Exemplo com caracteres não encontrados
        self.pattern3 = "XYZ"
        self.sequence3 = "ABCDEFGH"
        
        self.af1 = Automata(self.pattern1, self.sequence1)
        self.af2 = Automata(self.pattern2, self.sequence2)
        self.af3 = Automata(self.pattern3, self.sequence3)
    
    def test_init(self):
        """
        Verifica se as propriedades são inicializadas corretamente
        """
        # Verifica a inicialização dos atributos
        self.assertEqual(self.af1.pattern, self.pattern1)
        self.assertEqual(self.af1.sequence, self.sequence1)
        self.assertEqual(self.af1.m, len(self.pattern1))
        self.assertEqual(self.af1.states, [0, 1, 2, 3])
        self.assertEqual(set(self.af1.alphabet), set(['A', 'C']))
        
        # Verifica se a tabela de transição e lista de matches foram criadas
        self.assertIsNotNone(self.af1.transition_table)
        self.assertIsNotNone(self.af1.matches)
    
    def test_max_overlap(self):
        """
        Verifica se o cálculo da sobreposição máxima entre duas strings está correto
        """
        test_cases = [
            # s1, s2, expected_overlap
            ("ABC", "BCD", 2),     # Sobreposição de 2 caracteres (BC)
            ("ABC", "CDE", 1),     # Sobreposição de 1 caractere (C)
            ("ABCDE", "CDE", 3),   # Sobreposição de 3 caracteres (CDE)
            ("ABCDE", "ABCDE", 5), # Sobreposição total
            ("", "ABC", 0),        # String vazia
            ("ABC", "", 0)         # String vazia
        ]
        
        # Testa cada caso de sobreposição
        for s1, s2, expected in test_cases:
            with self.subTest(s1=s1, s2=s2):
                result = self.af1.max_overlap(s1, s2)
                self.assertEqual(result, expected, f"max_overlap({s1}, {s2}) deveria ser {expected}, obteve {result}")
    
    def test_build_transition_table(self):
        """
        Verifica se a tabela de transições está correta para diferentes padrões
        """
        # Verificação manual para o padrão "ACA"
        expected_transitions = {
            (0, 'A'): 1,
            (0, 'C'): 0,
            (1, 'A'): 1,
            (1, 'C'): 2,
            (2, 'A'): 3,
            (2, 'C'): 0,
            (3, 'A'): 1,
            (3, 'C'): 2
        }
        
        # Verifica se todas as transições esperadas estão na tabela
        for key, value in expected_transitions.items():
            self.assertEqual(self.af1.transition_table[key], value, 
                             f"Transição {key} deveria ser {value}, obteve {self.af1.transition_table.get(key)}")
        
        # Verifica o tamanho da tabela de transições
        self.assertEqual(len(self.af1.transition_table), len(self.af1.states) * len(self.af1.alphabet),
                        "A tabela de transição deve ter entradas state × alphabet")
    
    def test_process_sequence(self):
        """
        Verifica se a sequência de estados está correta ao processar uma sequência de entrada
        """
        # Verificação manual para o padrão "ACA" e sequência "CACAACAAACA"
        expected_states = [0, 0, 1, 2, 3, 1, 2, 3, 1, 1, 2, 3]
        
        # Processa a sequência e compara com os estados esperados
        states = self.af1.process_sequence()
        self.assertEqual(states, expected_states,
                        f"Estados esperados {expected_states}, obteve {states}")
        
        # Teste para padrão não encontrado
        states3 = self.af3.process_sequence()
        self.assertEqual(len(states3), len(self.sequence3) + 1,
                        "O número de estados deve ser o comprimento da sequência + 1")
        self.assertTrue(all(state == 0 for state in states3),
                        "Todos os estados devem ser 0 quando o padrão não é encontrado")
    
    def test_find_matches(self):
        """
        Verifica se as posições onde o padrão é encontrado estão corretas
        """
        # Verificação para o padrão "ACA" na sequência "CACAACAAACA"
        expected_matches1 = [1, 4, 8]  # O padrão ocorre nas posições 1, 4 e 8
        self.assertEqual(self.af1.matches, expected_matches1,
                        f"Ocorrências esperadas em {expected_matches1}, obteve {self.af1.matches}")
        
        # Verificação para o padrão "ACGT" na sequência "ACGTACGTACGTACGT"
        expected_matches2 = [0, 4, 8, 12]  # O padrão ocorre em múltiplas posições
        self.assertEqual(self.af2.matches, expected_matches2,
                        f"Ocorrências esperadas em {expected_matches2}, obteve {self.af2.matches}")
        
        # Verificação para padrão não encontrado
        self.assertEqual(self.af3.matches, [],
                        "Deve retornar lista vazia quando o padrão não é encontrado")
    
    @patch('AF.PrettyTable')
    def test_print_table(self, mock_pretty_table):
        """
        Verifica se a tabela de visualização do autómato é criada corretamente
        """
        # Cria um mock para PrettyTable
        mock_table = MagicMock()
        mock_pretty_table.return_value = mock_table
        
        result = self.af1.print_table()
        
        # Verifica se os métodos da PrettyTable foram chamados corretamente
        mock_table.add_row.assert_called()
        self.assertEqual(mock_table.add_row.call_count, 3,
                        "Deve adicionar 3 linhas à tabela (sequência, estado, ocorrência)")
        
        # Verifica se a tabela retornada pelo autómato é a esperada
        self.assertEqual(result, mock_table)
    
    def test_example_from_code(self):
        """
        Verifica se o exemplo do código original funciona conforme esperado
        """
        af_teste = Automata("ACA", "CACAACAAACA")
        
        # Verifica o alfabeto
        self.assertEqual(af_teste.alphabet, ['A', 'C'])
        
        # Verifica os matches encontrados
        self.assertEqual(af_teste.matches, [1, 4, 8])
        
        # Verifica se a tabela de transição existe
        self.assertIsNotNone(af_teste.transition_table)
        
        # Verifica se a tabela formatada existe
        self.assertIsNotNone(af_teste.table)
    
    def test_edge_cases(self):
        """
        Verifica como o autómato se comporta em situações limite
        """
        # Teste com padrão vazio (não levanta exceção no código original)
        af_empty_pattern = Automata("", "ACGT")
        self.assertEqual(af_empty_pattern.matches, [])
        
        # Teste com sequência vazia
        af_empty_seq = Automata("A", "")
        self.assertEqual(af_empty_seq.matches, [])
        
        # Teste com padrão igual à sequência
        af_same = Automata("ACGT", "ACGT")
        self.assertEqual(af_same.matches, [0])
        
        # Teste com padrão maior que a sequência
        af_long_pattern = Automata("ACGTACGT", "ACGT")
        self.assertEqual(af_long_pattern.matches, [])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAutomatosFinitos)
    unittest.TextTestRunner(verbosity=3).run(suite)