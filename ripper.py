import argparse
import fitz
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

def obter_destinatario(texto):
    padrao = re.compile(r"Destinatário:\s*-\s*(.*?)\s*CPF/CNPJ:", re.DOTALL)
    correspondencia = padrao.search(texto)

    if correspondencia:
        destinatario = correspondencia.group(1).strip()
        destinatario = re.sub(r'[\\/*?:"<>|]', '', destinatario)
        return destinatario
    else:
        return ""

def processar_pagina(pdf_path, output_directory, pdf_document, pagina_num):
    pagina = pdf_document[pagina_num]
    texto = pagina.get_text()
    destinatario = obter_destinatario(texto)

    novo_nome = f"{pagina_num + 1}_{destinatario}.pdf"
    novo_caminho = os.path.join(output_directory, novo_nome)

    novo_pdf = fitz.open()
    novo_pdf.insert_pdf(pdf_document, from_page=pagina_num, to_page=pagina_num)
    novo_pdf.save(novo_caminho)
    novo_pdf.close()

def separar_e_renomear(pdf_path, output_directory):
    pdf_document = fitz.open(pdf_path)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(processar_pagina, pdf_path, output_directory, pdf_document, pagina_num)
                   for pagina_num in range(pdf_document.page_count)]

        for future in futures:
            future.result()

    pdf_document.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Separar e renomear páginas de um PDF")
    parser.add_argument("-d", "--diretorio", required=True, help="Diretório contendo os PDFs")
    args = parser.parse_args()

    pdf_files = [f for f in os.listdir(args.diretorio) if f.endswith(".pdf")]

    for file_name in pdf_files:
        pdf_path = os.path.join(args.diretorio, file_name)
        output_directory = "dump/"

        start_time = time.time()
        separar_e_renomear(pdf_path, output_directory)
