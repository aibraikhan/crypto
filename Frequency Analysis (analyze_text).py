import re
from collections import Counter

def advanced_text_analysis(file_path, language='ru'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read().lower()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return
    except UnicodeDecodeError:
        # На случай, если файл сохранен в кодировке Windows-1251
        with open(file_path, 'r', encoding='cp1251') as file:
            raw_text = file.read().lower()

    # Извлечение букв и слов в зависимости от языка
    if language == 'ru':
        letters_only = re.sub(r'[^а-яё]', '', raw_text)
        words = re.findall(r'[а-яё]+', raw_text)
    elif language == 'kk':
        letters_only = re.sub(r'[^а-яёәіңғүұқөһ]', '', raw_text)
        words = re.findall(r'[а-яёәіңғүұқөһ]+', raw_text)
    else:
        print("Поддерживаемые языки: 'ru' или 'kk'")
        return

    # ==========================================
    # 1. ОБЩАЯ СТАТИСТИКА ТЕКСТА (Таблица 3)
    # ==========================================
    total_symbols = len(raw_text) # Считаем все символы, включая пробелы и знаки
    total_words = len(words)
    unique_words = len(set(words))
    
    if total_words > 0:
        lexical_richness = unique_words / total_words
        avg_word_length = sum(len(w) for w in words) / total_words
    else:
        lexical_richness = avg_word_length = 0

    print("\n" + "="*50)
    print("ОБЩАЯ СТАТИСТИКА")
    print("="*50)
    print(f"{'Параметр':<30} | {'Значение'}")
    print("-" * 50)
    print(f"{'Всего символов в тексте':<30} | {total_symbols:,}".replace(',', ' '))
    print(f"{'Всего слов (с повторами)':<30} | {total_words:,}".replace(',', ' '))
    print(f"{'Уникальных слов':<30} | {unique_words:,}".replace(',', ' '))
    print(f"{'Лексическое богатство':<30} | {lexical_richness:.3f}")
    print(f"{'Средняя длина слова':<30} | {avg_word_length:.2f} символа")

    # ==========================================
    # 2. ЧАСТОТА БУКВ (Таблица 2)
    # ==========================================
    total_letters = len(letters_only)
    letter_counts = Counter(letters_only)
    
    print("\n" + "="*50)
    print("ЧАСТОТА БУКВ (Топ-15)")
    print("="*50)
    print(f"{'#':<3} | {'Буква':<6} | {'Кол-во':<8} | {'% от всех'}")
    print("-" * 50)
    for i, (letter, count) in enumerate(letter_counts.most_common(15), 1):
        percent = (count / total_letters) * 100
        print(f"{i:<3} | {letter:<6} | {count:<8} | {percent:.2f}%")

    # ==========================================
    # 3. БИГРАММЫ СЛОВ (Таблица 1)
    # ==========================================
    # Создаем пары идущих подряд слов
    word_bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    total_bigrams = len(word_bigrams)
    bigram_counts = Counter(word_bigrams)

    print("\n" + "="*50)
    print("ЧАСТОТА БИГРАММ СЛОВ (Топ-15)")
    print("="*50)
    print(f"{'#':<3} | {'Биграмма':<20} | {'Кол-во':<8} | {'% от всех'}")
    print("-" * 50)
    for i, (bigram, count) in enumerate(bigram_counts.most_common(15), 1):
        percent = (count / total_bigrams) * 100 if total_bigrams > 0 else 0
        print(f"{i:<3} | {bigram:<20} | {count:<8} | {percent:.2f}%")

# ==========================================
# ЗАПУСК: 
# Обратите внимание на букву 'r' перед кавычками! Она решает проблему с ошибкой пути.
# ==========================================

# Укажите свой путь к файлу:
file_path = r'C:\Users\Алинур\Downloads\Преступление и наказание. Федор Достоевский.txt'

advanced_text_analysis(file_path, language='ru')