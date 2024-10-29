# Código do cliente para enviar/receber XML

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import grpc
import xml_service_pb2
import xml_service_pb2_grpc


def send_xml_file(filename):
    # Lê o conteúdo do ficheiro XML
    try:
        with open(filename, "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Estabelece a comunicação com o servidor
    channel = grpc.insecure_channel("localhost:50051")
    stub = xml_service_pb2_grpc.XMLParserServiceStub(channel)

    # Envia o ficheiro XML para o servidor
    response = stub.SendXMLFile(
        xml_service_pb2.XMLRequest(
            filename=filename,
            file_content=file_content
        )
    )

    # Imprime a resposta do servidor
    if response.success:
        print("Server response:", response.message)
    else:
        print("Failed to send file. Server response:", response.message)


if __name__ == "__main__":
    # Testar o envio de um ficheiro XML
    send_xml_file("example.xml")
