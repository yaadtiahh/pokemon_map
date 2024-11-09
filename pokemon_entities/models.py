from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон."""
    title = models.CharField(max_length=200, verbose_name='Название на рус.')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название на англ.')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Название на яп.')

    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='pokemons_imgs', null=True, verbose_name='Изображение')

    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolution",
        verbose_name='Эволюция'
    )

    def __str__(self):
        return str(self.title)


class PokemonEntity(models.Model):
    """Данные о покемоне."""
    lat = models.FloatField(null=True, verbose_name='Широта')
    lon = models.FloatField(null=True, verbose_name='Долгота')

    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Время начала')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Время окончания')

    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    atack = models.IntegerField(null=True, blank=True, verbose_name='Урон')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Броня')
    endurance = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон'
    )

    def __str__(self):
        return str(self.pokemon)
