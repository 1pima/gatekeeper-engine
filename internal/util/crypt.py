import hashlib
import hmac
import os
import base64
from typing import Tuple

import hvac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class VaultCrypt:
    NONCE_LENGTH = 12
    DEK_LENGTH = 32

    def __init__(self):
        # todo убрать хранения ключа для хэширования из памяти, хранить в воулте либо инитить клиент hmac
        self._vault: hvac.Client = None
        self.master_key_name: str = None
        self._hmac_key: bytes = None

    def configure(self, hvac_url: str, token: str, master_key_name: str, hmac_key: str):
        self._vault = hvac.Client(url=hvac_url, token=token)
        self.master_key_name = master_key_name
        self._hmac_key = hmac_key.encode()

    def nonce(self):
        return os.urandom(self.NONCE_LENGTH)

    def _generate_dek_bytes(self):
        return os.urandom(self.DEK_LENGTH)

    @staticmethod
    def aes_gcm(dek_bytes):
        """Advanced Encryption Standard Galois/Counter Mode"""
        return AESGCM(dek_bytes)

    def encrypt(self, plaintext: str) -> Tuple[str, str]:
        # 1. генерируем dek ключ, nonce
        dek = self._generate_dek_bytes()
        nonce = self.nonce()

        # 2. шифруем данные, сохраняем ключ в vault
        encrypted_data_bytes = self.aes_gcm(dek).encrypt(nonce, plaintext.encode('utf-8'), None)
        encrypted_data_b64 = base64.b64encode(nonce + encrypted_data_bytes).decode('utf-8')
        dek_b64 = base64.b64encode(dek).decode('utf-8')
        vault_rs = self._vault.secrets.transit.encrypt_data( # noqa
            name=self.master_key_name,
            plaintext=dek_b64
        )

        # 3. отдаем зашифрованные данные и зашифрованный dek
        encrypted_dek = vault_rs['data']['ciphertext']
        return encrypted_data_b64, encrypted_dek

    def decrypt(self, encrypted_data: str, encrypted_dek: str) -> str:
        # 1. Расшифровываем dek
        vault_resp = self._vault.secrets.transit.decrypt_data( # noqa
            name=self.master_key_name,
            ciphertext=encrypted_dek
        )
        dek_bytes = base64.b64decode(vault_resp['data']['plaintext'])

        # 2. Достаем nonce и полезную нагрузку из b64
        raw_data = base64.b64decode(encrypted_data)
        nonce, payload = raw_data[:self.NONCE_LENGTH], raw_data[self.NONCE_LENGTH:]

        # 3. расшифровываем и отдаем результат
        return self.aes_gcm(dek_bytes).decrypt(nonce, payload, None).decode('utf-8')

    def rewrap_dek(self, encrypted_dek: str) -> str:
        """
        Функция для переупаковки старых DEK ключей в vault
        TODO необходимо использовать в будущей очереди для ротации ключей (раз в N (180?) дней)
        """
        vault_rs = self._vault.secrets.transit.rewrap_data( # noqa
            name=self.master_key_name,
            ciphertext=encrypted_dek
        )
        return vault_rs['data']['ciphertext']

    def generate_hash(self, data: str):
        """
        Генерация хэша, чтобы упростить поиск в бд по зашифрованным данным
        """
        return hmac.new(
            key=self._hmac_key,
            msg=data.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()


vault = VaultCrypt()
