import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ЧАСТЬ 1: СЕРВЕР (ОРАКУЛ ЖЕРТВЫ)
class PaddingOracleServer:
    def __init__(self):
        # Сервер генерирует случайный секретный ключ
        self.key = os.urandom(16)
        
    def encrypt(self, plaintext):
        """Шифрует данные и выдает хакеру"""
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, 16))
        return iv, ciphertext

    def is_padding_valid(self, iv, ciphertext):
        """ 
        Возвращает True, если паддинг верный, и False, если битый.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        try:
            # Пытаемся снять паддинг. Если он кривой, вылетит ошибка (ValueError)
            unpad(decrypted, 16)
            return True
        except ValueError:
            return False

# ЧАСТЬ 2: ХАКЕР (АТАКУЮЩИЙ)
def padding_oracle_attack(oracle, iv, ciphertext):
    """
    Взламывает последний блок шифротекста байт за байтом
    """
    block_size = 16
    # Мы будем ломать первый блок шифротекста (поэтому меняем IV)
    target_block = ciphertext[:block_size]
    
    decrypted_block = bytearray(block_size)
    
    print("\n[+] Начинаем атаку на Оракула (взлом блока 16 байт)...")
    
    # Идем с конца блока (от 15-го байта к 0-му)
    for padding_val in range(1, block_size + 1):
        target_byte_index = block_size - padding_val
        
        # Перебираем все возможные варианты байта (от 0 до 255)
        for guess in range(256):
            # Создаем поддельный IV для отправки Оракулу
            forged_iv = bytearray(16)
            
            # Подготавливаем хвост поддельного IV так, чтобы там был нужный паддинг
            for i in range(target_byte_index + 1, block_size):
                forged_iv[i] = iv[i] ^ decrypted_block[i] ^ padding_val
                
            # Подставляем наш угадываемый байт
            forged_iv[target_byte_index] = iv[target_byte_index] ^ guess ^ padding_val
            
            # Спрашиваем Оракула: "Паддинг сошелся?"
            if oracle.is_padding_valid(bytes(forged_iv), target_block):
                # Если Оракул молчит (вернул True), мы угадали!
                decrypted_block[target_byte_index] = guess
                print(f"[*] Угадан байт [{target_byte_index}]: {chr(guess)} (Hex: {hex(guess)})")
                break
                
    return bytes(decrypted_block)

# ЗАПУСК ЭКСПЕРИМЕНТА
if __name__ == "__main__":
    # 1. Запускаем сервер
    oracle = PaddingOracleServer()
    
    # 2. Сервер шифрует супер-секретный текст
    secret_message = b"lesson14var4" # Ровно 16 байт для простоты примера
    iv, ciphertext = oracle.encrypt(secret_message)
    
    print("=== ИСХОДНЫЕ ДАННЫЕ ===")
    print(f"Перехваченный IV: {iv.hex()}")
    print(f"Перехваченный Шифротекст: {ciphertext.hex()}")
    
    # 3. Хакер проводит атаку (передаем только IV и шифротекст, ключ не передаем!)
    cracked_data = padding_oracle_attack(oracle, iv, ciphertext)
    
    print("\n=== РЕЗУЛЬТАТ ВЗЛОМА ===")
    print(f"Восстановленный текст: {cracked_data.decode('utf-8')}")
