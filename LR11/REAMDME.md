# Лабораторная работа 11

## Требования к решению
1. Фреймворк Flask или FastAPI или любой другой Python-framework (микро-фреймворк - без развесистой структуры файлов и папок внутри)
2. Формат ответа по маршруту `/login`: `{"author": "__ваш логин__"}`
3. Реализация дополнительных решений более чем с 1 фреймворком (варианты: Node.js, Django, Go)
4. Реализация фронтэнда и отправка данных на сервер с использованием какого-либо фронтэнд-фреймворка или библиотеки (Vue.js, Svelte, React)
5. Вывод и отображение исходного текста на страницу с формой (без перезагрузки страницы, асинхронно)

## FastAPI

### Запуск через консоль

![1](https://github.com/jamanuriyeva/CompPract/blob/2cd9f98343207fb8abd27dd2082b5d9b3ad0d9ab/LR11/pics/fastapi-run.png)

### Страница

![2](https://github.com/jamanuriyeva/CompPract/blob/2cd9f98343207fb8abd27dd2082b5d9b3ad0d9ab/LR11/pics/fastapi-page.png)

### Результат

Для расшифровки текста необходимо выбрать файл с ключом (private_key.pem) и файл с зашифрованным текстом (encrypted_data.bim). После нажатия на кнопку текст асинхронно расшифровывается

![3](https://github.com/jamanuriyeva/CompPract/blob/2cd9f98343207fb8abd27dd2082b5d9b3ad0d9ab/LR11/pics/fastapi-result.png)

## Django

### /login

![4](https://github.com/jamanuriyeva/CompPract/blob/2cd9f98343207fb8abd27dd2082b5d9b3ad0d9ab/LR11/pics/django-login.png)

### /decypher

![5](https://github.com/jamanuriyeva/CompPract/blob/2cd9f98343207fb8abd27dd2082b5d9b3ad0d9ab/LR11/pics/django-curl.png)

## Комментарий

Для проверки работоспособности сервиса необходимы были два файла private_key.pem и encrypted_data.bim. Чтобы их с легкостью получить была разработана программа.


Создается пара ключей: приватный (private_key) и публичный (public_key)

Приватный ключ сохраняется в файл private_key.pem

Формат: PEM (текстовый формат) без пароля (NoEncryption)

Используется схема шифрования OAEP (оптимальная асимметричная защита)

Зашифрованные данные (бинарные) сохраняются в файл encrypted_data.bin

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
# Генерация ключей
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()
# Сохраняем приватный ключ в PEM формате
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
# Текст для шифрования
message = b"I am no hater, yeah, we in the same whip. The only difference is that you do not own it"
# Шифруем сообщение
encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
# Сохраняем зашифрованные данные
with open("encrypted_data.bin", "wb") as f:
    f.write(encrypted)
print("Файлы успешно созданы:")
print("1. private_key.pem - приватный ключ")
print("2. encrypted_data.bin - зашифрованные данные")```
