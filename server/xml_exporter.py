import csv
import json
import xml.etree.ElementTree as ET


def export_to_json(file_path, output_path):
    try:
        # Parseia o ficheiro XML
        tree = ET.parse(file_path)
        root = tree.getroot()

        def element_to_dict(element):
            """Converte um elemento XML para um dicionário."""
            element_dict = element.attrib if element.attrib else {}
            if element.text and element.text.strip():
                element_dict['text'] = element.text.strip()
            for child in element:
                element_dict[child.tag] = element_to_dict(child)
            return element_dict

        # Converte a árvore XML para um dicionário
        xml_dict = {root.tag: element_to_dict(root)}

        # Exporta o dicionário para um ficheiro JSON
        with open(output_path, 'w') as json_file:
            json.dump(xml_dict, json_file, indent=4)

        print(f"XML successfully exported to JSON at {output_path}.")
        return True
    except Exception as e:
        print(f"Error exporting XML to JSON: {str(e)}")
        return False


def export_to_csv(file_path, output_path):
    try:
        # Parseia o ficheiro XML
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Coleta todos os cabeçalhos e dados dos elementos
        headers = set()
        data_rows = []

        for element in root:
            row_data = {}
            for child in element:
                headers.add(child.tag)
                row_data[child.tag] = child.text.strip() if child.text else ""
            data_rows.append(row_data)

        # Ordena os cabeçalhos
        headers = sorted(headers)

        # Escreve os dados num ficheiro CSV
        with open(output_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_rows)

        print(f"XML successfully exported to CSV at {output_path}.")
        return True
    except Exception as e:
        print(f"Error exporting XML to CSV: {str(e)}")
        return False
