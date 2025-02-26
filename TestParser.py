import unittest
# import pytest
from parser import Parser, gerar_pdf
import xml.etree.ElementTree as ET


test_pdf_path = "artigo_formatado.pdf"

class TestParser(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.parser = Parser("artigo.xml")

    def test_UT_01(self):
        """Testa se o título foi retornado corretamente"""
        self.assertEqual(self.parser.get_titulo().__class__, str)

    def test_UT_02(self):
        """Testa se os autores foram retornados corretamente"""
        self.assertEqual(self.parser.get_autores().__class__, list)

    def test_UT_03(self):
        """Testa se o resumo foi retornado corretamente"""
        self.assertEqual(self.parser.get_resumo().__class__, str)

    def test_UT_04(self):
        """Testa se a seção foi retornada corretamente"""
        self.assertEqual(self.parser.get_secoes().__class__, list)

    def test_UT_05(self):
        parser = Parser("artigo.xml")
        self.assertEqual(parser.get_referencias().__class__, list)
    
    def test_UT_06(self):
        try:
            parser = Parser("artigo_invalido.xml")
        except Exception as e:
            parser = e
        self.assertNotEqual(parser.__class__, Parser)
    
    def test_UT_07(self):
        parser = Parser("artigo_sem_titulo.xml")
        try:
            titulo = parser.get_titulo()
        except Exception as e:
            titulo = e.args[0]
        self.assertEqual(titulo.__class__, str)
    
    def test_UT_08(self):
        parser = Parser("artigo_sem_autores.xml")
        autores = parser.get_autores()
        self.assertEqual(autores.__class__, list)

    def test_UT_09(self):
        # Testar referências incompletas (sem ano ou titulo
        parser09 = Parser("ut_09.xml")
        self.assertEqual(parser09.get_referencias(), ['Título desconhecido, Fonte desconhecida, Ano desconhecido', 'Título desconhecido, Artificial Intelligence in Testing, 2021'])

    def test_UT_10(self):
        # testar título longo
        parser10 = Parser("ut_10.xml")
        self.assertEqual(parser10.get_titulo(), "EsteÉUmTítuloExtremamenteLongoProjetadoEspecificamenteParaTestarOsLimitesDeUmParserXMLQuePodeTerRestriçõesDeTamanhoOuErrosDeManipulaçãoDeStringsExcessivamenteGrandesDentroDeElementosOuAtributosNoArquivoXML")

    def test_UT_11(self):
        # testar resumo e seções vazias
        parser11 = Parser("ut_11.xml")
        self.assertEqual(parser11.get_resumo(), None)
        self.assertEqual(parser11.get_secoes(), [(None,[None])])
        
    def test_UT_12(self):
        # testar resumo longo
        parser12 = Parser("ut_12.xml")
        self.assertEqual(parser12.get_resumo(), 'Este documento tem como objetivo principal testar os limites de um parser XML ao lidar com elementos e atributos que contêm textos excepcionalmente longos. Muitas implementações de parsers XML possuem restrições internas, sejam elas baseadas no tamanho máximo permitido para um nó, na memória disponível para processar o documento ou em regras específicas de formatação e estruturação. Dessa forma, ao utilizar um título excessivamente longo e um resumo extenso, buscamos identificar possíveis falhas, como truncamento inesperado, erros de alocação de memória ou falhas de processamento que podem comprometer a integridade dos dados manipulados. Além disso, este teste pode revelar eventuais dificuldades no carregamento e interpretação do XML por diferentes bibliotecas e linguagens de programação, possibilitando ajustes e otimizações no código responsável por sua leitura e escrita. É importante considerar que parsers robustos devem ser capazes de processar conteúdos grandes sem comprometer a performance ou causar falhas inesperadas, garantindo a confiabilidade do sistema que depende dessa estrutura de dados. Portanto, ao executar esse teste, podemos avaliar não apenas a capacidade do parser em processar grandes volumes de texto, mas também sua resiliência e conformidade com os padrões estabelecidos para XML, identificando assim a necessidade de ajustes para evitar problemas futuros.')

    def test_IT_01(self):
        """Testa extração e formatação completa do artigo"""
        parser = Parser("artigo.xml")

        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf("artigo_formatado.pdf", dados)
        except Exception as e:
            success = e.args

        self.assertEqual(success, True)

    def test_IT_02(self):
        """Testa o pipeline de extração e geração de PDF"""

        parser = Parser("artigo.xml")  # Inicializa o parser com o XML de entrada
        dados = parser.get_dados_completos()  # Extrai os dados completos

        output_pdf = "artigo_pipeline.pdf"

        success = True
        try:
            gerar_pdf(output_pdf, dados)  # Gera o PDF com os dados extraídos
            # Verifica se o arquivo foi realmente criado
            import os
            self.assertTrue(os.path.exists(output_pdf), "O arquivo PDF não foi gerado.")
        except Exception as e:
            success = e.args

        self.assertEqual(success, True)
        
    def test_IT_03(self):
        """Testa integração com XML sem título"""
        parser = Parser("artigo_sem_article_title.xml")

        success = True
        try:
            dados = parser.get_dados_completos()
            
            # Se o título for None, substituí-lo por string vazia antes de gerar o PDF
            if dados.get("titulo") is None:
                dados["titulo"] = ""

            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args

        self.assertEqual(success, True)


    def test_IT_04(self):
        """Testa integração com XML sem autores"""

        parser = Parser("artigo_sem_autores.xml")

        success = True
        try:
            dados = parser.get_dados_completos()

            # Se os autores for None, substituí-lo por string vazia antes de gerar o PDF
            dados["autores"] = [autor if autor != "None None" else "" for autor in dados.get("autores", [])]
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args

        self.assertEqual(success, True)

    def test_IT_05(self):
        parser = Parser("artigo_sem_abstract.xml")
        
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
        
        self.assertEqual(success, True)
        
    def test_IT_06(self):
        parser = Parser("artigo_referencias_incompletas.xml")
        
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
            
        self.assertEqual(success, True)
    
    def test_IT_07(self):
        parser = Parser("artigo_titulo_longo.xml")
        
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
            
        self.assertEqual(success, True)
    
    def test_IT_08(self):
        parser = Parser("artigo_resumo_longo.xml")
        
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
            
        self.assertEqual(success, True)

    def test_IT_09(self):
        #testar integração com multiplos autores
        parser = Parser("artigo_multi_autor.xml")

        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
        # PDF gerado todos os autores corretamente
        self.assertEqual(success,True)

    def test_IT_10(self):
        # XML sem seções
        parser = Parser("artigo_sem_secao.xml")
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
        # PDF gerado sem seções
        self.assertEqual(success,True)
    
    def test_IT_11(self):
        # XML sem ref
        parser = Parser("artigo_sem_referencias.xml")
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
        # PDF gerado sem ref
        self.assertEqual(success,True)

    def test_IT_12(self):
        # Testar fluxo completo com diversas variações do XML
        success = True
        xmls = ["artigo_sem_secao.xml","artigo_multi_autor.xml","artigo_resumo_longo.xml"]
        try:
            for xml in xmls:
                parser = Parser(xml)
                dados = parser.get_dados_completos()
                gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
        self.assertEqual(success, True)
            
    
    def test_MT_01(self):
        parser = Parser("artigo.xml")

        success = True
        try:
            self.test_UT_01()
            self.test_UT_02()
            self.test_UT_03()
            self.test_UT_04()
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
            
        self.assertEqual(success, True)

    def test_MT_02(self):
        parser = None
        success = False
        try:
            parser = Parser("artigo_mal_formado.xml")
            dados = parser.get_dados_completos()  # Isso deve lançar uma exceção
        except Exception as e:
            # Aqui capturamos qualquer exceção gerada
            self.assertIsInstance(e, ET.ParseError) 
            success = True

        # Garantimos que a exceção tenha sido capturada
        self.assertTrue(success, "O teste falhou porque a exceção não foi levantada.")

    def test_MT_03(self):
        parser = Parser("artigo_sem_referencias.xml")
        
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
            
        self.assertEqual(success, True)
    
    def test_MT_04(self):
        parser = Parser("artigo_secao_vazia.xml")
        
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
            
        self.assertEqual(success, True)  

    def test_MT_05(self):
        parser = Parser("artigo_sem_autores.xml")
        
        success = True
        try:
            dados = parser.get_dados_completos()
            gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
            
        self.assertEqual(success, True)
    
    def test_MT_06(self):
        # Testar integração com múltiplos arquivos
        success = True
        xmls = ["artigo_sem_secao.xml","artigo_multi_autor.xml","artigo_resumo_longo.xml"]
        try:
            for xml in xmls:
                parser = Parser(xml)
                dados = parser.get_dados_completos()
                gerar_pdf(test_pdf_path, dados)
        except Exception as e:
            success = e.args
        self.assertEqual(success, True)


if __name__ == "__main__":
    unittest.main()

    # parser = Parser("artigo.xml")
    # print(parser.get_titulo().__class__)
