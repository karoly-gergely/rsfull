from django.db import models


class UrlRetrieveOnlyFileField(models.FileField):
    def _get_file(self):
        if self.url:
            return self.url
        return None

    def _set_file(self, file):
        self._file = file

    def _del_file(self):
        del self._file

    file = property(_get_file, _set_file, _del_file)
