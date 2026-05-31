import itertools

# Частотные биграммы русского языка (для оценки правильности текста)
# Чем больше совпадений, тем вероятнее, что текст расшифрован верно.
COMMON_BIGRAMS = {
    'ОЕ', 'ЕИ', 'НА', 'РА', 'СТ', 'НО', 'ЕН', 'ТО', 'ГЛ', 'ПД', 
    'КО', 'НИ', 'ОВ', 'ВО', 'ПО', 'ЛО', 'ПР', 'РО', 'ТЬ', 'ЕС',
    'ОМ', 'КА', 'РЕ', 'ДЕ', 'ЛЕ', 'КЛ', 'СЬ', 'УЧ', 'ЧЕ'
}

def score_text(text):
    """Оценивает текст: начисляет очки за наличие частых русских слогов"""
    score = 0
    clean_text = text.replace('_', '') # Убираем разделители для анализа
    for i in range(len(clean_text) - 1):
        bigram = clean_text[i:i+2]
        if bigram in COMMON_BIGRAMS:
            score += 1
    return score

def break_cipher(ciphertext, block_size):
    """
    Пытается взломать шифр двойной перестановки полным перебором.
    """
    n_blocks = len(ciphertext) // block_size
    
    # Генерируем ВСЕ возможные варианты ключей
    # range(5) -> [0, 1, 2, 3, 4]
    possible_keys_intra = list(itertools.permutations(range(block_size)))
    possible_keys_inter = list(itertools.permutations(range(n_blocks)))
    
    best_score = -1
    best_text = ""
    best_keys = ([], [])

    # 1. Перебираем все варианты перестановки ВНУТРИ блоков
    for k1 in possible_keys_intra:
        
        # Предварительная расшифровка внутри блоков
        temp_blocks = []
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i : i + block_size]
            if len(block) == block_size:
                decoded_block = "".join(block[k] for k in k1)
                temp_blocks.append(decoded_block)
            else:
                temp_blocks.append(block)
        
        # Если количество блоков не совпадает с ожидаемым для перестановки, пропускаем
        if len(temp_blocks) != n_blocks:
            continue

        # 2. Перебираем все варианты перестановки САМИХ блоков
        for k2 in possible_keys_inter:
            try:
                final_blocks = [temp_blocks[k] for k in k2]
                candidate_text = "".join(final_blocks)
                
                # Оцениваем полученный текст
                current_score = score_text(candidate_text)
                
                if current_score > best_score:
                    best_score = current_score
                    best_text = candidate_text
                    best_keys = (k1, k2)
            except IndexError:
                continue

    return best_text, best_keys

# --- ЗАПУСК ВЗЛОМА ---

text1 = "ОПЧУЛС_БООНЕВ_ОЖАЕОНЕЩЕИН"
print(f"Взламываем: {text1}")
result, keys = break_cipher(text1, block_size=5)
print(f"Результат: {result}")
print(f"Найденные ключи: Внутри={keys[0]}, Блоки={keys[1]}\n")

text2 = "КЭЕ_ТДУМБ_НЕЗМАЬСЗЕДОР_ТУ"
print(f"Взламываем: {text2}")
result2, keys2 = break_cipher(text2, block_size=5)
print(f"Результат: {result2}")
print(f"Найденные ключи: Внутри={keys2[0]}, Блоки={keys2[1]}\n")