import transliterate


def slugify(slug):
    url = transliterate.translit(slug, 'ru', reversed=True).replace(' ', '-')
    return url