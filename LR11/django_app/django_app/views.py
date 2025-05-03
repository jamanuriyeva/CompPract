from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def login(request):
    return JsonResponse({"author": "1147332"})

@csrf_exempt
def decypher(request):
    if request.method != 'POST':
        logger.warning('Attempt to access with method: %s', request.method)
        return JsonResponse(
            {"error": "Only POST method allowed"}, 
            status=405
        )

    # Проверка наличия файлов
    if 'key' not in request.FILES or 'secret' not in request.FILES:
        logger.error('Missing required files in request')
        return JsonResponse(
            {"error": "Both 'key' and 'secret' files are required"},
            status=400
        )

    try:
        # Чтение файлов
        key_file = request.FILES['key']
        secret_file = request.FILES['secret']

        key_data = key_file.read()
        secret_data = secret_file.read()

        # Проверка размера данных
        if len(secret_data) != 256:  # Для RSA 2048 бит
            logger.error('Invalid secret data size: %d', len(secret_data))
            return JsonResponse(
                {"error": "Invalid secret data size"},
                status=400
            )

        # Загрузка приватного ключа
        private_key = serialization.load_pem_private_key(
            key_data,
            password=None,
            backend=default_backend()
        )

        # Дешифровка
        decrypted = private_key.decrypt(
            secret_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        logger.info('Successfully decrypted data')
        return JsonResponse({
            "result": decrypted.decode('utf-8'),
            "status": "success"
        })

    except ValueError as e:
        logger.error('Value error during decryption: %s', str(e))
        return JsonResponse(
            {"error": "Invalid key or data format"},
            status=400
        )
    except Exception as e:
        logger.exception('Unexpected error during decryption')
        return JsonResponse(
            {"error": f"Decryption failed: {str(e)}"},
            status=500
        )