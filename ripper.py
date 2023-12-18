import fitz
import os
import re

def separar_e_renomear(pdf_path, output_directory):
    # Abre o PDF usando PyMuPDF
    pdf_document = fitz.open(pdf_path)

    # Cria o diretório de saída se não existir
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for pagina_num in range(pdf_document.page_count):
        # Obtém os dados do destinatário da página
        pagina = pdf_document[pagina_num]
        texto = pagina.get_text()
        destinatario = obter_destinatario(texto)

        # Renomeia o arquivo usando o nome do destinatário
        novo_nome = f"Nota_{destinatario}.pdf"
        novo_caminho = os.path.join(output_directory, novo_nome)

        # Salva a página como um novo PDF usando PyMuPDF
        novo_pdf = fitz.open()
        novo_pdf.insert_pdf(pdf_document, from_page=pagina_num, to_page=pagina_num)
        novo_pdf.save(novo_caminho)
        novo_pdf.close()

    # Fecha o documento original
    pdf_document.close()

def obter_destinatario(texto):
    # Procura o padrão "Destinatário:" seguido pelo nome do destinatário
    padrao = re.compile(r"Destinatário:\s*-\s*(.*?)\s*CPF/CNPJ:", re.DOTALL)
    correspondencia = padrao.search(texto)

    if correspondencia:
        destinatario = correspondencia.group(1).strip()

        # Remove caracteres inválidos para nome de arquivo
        destinatario = re.sub(r'[\\/*?:"<>|]', '', destinatario)

        return destinatario
    else:
        # Se não encontrar um padrão correspondente, retorna uma string vazia
        return ""


if __name__ == "__main__":
    pdf_path = "NFE1.pdf"
    output_directory = "dump/"
    separar_e_renomear(pdf_path, output_directory)
