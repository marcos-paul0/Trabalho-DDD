import unittest
from katalog.domain.entities import Midia, StatusMidia
from katalog.domain.value_objects import Progresso, Nota


class DomainTests(unittest.TestCase):
    def test_progresso_invalido(self):
        with self.assertRaises(ValueError):
            Progresso(-1, 10)
        with self.assertRaises(ValueError):
            Progresso(11, 10)

    def test_nota_invalida(self):
        with self.assertRaises(ValueError):
            Nota(-1)
        with self.assertRaises(ValueError):
            Nota(11)

    def test_midia_registra_progresso_e_percentual(self):
        m = Midia('T', 100)
        self.assertEqual(m.status, StatusMidia.PENDENTE)
        m.registrar_progresso(10)
        self.assertEqual(m.progresso.atual, 10)
        self.assertEqual(m.status, StatusMidia.EM_ANDAMENTO)
        self.assertAlmostEqual(m.percentual_consumido(), 10.0)

    def test_concluir_somente_completo(self):
        m = Midia('T2', 50)
        with self.assertRaises(ValueError):
            m.concluir(8)
        m.registrar_progresso(50)
        m.concluir(7)
        self.assertEqual(m.status, StatusMidia.CONCLUIDO)
        self.assertEqual(m.nota.valor, 7)


if __name__ == '__main__':
    unittest.main()
