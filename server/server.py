# Código do servidor para receber/parsing de XML

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from concurrent import futures
import grpc
import xml.etree.ElementTree as ET
from csv_to_xml import csv_to_xml
import xml_service_pb2
import xml_service_pb2_grpc
from xml_parser import parse_xml
from xml_validator import validate_xml
from xml_exporter import export_to_json, export_to_csv
from xml_transformer import transform_xml, sample_transformation


class XMLParserService(xml_service_pb2_grpc.XMLParserServiceServicer):
    def SendXMLFile(self, request, context):
        file_path = f"server/data/{request.filename}"
        xsd_path = "schemas/schema.xsd"  # Caminho para o ficheiro XSD

        try:
            # Salva o conteúdo do ficheiro recebido
            with open(file_path, "w") as file:
                file.write(request.file_content)

            print(f"Conteúdo do ficheiro recebido:\n{request.file_content}")

            # Valida o ficheiro XML com o esquema XSD
            is_valid, validation_message = validate_xml(file_path, xsd_path)
            if not is_valid:
                return xml_service_pb2.XMLResponse(message=validation_message, success=False)

            # Realiza o parsing do ficheiro XML recebido
            parse_xml(file_path)

            # Exporta para JSON e CSV
            export_to_json(file_path, "server/data/output.json")
            export_to_csv(file_path, "server/data/output.csv")

            # Aplica uma transformação e gera um novo ficheiro XML
            transform_xml(file_path, "server/data/transformed_output.xml", transformations=[sample_transformation])

            return xml_service_pb2.XMLResponse(
                message="File received, validated, parsed, exported, and transformed successfully.", success=True)
        except Exception as e:
            return xml_service_pb2.XMLResponse(message=f"Error: {str(e)}", success=False)

    def GetXMLSubset(self, request, context):
        try:
            # Carrega o ficheiro XML principal
            file_path = "server/data/transformed_output.xml"
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Busca as tags especificadas
            subset_elements = []
            for tag_id in request.tag_ids:
                elements = root.findall(f".//*[@id='{tag_id}']")  # Usando XPath para buscar por IDs de tags
                subset_elements.extend(elements)

            # Converte os elementos encontrados num novo XML
            subset_tree = ET.Element("Subset")
            for elem in subset_elements:
                subset_tree.append(elem)

            subset_xml_string = ET.tostring(subset_tree, encoding='unicode', method='xml')
            return xml_service_pb2.XMLSubsetResponse(subset_content=subset_xml_string)
        except Exception as e:
            return xml_service_pb2.XMLSubsetResponse(subset_content=f"Error: {str(e)}")

    def ConvertCSVToXML(self, request, context):
        print("DEBUG: Entrou em ConvertCSVToXML")
        try:
            # Ajusta o caminho para o CSV usando um caminho absoluto
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório absoluto deste script
            csv_file_path = os.path.join(base_dir, "datasets", request.filename)
            xml_output_path = os.path.join(base_dir, "data", "converted_output.xml")

            # Mensagens de depuração
            print(f"DEBUG: Caminho absoluto do ficheiro CSV: {csv_file_path}")
            print(f"DEBUG: Caminho absoluto do ficheiro XML de saída: {xml_output_path}")

            # Verifica se o ficheiro CSV existe
            if not os.path.isfile(csv_file_path):
                return xml_service_pb2.XMLResponse(message=f"File '{csv_file_path}' not found on server.",
                                                   success=False)

            # Converte o CSV para XML
            conversion_success = csv_to_xml(csv_file_path, xml_output_path)
            if not conversion_success:
                return xml_service_pb2.XMLResponse(message="Error converting CSV to XML", success=False)

            # Valida o novo XML gerado com o esquema XSD
            xsd_path = os.path.join(base_dir, "..", "schemas", "schema.xsd")
            is_valid, validation_message = validate_xml(xml_output_path, xsd_path)
            if not is_valid:
                return xml_service_pb2.XMLResponse(message=validation_message, success=False)

            return xml_service_pb2.XMLResponse(message="CSV converted and XML validated successfully.", success=True)
        except Exception as e:
            return xml_service_pb2.XMLResponse(message=f"Error: {str(e)}", success=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xml_service_pb2_grpc.add_XMLParserServiceServicer_to_server(XMLParserService(), server)
    server.add_insecure_port("[::]:50051")
    print("Server is running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
