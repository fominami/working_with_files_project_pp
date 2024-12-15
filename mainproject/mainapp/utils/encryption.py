from cryptography.fernet import Fernet, InvalidToken


SIGNATURE = b'ENCRYPTED'

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()


def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = SIGNATURE + fernet.encrypt(data)
    return encrypted_data

def decrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    if not data.startswith(SIGNATURE):
        raise ValueError("Неверный формат данных или сигнатура отсутствует.")
    try:
        decrypted_data = fernet.decrypt(data[len(SIGNATURE):])
    except InvalidToken:
        raise ValueError("Не удалось расшифровать данные. Проверьте правильность ключа и формата данных.")
    return decrypted_data


def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)
    
    with open(file_path, "rb") as file:
        file_data = file.read()
    
    encrypted_data = SIGNATURE + fernet.encrypt(file_data)
    
    with open(file_path, "wb") as file:
        file.write(encrypted_data)
    
    print(f"Файл {file_path} зашифрован.")


def decrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)
    
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    
    if not encrypted_data.startswith(SIGNATURE):
        raise ValueError("Файл не зашифрован или сигнатура отсутствует.")
    
    try:
        decrypted_data = fernet.decrypt(encrypted_data[len(SIGNATURE):])
    except InvalidToken:
        raise ValueError("Не удалось расшифровать данные. Проверьте правильность ключа и формата данных.")
    
    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    
    print(f"Файл {file_path} расшифрован.")
