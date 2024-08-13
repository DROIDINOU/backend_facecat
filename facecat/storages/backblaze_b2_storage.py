import b2sdk.v2 as b2sdk  # Importer le module b2sdk v2
from django.core.files.storage import Storage
from django.conf import settings
from django.core.files.base import ContentFile
from b2sdk.v2 import InMemoryAccountInfo, B2Api  # Importer les classes nécessaires
import os

class BackblazeB2Storage(Storage):
    def __init__(self, *args, **kwargs):
        self.b2_client = self._create_b2_client()
        self.bucket = self.b2_client.get_bucket_by_name(settings.B2_BUCKET_NAME)
    
    def _create_b2_client(self):
        info = InMemoryAccountInfo()  # Utilisation correcte de InMemoryAccountInfo
        print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu",info)
        b2_api = B2Api(info)  # Utilisation de B2Api avec InMemoryAccountInfo pour la gestion de l'authentification
        b2_api.authorize_account(
            'https://api003.backblazeb2.com',
            settings.B2_KEY_ID,
            settings.B2_APPLICATION_KEY,

        )
        return b2_api

    def _get_file_key(self, name):
        # Nettoyage du nom de fichier pour le rendre compatible avec Backblaze B2
        cleaned_name = name.replace('\\', '/')
        cleaned_name = os.path.basename(cleaned_name)
        return cleaned_name

    def _save(self, name, content):
        file_key = self._get_file_key(name)
        with content.open('rb') as file:
            self.bucket.upload_bytes(file.read(), file_key)
        return file_key

    def _open(self, name, mode='rb'):
        file_key = self._get_file_key(name)
        file_info = self.bucket.get_file_info(file_key)
        return ContentFile(file_info.download(), name)

    def exists(self, name):
        """
        Vérifie si un fichier avec le nom donné existe dans le bucket Backblaze B2.
        """
        try:
            file_version = self.bucket.get_file_info_by_name(name)
            return file_version is not None
        except b2sdk.exception.FileNotPresent:
            return False

    def url(self, name):
        file_key = self._get_file_key(name)
        return f"https://f003.backblazeb2.com/file/{settings.B2_BUCKET_NAME}/{file_key}"
