import xml.etree.ElementTree as ET


def transform_xml(input_file, output_file, transformations=None):
    """
    Aplica transformações ao ficheiro XML e gera um novo ficheiro XML.

    :param input_file: Caminho para o ficheiro XML de entrada.
    :param output_file: Caminho para o novo ficheiro XML gerado.
    :param transformations: Funções ou operações para aplicar aos elementos XML.
    """
    try:
        # Parseia o ficheiro XML de entrada
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Aplica as transformações definidas
        if transformations:
            for transformation in transformations:
                transformation(root)

        # Salva o novo ficheiro XML com as transformações aplicadas
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"XML successfully transformed and saved at {output_file}.")
        return True
    except Exception as e:
        print(f"Error transforming XML: {str(e)}")
        return False


def sample_transformation(root):
    """
    Exemplo de transformação: Modifica o valor de todos os atributos 'attribute' para 'new_value'.
    """
    for element in root.iter("element"):
        if "attribute" in element.attrib:
            element.attrib["attribute"] = "new_value"
