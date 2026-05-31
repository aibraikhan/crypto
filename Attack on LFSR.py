import random
import time

def get_lfsr_output(seed, mask, length, n_bits):
    state = seed
    seq = []
    for _ in range(n_bits):
        seq.append(state & 1)
        new_bit = bin(state & mask).count('1') % 2
        state = (state >> 1) | (new_bit << (length - 1))
    return seq

print("=== ПОДГОТОВКА СРЕДЫ ===")
mask1 = (1 << 10) | (1 << 9) | (1 << 7)  
mask2 = (1 << 7) | (1 << 4) | (1 << 1)   
mask3 = (1 << 6)                         

real_s1 = random.randint(1, 2**13 - 1)
real_s2 = random.randint(1, 2**15 - 1)
real_s3 = random.randint(1, 2**17 - 1)

print(f"Загаданы секретные Seed: LFSR-1={hex(real_s1)}, LFSR-2={hex(real_s2)}, LFSR-3={hex(real_s3)}\n")

seq1 = get_lfsr_output(real_s1, mask1, 13, 2000)
seq2 = get_lfsr_output(real_s2, mask2, 15, 2000)
seq3 = get_lfsr_output(real_s3, mask3, 17, 2000)

target_gamma = []
for i in range(2000):
    z = (seq1[i] & seq2[i]) ^ ((1 ^ seq1[i]) & seq3[i])
    target_gamma.append(z)

print("=== СТАРТ КОРРЕЛЯЦИОННОЙ АТАКИ (ПРО-ВЕРСИЯ) ===")

# --- Атака на LFSR-2 ---
print("Атака на LFSR-2 (15 бит)...")
start_time = time.time()
candidates_s2 = []

for s in range(1, 2**15):
    test_seq = get_lfsr_output(s, mask2, 15, 2000)
    matches = sum(1 for i in range(2000) if test_seq[i] == target_gamma[i])
    
    if matches / 2000 >= 0.73:
        candidates_s2.append(s)
        print(f"  [~] Подозреваемый LFSR-2: {hex(s)} (Совпадение: {matches/2000:.2%})")
print(f"Время: {time.time() - start_time:.2f} сек. Найдено кандидатов: {len(candidates_s2)}\n")

# --- Атака на LFSR-3 ---
print("Атака на LFSR-3 (17 бит)...")
start_time = time.time()
candidates_s3 = []

for s in range(1, 2**17):
    test_seq = get_lfsr_output(s, mask3, 17, 2000)
    matches = sum(1 for i in range(2000) if test_seq[i] == target_gamma[i])
    
    if matches / 2000 >= 0.73:
        candidates_s3.append(s)
        print(f"  [~] Подозреваемый LFSR-3: {hex(s)} (Совпадение: {matches/2000:.2%})")
print(f"Время: {time.time() - start_time:.2f} сек. Найдено кандидатов: {len(candidates_s3)}\n")

# --- Атака на LFSR-1 (финал) ---
print("Атака на LFSR-1 (13 бит) с перебором кандидатов...")
start_time = time.time()
found = False

# Перебираем все комбинации подозреваемых
for s2 in candidates_s2:
    seq2_test = get_lfsr_output(s2, mask2, 15, 2000)
    for s3 in candidates_s3:
        seq3_test = get_lfsr_output(s3, mask3, 17, 2000)
        
        for s1 in range(1, 2**13):
            test_seq1 = get_lfsr_output(s1, mask1, 13, 2000)
            is_correct = True
            
            for i in range(2000):
                z = (test_seq1[i] & seq2_test[i]) ^ ((1 ^ test_seq1[i]) & seq3_test[i])
                if z != target_gamma[i]:
                    is_correct = False
                    break
            
            if is_correct:
                print(f"\n[+] УСПЕХ! Взлом завершен. Истинные ключи:")
                print(f"    LFSR-1: {hex(s1)}")
                print(f"    LFSR-2: {hex(s2)}")
                print(f"    LFSR-3: {hex(s3)}")
                found = True
                break
        if found: break
    if found: break

if not found:
    print("[-] Ключи не найдены. Попробуйте снизить порог (например, до 0.72)")

print(f"\nВремя финального этапа: {time.time() - start_time:.2f} сек")