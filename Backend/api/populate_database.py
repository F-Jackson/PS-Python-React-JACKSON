import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django

django.setup()

from django.core.files.images import ImageFile

from games.models import GamesModel


def populate():
    GamesModel.objects.all().delete()
    with open('mocks/products.json') as f:
        data = json.load(f)
        for item in data:
            img = ImageFile(open(f'mocks/assets/{item["image"]}', 'rb'))
            try:
                model = GamesModel.objects.create(
                    name=item['name'],
                    price=item['price'],
                    score=item['score'],
                )
                model.image = img
                model.save()
            except Exception as e:
                print(e)
            else:
                print('sucess')


if __name__ == "__main__":
    populate()
