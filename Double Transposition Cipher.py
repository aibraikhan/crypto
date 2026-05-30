def decrypt_block_cipher(ciphertext, key, keyv2):
    
    block_size = len(key)
    result = []
    
    # Идем по тексту шагами по 5 символов (размер блока)
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i : i + block_size]
        
        # Если блок неполный (меньше 5 символов), оставляем как есть
        if len(block) < block_size:
            result.append(block)
            continue
            
        # Переставляем буквы внутри блока согласно ключу
        # Для каждого индекса в ключе берем соответствующую букву из блока
        decrypted_block = "".join(block[k] for k in key)
        result.append(decrypted_block)

        # Переставляем буквы внутри блока согласно ключу
        # Для каждого индекса в ключе берем соответствующую букву из блока
    s_block = [result[k] for k in keyv2]
        
    return "".join(s_block)

# Исходные данные
text ="ОПЧУЛС_БООНЕВ_ОЖАЕОНЕЩЕИН"
key = [1, 0, 4, 3, 2]
keyv2 = [0, 2, 3, 1, 4]

decrypted_text = decrypt_block_cipher(text, key, keyv2)


print(f"Зашифрованный текст: {text}")
print(f"Расшифрованный текст: {decrypted_text}")# Исходные данные

text2 ="КЭЕ_ТДУМБ_НЕЗМАЬСЗЕДОР_ТУ"
key2 = [2, 4, 3, 1, 0]
key2v2 = [3, 4, 1, 0, 2]

decrypted_text2 = decrypt_block_cipher(text2, key2, key2v2)


print(f"Зашифрованный текст: {text2}")
print(f"Расшифрованный текст: {decrypted_text2}")