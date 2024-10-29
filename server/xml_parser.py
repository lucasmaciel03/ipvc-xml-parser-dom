# Funções específicas para parsing e validação

import xml.etree.ElementTree as ET


def parse_xml(file_path):
    try:
        # Parseia o ficheiro XML
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Imprime a estrutura do XML
        print("Root tag:", root.tag)
        print("Attributes:", root.attrib)

        # Itera pelos elementos do XML
        for child in root:
            print(f"Tag: {child.tag}, Attributes: {child.attrib}, Text: {child.text}")

    except ET.ParseError as e:
        print(f"Erro ao fazer parsing do ficheiro XML: {str(e)}")
