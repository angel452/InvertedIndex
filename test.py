def process_bit_string(bit_string):
    results = []
    index = 0
    
    while index < len(bit_string):
        # Paso 1: Encontrar la posición del primer '1' y determinar k
        first_one_index = bit_string.find('1', index)
        
        if first_one_index == -1:
            break  # No hay más secuencias para procesar
        
        # Si el primer '1' está al final del string
        if first_one_index == len(bit_string) - 1:
            results.append(1)
            break
        
        # Determinar k, que es el número de ceros antes del primer '1'
        k = first_one_index - index
        
        # Paso 2: Leer los siguientes k bits después del primer '1'
        end_index = first_one_index + 1 + k
        
        # Si el rango de bits excede el tamaño del string, ajustarlo
        if end_index > len(bit_string):
            end_index = len(bit_string)
        
        following_bits = bit_string[first_one_index + 1 : end_index]
        
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
        index = end_index
    
    return results

# Ejemplo de uso
bit_string = "000110100111"
results = process_bit_string(bit_string)
print(f"Números encontrados: {', '.join(map(str, results))}")

# Caso excepcional: solo un '1'
bit_string = "11"
results = process_bit_string(bit_string)
print(f"Números encontrados: {', '.join(map(str, results))}")

# Caso con cadena 10101
bit_string = "0101101011"
results = process_bit_string(bit_string)
print(f"Números encontrados: {', '.join(map(str, results))}")
