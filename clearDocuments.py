import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Configuración
input_directory = "unprocessed_documents"
output_directory = "processed_documents"

def rename_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    files.sort()

    for index, filename in enumerate(files):
        new_name = f"doc{index + 1}.txt"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
    
    print(f"Archivos renombrados en la carpeta '{directory}'.")

def process_text(text):
    # Convertir a minúsculas
    text = text.lower()

    # Eliminar signos de puntuacion
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Eliminar números
    text = text.translate(str.maketrans('', '', string.digits))

    # Tokenizar el texto
    tokens = word_tokenize(text)

    # Eliminar stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words and len(word) >= 3]

    # Lematizacion o Stemming
    lemmatizer = WordNetLemmatizer()
    filtered_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Añadir saltos de línea
    processed_lines = []
    for i in range(0, len(filtered_tokens), 100):
        line = ' '.join(filtered_tokens[i:i + 100])
        processed_lines.append(line)
        #print(line)

    # Unir los tokens en un solo string
    return '\n'.join(processed_lines)

def process_document(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open (os.path.join(input_dir, filename), 'r') as file:
                content = file.read()
            
            processed_content = process_text(content)

            with open(os.path.join(output_dir, filename), 'w') as file:
                file.write(processed_content)
    
    print(f"Documentos procesados guardados en la carpeta '{output_dir}'.")

#rename_files(input_directory)

process_document(input_directory, output_directory)