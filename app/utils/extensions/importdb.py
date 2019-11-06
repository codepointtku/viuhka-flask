#ignore

import json
import requests

from sys import exit, argv
from os.path import exists
from app.services.models.service import Service, get_service_by_name, get_category_item_by_name
from app.services.models.category import get_categories, get_relation_type, get_category_by_category_items, Category, CategoryItems, get_category_by_name
from sqlalchemy.exc import DataError
from .html_parser import strip_tags

CATEGORY_IDS = {
    'target': 'Neuvonta- ja ohjauspalvelut',
    'service_path': 'Koulutuspalvelut',
    'classification': 'Työllistymisedellytyksiä lisäävät palvelut',
    'immigration': 'Työnhaku- ja työnvälityspalvelut',
    'age_group': 'Yrittäjyyspalvelut',
    'unemployment_duration': 'Terveys-, kuntoutus- ja sosiaalipalvelut',
    'health': 'Muut palvelut',
    'integration': 'Palveluja kohderyhmittäin'
}


class Import:
    def __init__(self):
        self.urls = ['https://viuhka.turku.fi/employment/_search?size=1000']
        self.data = []
        if '--debug' in argv:
            if not exists('viuhka-data.json'):
                for url in self.urls:
                    self.data.append(json.loads(requests.get(url, headers={
                                     'User-Agent': 'PalveluViuhka python request'}).content.decode('utf-8')))
                json.dump(self.data, open('viuhka-data.json', 'w'),
                          indent=4, sort_keys=True)
            else:
                try:
                    self.data = json.load(open('viuhka-data.json', 'r'))
                except json.decoder.JSONDecodeError:
                    print('Corrupt data, re-creating')
                    for url in self.urls:
                        self.data.append(json.loads(requests.get(url, headers={
                                         'User-Agent': 'PalveluViuhka python request'}).content.decode('utf-8')))
                    json.dump(self.data, open('viuhka-data-%s.json', 'w'), indent=4, sort_keys=True)
        else:
            for url in self.urls:
                self.data.append(json.loads(requests.get(url, headers={
                                 'User-Agent': 'PalveluViuhka python request'}).content.decode('utf-8')))

    def execute(self, app):
        count = 0
        with app.app_context():
            for data in self.data:
                for hit in data['hits']['hits']:
                    for key in hit:
                        if key == '_source':
                            try:
                                if get_service_by_name(hit[key]['name']):
                                    continue
                                print('Creating service')
                                s = Service(
                                    form=hit[key]
                                )
                                count += 1
                                print('Adding category items')
                                for value in hit[key]:
                                    _categoryItems = []
                                    if isinstance(hit[key][value], list):
                                        for item in hit[key][value]:
                                            try:
                                                if isinstance(item, int):
                                                    item = str(item)
                                                cgItem = get_category_item_by_name(
                                                    item)
                                            except Exception as ex:
                                                continue
                                            cgs = dict(enumerate(get_categories()))
                                            if not cgItem or cgItem is None:
                                                print(
                                                    'Look up for category: %s' % value)
                                                try:
                                                    category = get_category_by_name(
                                                        CATEGORY_IDS[value])
                                                except:
                                                    category = get_category_by_category_items(
                                                        item)
                                                if not category or category is None:
                                                    x = True
                                                    while x:
                                                        try:
                                                            inp = int(input(
                                                                'No category found for item: %s\n[1] Create\n[2] Add to existing? ' % item))
                                                            x = False
                                                        except Exception as ex:
                                                            if isinstance(ex, KeyboardInterrupt):
                                                                exit(2)
                                                            print('1 or 2')
                                                    if inp == 1:
                                                        name = input(
                                                            'Category name: (Default: %s) ' % CATEGORY_IDS[value])
                                                        if not name or name is None:
                                                            name = CATEGORY_IDS[value]
                                                        category = Category(
                                                            name=name,
                                                            skip_csrf_check=True
                                                        ).save()
                                                        cgs = dict(
                                                            enumerate(get_categories()))
                                                    elif inp == 2:
                                                        print('\n'*50)
                                                        x = ''
                                                        for k in cgs:
                                                            x += '[%s] %s\n' % (
                                                                k, cgs[k].name)
                                                        p = True
                                                        while p:
                                                            print(x)
                                                            inp = input('$ ')
                                                            if inp.lower() == 'exit':
                                                                exit(2)
                                                            try:
                                                                category = cgs[int(
                                                                    inp)]
                                                                p = False
                                                            except:
                                                                print(
                                                                    'Invalid option, type exit to exit')
                                                        print(
                                                            'Selected category: %s' % category.name)
                                                        CategoryItems(
                                                            category.id,
                                                            item
                                                        ).save()
                                                        print('Added %s to category %s' % (
                                                            item, category.name))
                                                else:
                                                    CategoryItems(
                                                        category.id,
                                                        item
                                                    ).save()
                                                    print('Added %s to category %s' % (
                                                        item, category.name))
                                            else:
                                                try:
                                                    category = get_category_by_name(
                                                        CATEGORY_IDS[value])
                                                except:
                                                    category = get_category_by_category_items(
                                                        cgItem.text)
                                                if not category or category is None:
                                                    x = True
                                                    while x:
                                                        try:
                                                            inp = int(input(
                                                                'No category found for item: %s\n[1] Create\n[2] Add to existing? ' % cgItem))
                                                            x = False
                                                        except Exception as ex:
                                                            if isinstance(ex, KeyboardInterrupt):
                                                                exit(2)
                                                            print('1 or 2')
                                                    if inp == 1:
                                                        name = input(
                                                            'Category name: (Default: %s) ' % CATEGORY_IDS[value])
                                                        if not name or name is None:
                                                            name = CATEGORY_IDS[value]
                                                        category = Category(
                                                            name=name,
                                                            skip_csrf_check=True
                                                        ).save()
                                                        cgs = dict(
                                                            enumerate(get_categories()))
                                                    elif inp == 2:
                                                        print('\n'*50)
                                                        x = ''
                                                        for k in cgs:
                                                            x += '[%s] %s\n' (k,
                                                                              cgs[k].name)
                                                        p = True
                                                        while p:
                                                            print(x)
                                                            inp = input('$ ')
                                                            if inp.lower() == 'exit':
                                                                exit(2)
                                                            try:
                                                                category = cgs[int(
                                                                    inp)]
                                                                p = False
                                                            except:
                                                                print(
                                                                    'Invalid option, type exit to exit.')
                                                        CategoryItems(
                                                            category.id,
                                                            cgItem
                                                        )
                                                        print('Added %s to category %s' % (
                                                            cgItem.text, category.name))
                                                else:
                                                    CategoryItems(
                                                        category.id,
                                                        cgItem
                                                    )
                                                    print('Added %s to category %s' % (
                                                        cgItem.text, category.name))
                                            _categoryItems.append(item)
                                    if _categoryItems:
                                        s.category_items = _categoryItems
                                s.save()
                                print('Service added')
                            except DataError as ex:
                                print(ex)
                                column = str(ex).split('column')[1].split(
                                    ' ')[1].replace('\'', '')
                                print('Column: %s length: %s' %
                                      (column, len(hit[key][column])))
                                exit(2)
        if count > 0:
            print('Imported %u services to database' % count)
