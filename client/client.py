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
        # Solicita um subconjunto do XML
        get_subset_of_xml(stub, ["1", "2"])  # IDs de exemplo para teste
    else:
        print("Failed to send file. Server response:", response.message)


def get_subset_of_xml(stub, tag_ids):
    # Solicita ao servidor um subconjunto do XML
    response = stub.GetXMLSubset(
        xml_service_pb2.TagIDRequest(
            tag_ids=tag_ids
        )
    )
    print("Subset response:", response.subset_content)


def send_csv_file(filename):
    # Verifique se o ficheiro existe no caminho especificado
    if not os.path.isfile(filename):
        print(f"DEBUG CLIENT: Ficheiro '{filename}' não encontrado.")
        return

    # Lê o conteúdo do ficheiro CSV
    try:
        with open(filename, "r") as file:
            file_content = file.read()
            print(f"DEBUG CLIENT: Conteúdo do ficheiro CSV: {file_content}")  # Verificação adicional no cliente
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Estabelece a comunicação com o servidor
    channel = grpc.insecure_channel("localhost:50051")
    stub = xml_service_pb2_grpc.XMLParserServiceStub(channel)

    # Envia o ficheiro CSV para o servidor
    response = stub.ConvertCSVToXML(
        xml_service_pb2.XMLRequest(
            filename=os.path.basename(filename),
            file_content=file_content
        )
    )

    # Imprime a resposta do servidor
    if response.success:
        print("Server response:", response.message)
    else:
        print("Failed to convert CSV. Server response:", response.message)


if __name__ == "__main__":
    # Testar o envio de um ficheiro XML
    send_xml_file("example.xml")

    # Testar o envio de um ficheiro CSV (apenas o nome do ficheiro)
    send_csv_file("server/datasets/example.csv")
