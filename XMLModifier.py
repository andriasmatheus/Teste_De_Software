import xml.etree.ElementTree as ET

class XMLModifier:
    def __init__(self, arquivo_xml):
        """Inicializa o parser e carrega o XML"""
        self.tree = ET.parse(arquivo_xml)
        self.root = self.tree.getroot()

    def set_titulo(self, novo_titulo):
        """Atualiza o título do artigo"""
        self.root.find(".//article-title").text = novo_titulo

    def set_autores(self, autores):
        """Atualiza a lista de autores do artigo"""
        for i, autor in enumerate(self.root.findall(".//contrib[@contrib-type='author']")):
            nome, sobrenome = autores[i].split()
            autor.find(".//given-names").text = nome
            autor.find(".//surname").text = sobrenome

    def set_resumo(self, novo_resumo):
        """Atualiza o resumo do artigo"""
        self.root.find(".//abstract/p").text = novo_resumo

    def set_secoes(self, secoes):
        """Atualiza as seções do artigo"""
        for i, secao in enumerate(self.root.findall(".//sec")):
            titulo_secao, paragrafos = secoes[i]
            secao.find("title").text = titulo_secao
            for j, p in enumerate(secao.findall("p")):
                p.text = paragrafos[j]

    def set_referencias(self, referencias):
        """Atualiza as referências do artigo"""
        for i, ref in enumerate(self.root.findall(".//ref")):
            titulo_ref, source_ref, ano_ref = referencias[i]
            titulo_ref_elem = ref.find(".//article-title")
            source_ref_elem = ref.find(".//source")
            ano_ref_elem = ref.find(".//year")
            if titulo_ref_elem is not None:
                titulo_ref_elem.text = titulo_ref
            if source_ref_elem is not None:
                source_ref_elem.text = source_ref
            if ano_ref_elem is not None:
                ano_ref_elem.text = ano_ref

    def set_id_artigo(self, novo_doi):
        """Atualiza o DOI do artigo"""
        self.root.find(".//article-id[@pub-id-type='doi']").text = novo_doi

    def set_issn(self, novo_issn):
        """Atualiza o ISSN do artigo"""
        self.root.find(".//issn").text = novo_issn

    def set_data_publicacao(self, ano, mes, dia):
        """Atualiza a data de publicação do artigo"""
        data_pub = self.root.find(".//pub-date[@pub-type='epub']")
        data_pub.find("year").text = str(ano)
        data_pub.find("month").text = str(mes)
        data_pub.find("day").text = str(dia)

    def set_journal_id(self, novo_journal_id):
        """Atualiza o ID da revista"""
        self.root.find(".//journal-id[@journal-id-type='publisher']").text = novo_journal_id

    def set_journal_title(self, novo_journal_title):
        """Atualiza o título da revista"""
        self.root.find(".//journal-title").text = novo_journal_title

    def save(self, novo_arquivo_xml):
        """Salva as modificações em um novo arquivo XML"""
        self.tree.write(novo_arquivo_xml)
