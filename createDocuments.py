import os
import random
import string

# Configuración
num_documents = 10
num_words_per_document = 5
words_list = ["rojo", "amarillo", "verde", "azul", "blanco", "negro", "gris", "morado", "naranja", "rosa"]

def generate_random_word(length):
    """Genera una palabra aleatoria de longitud especificada."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_document(num_words, words_list):
    """Genera un documento con una combinación de palabras de la lista dada."""
    return [random.choice(words_list) for _ in range(num_words)]

def save_document(filename, lines):
    """Guarda el contenido en un archivo de texto."""
    with open(filename, 'w') as file:
        for line in lines:
            file.write(f"{line}\n")

# Crear documentos de prueba
os.makedirs("test_documents", exist_ok=True)

for i in range(1, num_documents + 1):
    document_name = f"test_documents/Doc{i}.txt"
    document_content = generate_document(num_words_per_document, words_list)
    save_document(document_name, document_content)

print(f"{num_documents} documentos de prueba generados en la carpeta 'test_documents'.")
