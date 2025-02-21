import unittest
from parser import Parser  # Importando a classe Parser
from XMLModifier import XMLModifier  # Importando a classe XMLModifier

class TestParser(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.xml_modifier = XMLModifier("artigo.xml")
        self.parser = Parser("artigo.xml")

    def test_get_titulo(self):
        """Testa se o título foi modificado corretamente"""
        self.xml_modifier.set_titulo("Novo título")
        self.xml_modifier.save("artigo.xml")
        self.assertEqual(self.parser.get_titulo(), "Novo título")

if __name__ == "__main__":
    unittest.main()
