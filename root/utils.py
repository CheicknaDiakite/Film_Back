import os
import uuid
from django.utils.text import slugify


from django.utils.deconstruct import deconstructible

@deconstructible
class upload_to:
    """
    Génère un chemin de fichier dynamique et unique pour upload_to.
    """
    def __init__(self, directory):
        self.directory = directory

    def __call__(self, instance, filename):
        name, ext = os.path.splitext(filename)

        # Supprime les accents et caractères spéciaux
        name = slugify(name)

        # Nom unique
        filename = f"{name}-{uuid.uuid4().hex}{ext.lower()}"

        return os.path.join(self.directory, filename)