import os
from collections import defaultdict
import math
import time

'''
def get_tokens(directory):
    print("Getting tokens from directory: ", directory, "/")

    # Diccionario para almacenar tokens
    tokens = defaultdict(list)

    # Recorrer los archivos en el directorio
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            doc_id = int(filename.split(".")[0].split("doc")[1])
            print("Reading file: ", filename, end=" --> ")
            print("doc_id: ", doc_id)

            filepath = os.path.join(directory, filename)
            
            # Leer el archivo
            with open(filepath, 'r', encoding='utf-8') as file:
                allContent = file.read()

                # Tokenizar el texto
                allContentSplited = allContent.split()

                # Agregar los tokens al diccionario
                for word in allContentSplited:
                    if doc_id not in tokens[word]:
                        tokens[word].append(doc_id)
    
    # Ordenar los tokens alfabéticamente
    tokens = dict(sorted(tokens.items()))

    return tokens
'''

def get_tokensV2(directory):
    print("Getting tokens from directory: ", directory, "/")

    # Diccionario para almacenar tokens
    tokens = defaultdict(list)

    # Recorrer los archivos en el directorio
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            doc_id = int(filename.split(".")[0].split("doc")[1])
            print("Reading file: ", filename, end=" --> ")
            print("doc_id: ", doc_id)

            filepath = os.path.join(directory, filename)

            # Leer el archivo línea por línea
            with open (filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    # Tokenizar el texto
                    allContentSplited = line.split()

                    # Agregar los tokens al diccionario
                    for word in allContentSplited:
                        if doc_id not in tokens[word]:
                            tokens[word].append(doc_id)
    
    # Ordenar los tokens alfabéticamente
    tokens = dict(sorted(tokens.items()))

    return tokens
    
def convert_to_distances(tokens):
    distances = {}
    for token, docs_id in tokens.items():
        # Ordenar los ids de los documentos
        docs_id_sorted = sorted(docs_id)
        
        # Calcular las distancias entre documentos consecutivos
        if docs_id_sorted:
            distances[token] = [docs_id_sorted[0]] + [docs_id_sorted[i] - docs_id_sorted[i - 1] for i in range(1, len(docs_id_sorted))]    
        else:
            distances[token] = []
    return distances       

def create_ptr_to_term_ptr_to_doc(tokens):
    # Create table: ptr_to_term
    token_keys = list(tokens.keys())

    concatenated_string_term = ""
    ptr_to_term = []

    current_index = 0
    for word in token_keys:
        concatenated_string_term += word
        ptr_to_term.append(current_index)
        current_index += len(word)
    
    # Create table: ptr_to_doc (Codificacion Gamma)
    ptr_to_doc = []
    concatenated_string_doc = ""
    current_index = 0

    for word, docs_id in tokens.items():
        #print()
        #print("[+] Docs_id: ", docs_id)

        concatenated_string_doc_temp = ""
        for doc_id in docs_id:
            

            if doc_id == 1:
                gama_code = '1'
            else:
                # Codificacion Gamma
                parteUnaria = '0' * ((math.floor(math.log2(doc_id)) + 1)-1) + '1'
                parteBinaria = bin(doc_id - (2 ** math.floor(math.log2(doc_id))))[2:]
                parteBinaria_completa = parteBinaria.zfill(math.floor(math.log2(doc_id)))
                gama_code = parteUnaria + parteBinaria_completa

            concatenated_string_doc_temp += gama_code
        #print("Gama code: ", concatenated_string_doc_temp)
        
        concatenated_string_doc += concatenated_string_doc_temp
        ptr_to_doc.append(current_index)
        current_index += len(concatenated_string_doc_temp)
    
    return concatenated_string_term, ptr_to_term, concatenated_string_doc, ptr_to_doc

def get_word_range(index, ptr_to_term, concatenated_string_term):
    start = ptr_to_term[index]
    end = ptr_to_term[index + 1] if index + 1 < len(ptr_to_term) else len(concatenated_string_term)
    return concatenated_string_term[start:end]

def search_word(concatenated_string_term, ptr_to_term, concatenated_string_doc, ptr_to_doc, word):
    print("Searching word: ", word)

    # ********* Tomar tiempo de inicio **************
    start_time = time.time()
    # **********************************************

    # ----------------- Busqueda de la palabra -----------------
    # --> Busqueda binaria en ptr_to_term y concatenated_string_term
    low, high = 0, len(ptr_to_term) - 1
    while low <= high:
        mid = (low + high) // 2

        current_word = get_word_range(mid, ptr_to_term, concatenated_string_term)

        if current_word == word:
            break
        elif current_word < word:
            low = mid + 1
        else:
            high = mid - 1
    
    indexFound = mid
    print("[+] Indice dentro de la tabla: ", indexFound)

    # --> Decodificador de Gamma
    codeGamma = get_word_range(indexFound, ptr_to_doc, concatenated_string_doc)
    print("[+] Gamma code (encoded): ", codeGamma)

    # Decodificar Gamma
    # Pasos:
    # Iniciamos leyendo los ceros hasta encontrar un 1, así obtenemos el valor k
    # Luego, leemos los k siguientes bits, y los que serán interpretados en su forma decimal x
    # Por último, hacemos la siguiente suma: 2**k + x dándonos así el valor N
    results = []
    index_gamma = 0

    while index_gamma < len(codeGamma):
        # Paso 1: Encontrar la posición del primer '1' y determinar k
        first_one_index = codeGamma.find('1', index_gamma)
        if first_one_index == -1:
            break # No hay más secuencias para procesar

        # Si el primer '1' está al final del string
        if first_one_index == len(codeGamma) - 1:
            results.append(1)
            break

        # Determinar k, que es el número de ceros antes del primer '1'  
        k = first_one_index - index_gamma

        # Paso 2: Leer los siguientes k bits después del primer '1'
        end_index = first_one_index + 1 + k

        # Si el rango de bits excede el tamaño del string, ajustarlo
        if end_index > len(codeGamma):
            end_index = len(codeGamma)

        following_bits = codeGamma[first_one_index + 1 : end_index]

        # Si following_bits está vacío, agregar el resultado especial
        if not following_bits:
            results.append(2**k)
        else:
            # Convertir los siguientes k bits a decimal
            x = int(following_bits, 2)
            # Calcular 2**k + x
            result = 2**k + x
            results.append(result)
        
        # Actualizar el índice para procesar la siguiente secuencia
        index_gamma = end_index
    
    #print("[+] Documentos encontrados (distancias): ", results)

    # --> Decodificar las distancias
    docs_id = []
    for i in range(len(results)):
        if i == 0:
            docs_id.append(results[i])
        else:
            docs_id.append(docs_id[i - 1] + results[i])
    
    print()
    print("[+] Documentos encontrados: ", docs_id)

    # ************** Tomar tiempo de fin **************
    end_time = time.time()
    # ***********************************************

    # Calcular tiempo de ejecución
    elapsed_time = end_time - start_time
    print()
    print("------------------------------------------------------")
    print("| Time of search: ", elapsed_time , " seconds")
    print("------------------------------------------------------")

if __name__ == "__main__":
    directory = "processed_documents"

    # ********* Tomar tiempo de inicio **************
    start_time = time.time()
    # ****************************************

    #tokens = get_tokens(directory)
    tokens = get_tokensV2(directory)

    #print()
    #print("Tokens obtained!")
    #for word, docs_id in tokens.items():
    #    print(word, " --> ", docs_id)

    tokens_distances = convert_to_distances(tokens)

    #print()
    #print("Tokens distances:")
    #for word, distances in tokens_distances.items():
    #    print(word, " --> ", distances)

    concatenated_string_term, ptr_to_term, concatenated_string_doc, ptr_to_doc = create_ptr_to_term_ptr_to_doc(tokens_distances)
    #print()
    #print("Concatenated string: ", concatenated_string_term)
    #print("ptr_to_term: ", ptr_to_term)

    #print()
    #print("Concatenated string: ", concatenated_string_doc)
    #print("ptr_to_doc: ", ptr_to_doc) 

    # ************** Tomar tiempo de fin **************
    end_time = time.time()
    # ***********************************************

    # Calcular tiempo de ejecución
    elapsed_time = end_time - start_time
    print()
    print("------------------------------------------------------")
    print("| Time to index: ", elapsed_time , " seconds")
    print("| Time to index: ", elapsed_time / 60 , " minutes")
    print("------------------------------------------------------")
    
    wordToSearch = "mother"
    print()
    search_word(concatenated_string_term, ptr_to_term, concatenated_string_doc, ptr_to_doc, wordToSearch)
    print()