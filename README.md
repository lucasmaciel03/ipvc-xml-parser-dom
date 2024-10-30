<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="./images/ipvc.png" alt="Logo" width="auto" height="200">
  </a>

  <h1 align="center">Instituto Politéncico Viana do Castelo</h1>

  <h3 align="center">Integração de SIstemas</h3>

  <h3 align="center">Lucas Maciel | João Fernandes</h3>

  <h3 align="center">Document Object Model</h3>
</p>

# Serviço gRPC: XML Parser

Este serviço fornece funcionalidades para upload de ficheiros XML, extração de subconjuntos de XML e conversão de
ficheiros CSV para XML, utilizando gRPC para a comunicação entre cliente e servidor.

## Métodos Disponíveis

### 1. SendXMLFile

- **Descrição:** Envia um ficheiro XML para o servidor para validação e processamento.
- **Requisição:**
    - `filename (string)`: Nome do ficheiro XML.
    - `file_content (string)`: Conteúdo do ficheiro XML.
- **Resposta:**
    - `message (string)`: Mensagem sobre o status do processamento.
    - `success (bool)`: Indica se o processamento foi bem-sucedido.

### 2. GetXMLSubset

- **Descrição:** Solicita um subconjunto do XML com base em IDs de tags fornecidas.
- **Requisição:**
    - `tag_ids (repeated string)`: Lista de IDs de tags para buscar.
- **Resposta:**
    - `subset_content (string)`: Conteúdo XML correspondente ao subconjunto extraído.

### 3. ConvertCSVToXML

- **Descrição:** Converte um ficheiro CSV para XML e valida o XML gerado.
- **Requisição:**
    - `filename (string)`: Nome do ficheiro CSV.
    - `file_content (string)`: Conteúdo do ficheiro CSV.
- **Resposta:**
    - `message (string)`: Mensagem sobre o status da conversão e validação.
    - `success (bool)`: Indica se a conversão foi bem-sucedida.

## Exceções Tratadas

- Validação de ficheiros XML com esquema XSD.
- Conversão de CSV para XML com validação.
- Erros de parsing de XML.
- Manuseio de exceções durante exportações para JSON e CSV.

## Como Utilizar

### Pré-requisitos

- Python 3.8+ instalado.
- Instalar as dependências especificadas no ficheiro `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### Inicializar o Servidor

1. Navegue até ao diretório principal do projeto e execute o comando para iniciar o servidor gRPC:
    ```bash
    python server/server.py
    ```
   O servidor será iniciado na porta 50051. Certifique-se de que esta porta está aberta no seu sistema.

### Executar o Cliente

1. No diretório do cliente, edite o ficheiro `client.py` para definir o ficheiro XML ou CSV que deseja enviar.
2. Execute o comando para testar o envio de um ficheiro XML:
    ```bash
    python client/client.py
    ```
3. Para converter um ficheiro CSV para XML, edite o caminh****o do ficheiro CSV no código e execute:
    ```bash
    python client/client.py
    ```

### Configuração dos Logs

Os logs são gerados automaticamente e armazenados no ficheiro `server.log`. Eles incluem informações sobre operações
realizadas, validações e erros. Verifique o ficheiro `server.log` na raiz do projeto para obter detalhes das operações.



