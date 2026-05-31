import urllib.request
import urllib.parse
import json
import re
import random
import math
from collections import defaultdict

# ==========================================
# 1. ТВОЙ ИСХОДНЫЙ ШИФР
# ==========================================
cipher_text = """
15 22 67 30 93 49 22 94 65 94 44 49, 49 39 51 22 75 49 41 11 15 22 49
11 53 51 75 51 78 94, 44 49 27 51 22 67 44 86 51, 26 49 39 51 75 “78 45 94 – 62
75 – 78 11 51 44 49 78 91 49 22 72 14”, 94 11 67 26 93 5 1 44 51 90 67 93 51 44
94 11 67 53 75 67 41 49 45 94 11 49 93 15 30 35 49 15 67 11 67 14, 44 51 45 78
49 11 65 94 14 44 94 86 49 86 94 41 15 20 75 53 75 94 26 67 11, 44 51 53 67 78
67 26 75 51 11 49 11 65 94 14, 35 22 67 51 90 67 15 39 51 75 22 58 53 75 51 27
72 11 49 51 22 15 67 11 15 51 39 44 51 53 67 78 49 93 51 86 88 11 67 27 75 49
26 51 27 51 15 53 93 67 22 44 67 90 67 35 51 75 44 67 90 67 53 75 94 26 75 49 86
49, 44 51 26 44 49 20 18 51 90 67 45 49 93 67 15 22 94.
67 35 51 75 51 78 44 67 14 45 51 15 22 86 67 39 49 44 78 94 75 49 - 94
39 49 26 88 75 15 11 94 86 94 44 90 67 39 94 15 22 75 49 65 94 93 67 14 53 51
75 51 27 51 45 86 49 39 94 78 11 94 44 88 93 94 15 58 11 53 51 75 51 78. 26 78 51
15 58 41 11 49 22 49 93 67 53 75 67 45 51 86 22 67 75 67 11, 36 67 44 49 75 51 14
94 86 75 67 44 65 22 51 14 44 67 11 15 90 94 75 93 30 44 78 49 39 94 93 49 39
53, 44 67 44 51 75 51 49 93 58 44 67 14 26 49 78 49 35 51 14 27 72 93 67 27 72
67 15 11 51 22 94 22 58 11 15 20 27 49 26 88. 67 15 22 49 11 49 93 67 15 58 44
51 39 49 93 67 53 67 93 67 15 94 53 30 22 51 44 22 51 39 44 67 22 72, 86 67 22
67 75 88 20 44 51 26 11 49 44 72 51 90 67 15 22 94 94 15 53 67 93 58 26 67 11 49
93 94 39 49 15 22 51 75 15 86 94. 11 15 51 27 93 94 45 51 86 15 49 39 67 93 51
22 88, 27 93 94 45 51, 27 93 94 45 51, 67 44 11 72 75 49 15 22 49 51 22 44 49
90 93 49 26 49 41, 44 49 11 94 15 49 51 22 44 49 78 90 67 93 67 11 67 14, 88 45
51 53 75 51 86 75 49 15 44 67 15 93 72 65 44 67, 86 49 86 35 49 15 67 11 67 14
67 22 15 86 88 86 94 44 88 78 94 22 53 67 78 44 67 15 44 51 26 44 49 86 67 39
88 20 39 51 93 67 78 94 20, 53 67 15 93 51 78 44 20 20 11 15 11 67 51 14 45 94
26 44 94...
22 94 41 67 44 58 86 67 18 51 93 86 44 88 93 27 51 15 65 88 39 44 72 14 53
94 15 22 67 93 51 22 - 94 39 51 93 67 78 94 30 67 27 67 75 11 49 93 49 15 58,
35 49 15 67 11 67 14 53 67 78 93 67 39 94 93 15 30 11 86 67 93 51 44 86 49 41,
44 67 88 53 49 15 22 58 44 51 88 15 53 51 93, 94 15 11 67 20 49 11 22 67 39
49 22 94 35 51 15 86 88 20 11 94 44 22 67 11 86 88 44 51 11 72 75 67 44 94 93.
78 11 51 22 51 44 94, 27 51 15 65 88 39 44 67 11 72 44 72 75 44 88 11 94 26 -53
67 78 36 20 26 51 93 30 45 49, 53 67 78 41 11 49 22 94 93 94 51 90 67 94 88 11
67 93 67 86 93 94 44 49 78 75 88 90 88 20 15 22 67 75 67 44 88, 11 22 51 39
44 67 22 88.
"""

# ==========================================
# 2. ОБУЧЕНИЕ НА БОЛЬШИХ ДАННЫХ (КВАДРОГРАММЫ)
# ==========================================
def fetch_massive_corpus():
    print("[1/4] Выкачиваю тонну текста из Википедии для базы (около 15 секунд)...")
    # Берем самые длинные статьи, чтобы покрыть максимум слов
    articles = ["Россия", "СССР", "Российская_империя", "Русский_язык", "Пушкин,_Александр_Сергеевич", "Вторая_мировая_война"]
    corpus = ""
    for title in articles:
        url = f"https://ru.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(title)}&format=json"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                for page_id in data['query']['pages']:
                    corpus += data['query']['pages'][page_id].get('extract', '') + " "
        except Exception:
            continue
            
    if len(corpus) < 50000:
        print("[ОШИБКА] Не удалось скачать текст. Проверь интернет!")
        exit()
    return corpus.upper()

def build_quadgrams(corpus):
    print(f"[2/4] Анализирую текст ({len(corpus)} символов). Строю квадрограммы...")
    # Убираем все пробелы, потому что в твоем шифре слова слиплись
    text = re.sub(r'[^А-ЯЁ]', '', corpus)
    ngrams = defaultdict(int)
    
    for i in range(len(text) - 3):
        ngrams[text[i:i+4]] += 1
        
    N = sum(ngrams.values())
    for key in ngrams:
        ngrams[key] = math.log10(float(ngrams[key]) / N)
    
    floor = math.log10(0.01 / N) # Суровый штраф за бессмыслицу
    return ngrams, floor

# ==========================================
# 3. АГРЕССИВНЫЙ АЛГОРИТМ ВЗЛОМА
# ==========================================
def get_score(text_letters, ngrams, floor):
    score = 0
    # Проверяем текст окнами по 4 буквы
    for i in range(len(text_letters) - 3):
        score += ngrams.get(text_letters[i] + text_letters[i+1] + text_letters[i+2] + text_letters[i+3], floor)
    return score

def format_final_text(cipher, key_dict):
    # Красиво собирает финальный текст, оставляя знаки препинания на местах
    return re.sub(r'\d+', lambda m: key_dict.get(m.group(0), "_"), cipher)

def crack_cipher():
    corpus = fetch_massive_corpus()
    ngrams, floor = build_quadgrams(corpus)
    
    print("[3/4] Модель заряжена. Начинаю жесткий перебор...")
    numbers = re.findall(r'\d+', cipher_text)
    unique_numbers = list(set(numbers))
    alphabet = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
    
    global_best_score = -99e9
    global_best_key = {}
    
    print("[4/4] Идет взлом (30 глубоких проходов). Подожди немного...")
    
    # 30 независимых попыток, чтобы не застрять в "тупике"
    # Увеличиваем количество попыток с 30 до 100!
    for attempt in range(1, 101):
        random.shuffle(alphabet)
        current_key = {num: alphabet[i] for i, num in enumerate(unique_numbers)}
        current_text = [current_key[n] for n in numbers]
        best_score = get_score(current_text, ngrams, floor)
        
        stagnation = 0
        # Заставляем его мутировать дольше: не 2000, а 5000 шагов без улучшений
        while stagnation < 5000:
            n1, n2 = random.sample(unique_numbers, 2)
            
            current_key[n1], current_key[n2] = current_key[n2], current_key[n1]
            test_text = [current_key[n] for n in numbers]
            test_score = get_score(test_text, ngrams, floor)
            
            if test_score > best_score:
                best_score = test_score
                stagnation = 0
            else:
                current_key[n1], current_key[n2] = current_key[n2], current_key[n1]
                stagnation += 1
                
        # Теперь он будет отчитываться о КАЖДОМ проходе, даже если он неудачный
        if best_score > global_best_score:
            global_best_score = best_score
            global_best_key = current_key.copy()
            preview = format_final_text(cipher_text, global_best_key)[:40]
            print(f"  [🏆 РЕКОРД] Попытка {attempt}/100 | Счет: {best_score:.1f} -> {preview}...")
        else:
            # Выводим серым/обычным текстом попытки, которые не побили рекорд
            print(f"  [-] Попытка {attempt}/100 завершена (Счет: {best_score:.1f} - хуже рекорда)")
                
        if best_score > global_best_score:
            global_best_score = best_score
            global_best_key = current_key.copy()
            preview = format_final_text(cipher_text, global_best_key)[:50]
            print(f"  [+] Попытка {attempt}/30 — Новый рекорд! ({best_score:.1f}) -> {preview}...")

 
    print("\n ШИФР ВЗЛОМАН: \n")
 
    print(format_final_text(cipher_text, global_best_key))

if __name__ == "__main__":
    crack_cipher()