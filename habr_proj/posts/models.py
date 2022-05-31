from django.db import models


class PostCategory(models.Model):
    DESIGN = 'DS'
    WEB = 'WB'
    MOBILE = 'MB'
    MARKETING = 'MK'
    CATEGORIES = (
        (DESIGN, 'дизайн'),
        (WEB, 'веб-разработка'),
        (MOBILE, 'мобильная разработка'),
        (MARKETING, 'маркетинг'),
    )

    name = models.CharField(verbose_name="категория", max_length=2, choices=CATEGORIES)
    description = models.TextField(blank=True)
