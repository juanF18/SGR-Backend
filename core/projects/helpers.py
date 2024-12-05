import os
from django.utils.deconstruct import deconstructible


@deconstructible
class RenameFileWithProjectID:
    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, instance, filename):
        # Si el proyecto ya tiene un ID (cuando ya está guardado), usamos ese ID
        if instance.pk:
            project_id = instance.pk
        else:
            project_id = (
                "new_project"  # En caso de que no tenga un ID aún (durante la creación)
            )

        # Extraemos la extensión del archivo
        ext = filename.split(".")[-1]
        # Generamos el nuevo nombre del archivo con el ID del proyecto
        filename = f"{project_id}_{self.field_name}.{ext}"

        # Devolvemos la ruta donde se guardará el archivo
        return os.path.join(f"projects/{self.field_name}", filename)
