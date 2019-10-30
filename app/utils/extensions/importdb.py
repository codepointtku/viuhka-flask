#ignore
import json, requests

from sys import exit, argv
from os.path import exists
from app.services.models.service import Service, get_service_by_name, get_category_item_by_name
from app.services.models.category import get_categories, get_relation_type, get_category_by_category_items, Category, CategoryItems
from sqlalchemy.exc import DataError

class Import:
    def __init__(self):
        self.url = 'https://viuhka.turku.fi/employment/_search'
        if '--debug' in argv:
            if not exists('viuhka-data.json'):
                self.data = json.loads(requests.get(self.url, headers={'User-Agent':'PalveluViuhka python request'}).content.decode('utf-8'))
                json.dump(self.data, open('viuhka-data.json', 'w'), indent=4, sort_keys=True)
            else:
                try:
                    self.data = json.load(open('viuhka-data.json', 'r'))
                except json.decoder.JSONDecodeError:
                    print('Corrupt data, re-creating')
                    self.data = json.loads(requests.get(self.url, headers={'User-Agent':'PalveluViuhka python request'}).content.decode('utf-8'))
                    json.dump(self.data, open('viuhka-data.json', 'w'), indent=4, sort_keys=True)
        else:
            self.data = json.loads(requests.get(self.url, headers={'User-Agent':'PalveluViuhka python request'}).content.decode('utf-8'))


    def execute(self, app):
        count = 0
        with app.app_context():
            for hit in self.data['hits']['hits']:
                for key in hit:
                    if key == '_source':
                        try:
                            if get_service_by_name(hit[key]['name']):
                                continue
                            print('Creating service')
                            s = Service(
                                form = hit[key]
                            )
                            count += 1
                            print('Adding category items')
                            for value in hit[key]:
                                _categoryItems = []
                                if isinstance(hit[key][value], list):
                                    for item in hit[key][value]:
                                        cgItem = get_category_item_by_name(item)
                                        cgs = dict(enumerate(get_categories()))
                                        if not cgItem or cgItem is None:
                                            category = get_category_by_category_items(item)
                                            if not category or category is None:
                                                x = True
                                                while x:
                                                    try:
                                                        inp = int(input('No category found for item: %s\n[1] Create\n[2] Add to existing? ' % item))
                                                        x = False
                                                    except Exception as ex:
                                                        if isinstance(ex, KeyboardInterrupt):
                                                            exit(2)
                                                        print('1 or 2')
                                                if inp == 1:
                                                    name = input('Category name: ')
                                                    category = Category(
                                                        name = name
                                                    ).save()
                                                    cgs = dict(enumerate(get_categories()))
                                                elif inp == 2:
                                                    x = ''
                                                    for k in cgs:
                                                        x += '[%s] %s\n' % (k, cgs[k].name)
                                                    p = True
                                                    while p:
                                                        print(x)
                                                        inp = input('$ ')
                                                        try:
                                                            category = cgs[int(inp)]
                                                            p = False
                                                        except:
                                                            print('Invalid option')
                                                    print('Selected category: %s' % category.name)
                                                    CategoryItems(
                                                        category.id,
                                                        item
                                                    ).save()
                                                    print('Added %s to category %s' % (item, category.name))
                                            else:
                                                CategoryItems(
                                                    category.id,
                                                    item
                                                ).save()
                                                print('Added %s to category %s' % (item, category.name))
                                        else:
                                            category = get_category_by_category_items(cgItem.text)
                                            if not category or category is None:
                                                x = True
                                                while x:
                                                    try:
                                                        inp = int(input('No category found for item: %s\n[1] Create\n[2] Add to existing? ' % cgItem))
                                                        x = False
                                                    except Exception as ex:
                                                        if isinstance(ex, KeyboardInterrupt):
                                                            exit(2)
                                                        print('1 or 2')
                                                if inp == 1:
                                                    name = input('Category name: ')
                                                    category = Category(
                                                        name = name
                                                    ).save()                                                    
                                                    cgs = dict(enumerate(get_categories()))
                                                elif inp == 2:
                                                    x = ''
                                                    for k in cgs:
                                                        x += '[%s] %s\n' (k, cgs[k].name)
                                                    p = True
                                                    while p:
                                                        print(x)
                                                        inp = input('$ ')
                                                        try:
                                                            category = cgs[int(inp)]
                                                            p = False
                                                        except:
                                                            print('Invalid option')
                                                    CategoryItems(
                                                        category.id,
                                                        cgItem
                                                    )
                                                    print('Added %s to category %s' % (cgItem.text, category.name))
                                            else:
                                                CategoryItems(
                                                    category.id,
                                                    cgItem
                                                )
                                                
                                                print('Added %s to category %s' % (cgItem.text, category.name))
                                        _categoryItems.append(item)
                                if _categoryItems:
                                    s.category_items = _categoryItems
                            s.save()
                            print('Service added')
                                    

                        except DataError as ex:
                            print(ex)
                            column = str(ex).split('column')[1].split(' ')[1].replace('\'','')
                            print('Column: %s length: %s' % (column, len(hit[key][column])))
                            exit(2)
        if count > 0:
            print('Imported %u services to database' % count)