import argparse
import fitz
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

counter = Counter()

def obter_destinatario_e_nota(texto):
    padrao_destinatario = re.compile(r"Destinatário:\s*-\s*(.*?)\s*CPF/CNPJ:", re.DOTALL)
    correspondencia_destinatario = padrao_destinatario.search(texto)

    padrao_nota = re.compile(r"Nota fiscal N°\s*([\d.]+)", re.DOTALL)
    correspondencia_nota = padrao_nota.search(texto)

    destinatario = ""
    nota_fiscal = ""

    if correspondencia_destinatario:
        destinatario = correspondencia_destinatario.group(1).strip()
        destinatario = re.sub(r'[\\/*?:"<>|]', '', destinatario)

    if correspondencia_nota:
        nota_fiscal = correspondencia_nota.group(1).replace(".", "").strip()

    return destinatario, nota_fiscal

def processar_pagina(pdf_path, output_directory, pdf_document, pagina_num):
    pagina = pdf_document[pagina_num]
    texto = pagina.get_text()
    destinatario, nota_fiscal = obter_destinatario_e_nota(texto)

    counter_value = counter.increment()

    novo_caminho = os.path.join(output_directory, f"{nota_fiscal} - {counter_value} - {destinatario}.pdf")

    print(novo_caminho)

    novo_document = fitz.open()
    novo_document.insert_pdf(pdf_document, from_page=pagina_num, to_page=pagina_num)
    novo_document.save(novo_caminho)
    novo_document.close()

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

    elapsed_time = time.time() - start_time
    print(f"Tempo total de execução: {elapsed_time} segundos.")
