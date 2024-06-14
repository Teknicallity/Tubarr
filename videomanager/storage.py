from django.core.files.storage import FileSystemStorage


class ExistingFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Prevent Django from modifying the file name
        return name

    def _save(self, name, content):
        # Prevent Django from saving the file again
        return name
