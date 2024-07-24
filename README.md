# CSVReader
### Descrição do Projeto

Este projeto consiste em um script Python desenvolvido para automatizar o download de vídeos e arquivos de legenda a partir de uma lista de URLs fornecidas em um arquivo CSV. Foi solicitado pelo meu superior no trabalho para facilitar a gestão de conteúdo multimídia. O script oferece suporte para baixar vídeos em diferentes formatos, como MP3 e MP4, e também para capturar arquivos de legenda (SRT) associados aos vídeos.

### Funcionalidades Principais

- **Leitura de Arquivo CSV:** O script começa lendo um arquivo CSV que contém uma lista de URLs e outros metadados. Ele valida a existência do arquivo e a integridade dos dados antes de iniciar o processo de download.

- **Verificação de URLs:** Utiliza expressões regulares para validar as URLs fornecidas, garantindo que apenas links válidos sejam processados.

- **Download de Vídeos e Legendas:** Com base nas URLs válidas, o script faz o download dos vídeos nos formatos especificados (MP3 ou MP4) e de arquivos de legenda em SRT. Ele utiliza diferentes User Agents para simular requisições de diferentes navegadores, aumentando a eficiência do download.

- **Gestão de Arquivos e Diretórios:** O script cria pastas organizadas para armazenar os arquivos baixados, utilizando nomes derivados das URLs e garantindo que não haja caracteres inválidos nos nomes dos diretórios.

- **Tratamento de Erros e Tentativas de Download:** Implementa um sistema de tentativas múltiplas para downloads falhos, com um tempo de espera crescente entre as tentativas, até um máximo de cinco tentativas.

### Como Usar

1. **Configuração dos Caminhos:** Defina os caminhos para o arquivo CSV (`caminho_csv`) e para o diretório de armazenamento dos downloads (`caminho_hd`).

2. **Execução do Script:** Execute o script `main()` para iniciar o processo de download. O script irá ler o CSV, validar os links, e baixar os arquivos correspondentes, organizando-os em pastas.

3. **Logs e Erros:** O script fornece feedback detalhado sobre o progresso dos downloads, incluindo logs de erros e status de arquivos já existentes.
