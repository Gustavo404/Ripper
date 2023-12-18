# Script de Separação e Renomeação de Notas Fiscais

Este script em Python foi desenvolvido para automatizar a tarefa de separar um PDF contendo várias páginas de notas fiscais, onde cada página possui informações de destinatários diferentes. O script extrai o nome do destinatário de cada página e renomeia o arquivo PDF resultante com base nesse nome.

Pré-requisitos
- Python 3.xhistor
- Bibliotecas Python: PyMuPDF, pymupdf e fitz

Você pode instalar as bibliotecas necessárias executando o seguinte comando:

```bash
pip install PyPDF2 pymupdf fitz
```

# Como Usar

1. Clone ou faça o download deste repositório.
2. Abra um terminal e navegue até o diretório onde o script está localizado.
3. Execute o script usando o seguinte comando:

```bash
python ripper.py
```

O script solicitará o caminho do arquivo PDF que contém as notas fiscais. Certifique-se de fornecer o caminho correto para o seu arquivo.

Os PDFs renomeados serão salvos no diretório especificado no script.

Observações
- Certifique-se de que os destinatários estão formatados conforme esperado no PDF para garantir a extração correta do nome.
- Caso encontre problemas, ajuste a expressão regular na função obter_destinatario conforme necessário para o formato específico do seu PDF.
