import csv
import xml.etree.ElementTree as ET


def csv_to_xml(csv_file_path, xml_output_path):
    try:
        # Cria a estrutura XML principal
        root = ET.Element("root")

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            # Itera por cada linha do CSV
            for row in reader:
                # Cria um elemento XML para cada linha
                element = ET.Element("element")

                # Define os atributos com base no cabeçalho do CSV
                for key, value in row.items():
                    element.set(key, value)

                # Adiciona o elemento à raiz
                root.append(element)

        # Gera a árvore XML e escreve num ficheiro
        tree = ET.ElementTree(root)
        tree.write(xml_output_path, encoding="utf-8", xml_declaration=True)
        print(f"CSV successfully converted to XML at {xml_output_path}.")
        return True
    except Exception as e:
        print(f"Error converting CSV to XML: {str(e)}")
        return False
