# Código do servidor para receber/parsing de XML

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from concurrent import futures
import grpc
import xml_service_pb2
import xml_service_pb2_grpc
from xml_parser import parse_xml  # Importa a função de parsing


class XMLParserService(xml_service_pb2_grpc.XMLParserServiceServicer):
    def SendXMLFile(self, request, context):
        file_path = f"server/data/{request.filename}"
        try:
            with open(file_path, "w") as file:
                file.write(request.file_content)

            print(f"Conteúdo do ficheiro recebido:\n{request.file_content}")  # Log para ver o conteúdo

            # Realiza o parsing do ficheiro XML recebido
            parse_xml(file_path)

            return xml_service_pb2.XMLResponse(message="File received successfully and parsed.", success=True)
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
