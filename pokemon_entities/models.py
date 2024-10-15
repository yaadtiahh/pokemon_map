from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='pokemons_imgs', null=True)

    def __str__(self):
        return '{}'.format(self.title)
