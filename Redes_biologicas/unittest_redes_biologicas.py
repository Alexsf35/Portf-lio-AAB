import unittest
from ReactionGraph import MetabolicNetwork

class TestMetabolicNetwork(unittest.TestCase):
    """
    Classe de testes unitários para a classe MetabolicNetwork.

    """

    def setUp(self):
        """
        Inicializa a rede metabólica com um conjunto fixo de reações
        para ser utilizado em todos os testes.
        """
        reactions = {
            'R01': {'cons': ['M03', 'M05'], 'prod': ['M07']},
            'R02': {'cons': ['M04', 'M05'], 'prod': ['M07', 'M02']},
            'R03': {'cons': ['M08', 'M07', 'M02'], 'prod': ['M04', 'M05']},
            'R04': {'cons': ['M03', 'M04'], 'prod': ['M01']},
            'R05': {'cons': ['M05', 'M08'], 'prod': ['M01', 'M04']},
            'R06': {'cons': ['M08', 'M07'], 'prod': ['M01', 'M05']},
            'R07': {'cons': ['M03', 'M07'], 'prod': ['M06', 'M01']},
            'R08': {'cons': ['M01', 'M05'], 'prod': ['M02', 'M08']},
            'R09': {'cons': ['M07', 'M06'], 'prod': ['M04', 'M08']},
            'R10': {'cons': ['M03', 'M05', 'M04'], 'prod': ['M08', 'M02']}
        }
        self.network = MetabolicNetwork(reactions)

    def test_metabolitos(self):
        """
        Testa se a lista de metabolitos únicos está correta.
        """
        expected = ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08']
        result = self.network.metabolitos()
        self.assertEqual(result, expected)

    def test_consome(self):
        """
        Testa os metabolitos consumidos por reações específicas.
        """
        self.assertEqual(self.network.consome('R10'), ['M03', 'M05', 'M04'])
        self.assertEqual(self.network.consome('R05'), ['M05', 'M08'])

    def test_produz(self):
        """
        Testa os metabolitos produzidos por uma reação específica.
        """
        self.assertEqual(self.network.produz('R04'), ['M01'])

    def test_consomem(self):
        """
        Testa as reações que consomem um determinado metabolito.
        """
        self.assertEqual(self.network.consomem('M08'), ['R03', 'R05', 'R06'])

    def test_produzem(self):
        """
        Testa as reações que produzem um determinado metabolito.
        """
        self.assertEqual(self.network.produzem('M04'), ['R03', 'R05', 'R09'])

    def test_mlig(self):
        """
        Testa os metabolitos ligados a partir dos produtos das reações que consomem um metabolito.
        """
        self.assertEqual(self.network.mlig('M07'), ['M01', 'M04', 'M05', 'M06', 'M08'])

    def test_rlig(self):
        """
        Testa as reações que consomem os produtos de uma dada reação.
        """
        self.assertEqual(self.network.rlig('R01'), ['R03', 'R06', 'R07', 'R09'])

    def test_ativadas_por(self):
        """
        Testa as reações ativadas por um conjunto de metabolitos.
        """
        self.assertEqual(self.network.ativadas_por('M06', 'M01'), [])
        self.assertEqual(self.network.ativadas_por('M03', 'M04'), ['R04'])

    def test_produzidos_por(self):
        """
        Testa os metabolitos produzidos por um conjunto de reações.
        """
        self.assertEqual(self.network.produzidos_por('R01', 'R02'), ['M02', 'M07'])

    def test_r_ativ(self):
        """
        Testa todas as reações ativadas (direta ou indiretamente) por metabolitos dados.
        """
        self.assertEqual(self.network.r_ativ('M01', 'M05'), ['R02', 'R03', 'R05', 'R06', 'R08'])

    def test_m_ativ(self):
        """
        Testa os metabolitos resultantes de todas as reações ativadas por metabolitos dados.
        """
        self.assertEqual(self.network.m_ativ('M01', 'M05'), ['M01', 'M02', 'M04', 'M05', 'M07', 'M08'])


if __name__ == '__main__':
    unittest.main()
