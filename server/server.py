# Código do servidor para receber/parsing de XML

import logging

# Configuração de logging
logging.basicConfig(
    filename='server.log',  # Nome do arquivo de log
    level=logging.INFO,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato da mensagem de log
)

# Testando o logger
logging.info("Server started")

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
        logging.info(f"Received XML file: {request.filename}")
        file_path = f"server/data/{request.filename}"
        xsd_path = "schemas/schema.xsd"  # Caminho para o ficheiro XSD

        try:
            # Salva o conteúdo do ficheiro recebido
            with open(file_path, "w") as file:
                file.write(request.file_content)
            logging.info(f"Saved XML file: {file_path}")

            # Valida o ficheiro XML com o esquema XSD
            is_valid, validation_message = validate_xml(file_path, xsd_path)
            if not is_valid:
                logging.warning(f"Validation failed for file: {file_path}. Reason: {validation_message}")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(validation_message)
                return xml_service_pb2.XMLResponse(message=validation_message, success=False)

            # Processamento e exportação
            parse_xml(file_path)
            export_to_json(file_path, "server/data/output.json")
            export_to_csv(file_path, "server/data/output.csv")
            transform_xml(file_path, "server/data/transformed_output.xml", transformations=[sample_transformation])

            logging.info(f"Successfully processed XML file: {file_path}")
            return xml_service_pb2.XMLResponse(
                message="File processed successfully.", success=True)
        except FileNotFoundError as e:
            logging.error(f"File not found: {file_path}. Error: {str(e)}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"File not found: {str(e)}")
            return xml_service_pb2.XMLResponse(message="File not found", success=False)
        except Exception as e:
            logging.error(f"Error processing XML file {file_path}: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error processing XML: {str(e)}")
            return xml_service_pb2.XMLResponse(message=f"Error: {str(e)}", success=False)

    def GetXMLSubset(self, request, context):
        logging.info(f"Received request for XML subset with IDs: {request.tag_ids}")
        try:
            file_path = "server/data/transformed_output.xml"
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Busca as tags especificadas
            subset_elements = []
            for tag_id in request.tag_ids:
                elements = root.findall(f".//*[@id='{tag_id}']")
                subset_elements.extend(elements)

            # Converte os elementos encontrados num novo XML
            subset_tree = ET.Element("Subset")
            for elem in subset_elements:
                subset_tree.append(elem)

            subset_xml_string = ET.tostring(subset_tree, encoding='unicode', method='xml')
            logging.info(f"Successfully extracted XML subset for IDs: {request.tag_ids}")
            return xml_service_pb2.XMLSubsetResponse(subset_content=subset_xml_string)
        except Exception as e:
            logging.error(f"Error extracting XML subset for IDs {request.tag_ids}: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error extracting subset: {str(e)}")
            return xml_service_pb2.XMLSubsetResponse(subset_content=f"Error: {str(e)}")

    def ConvertCSVToXML(self, request, context):
        logging.info(f"Received CSV file for conversion: {request.filename}")
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_file_path = os.path.join(base_dir, "datasets", request.filename)
            xml_output_path = os.path.join(base_dir, "data", "converted_output.xml")

            # Mensagens de depuração
            logging.debug(f"DEBUG: CSV file path: {csv_file_path}")
            logging.debug(f"DEBUG: Output XML file path: {xml_output_path}")

            # Verifica se o ficheiro CSV existe
            if not os.path.isfile(csv_file_path):
                logging.warning(f"CSV file not found: {csv_file_path}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"File '{csv_file_path}' not found on server.")
                return xml_service_pb2.XMLResponse(message=f"File '{csv_file_path}' not found on server.", success=False)

            # Converte o CSV para XML
            conversion_success = csv_to_xml(csv_file_path, xml_output_path)
            if not conversion_success:
                logging.warning(f"Conversion from CSV to XML failed for file: {csv_file_path}")
                return xml_service_pb2.XMLResponse(message="Error converting CSV to XML", success=False)

            # Valida o novo XML gerado com o esquema XSD
            xsd_path = os.path.join(base_dir, "..", "schemas", "schema.xsd")
            is_valid, validation_message = validate_xml(xml_output_path, xsd_path)
            if not is_valid:
                logging.warning(f"Validation failed for converted XML file: {xml_output_path}. Reason: {validation_message}")
                return xml_service_pb2.XMLResponse(message=validation_message, success=False)

            logging.info(f"Successfully converted CSV to XML for file: {request.filename}")
            return xml_service_pb2.XMLResponse(message="CSV converted and XML validated successfully.", success=True)
        except Exception as e:
            logging.error(f"Error converting CSV to XML for file {request.filename}: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
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
