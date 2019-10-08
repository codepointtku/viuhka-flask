from sys import argv, exit
from os.path import dirname, join, abspath
from os import sep, walk

from functools import reduce

from flask import Flask

from app.managers.login import login_manager


import json

ENV_IGNORE = [
    'SQL_USERNAME',
    'SQL_PASSWORD'
]

SQL_DEFAULTS = {
    'SQL_USERNAME':'root',
    'SQL_PASSWORD':'root',
    'SQL_HOST':'localhost',
    'SQL_PORT':'3306',
    'SQL_DATABASE':'default',
    'USE_BINDS':False
}

root = abspath(join(dirname(abspath(__file__)), '..', '..'))

app = None

def config(app):
    if '--prod' in argv:
        app.config.update(
            read_env(ignore=['DEBUG'])
        )
        app.config['SQLALCHEMY_ECHO'] = False
    else:
        app.config.update(
            read_env()
        )
        app.config['SQLALCHEMY_ECHO'] = '--quiet' not in argv

    database =  read_env('SQL_DATABASE').get('SQL_DATABASE')    if read_env('SQL_DATABASE').get('SQL_DATABASE') else SQL_DEFAULTS['SQL_DATABASE']
    username =  read_env('SQL_USERNAME').get('SQL_USERNAME')    if read_env('SQL_USERNAME').get('SQL_USERNAME') else SQL_DEFAULTS['SQL_USERNAME']
    password =  read_env('SQL_PASSWORD').get('SQL_PASSWORD')    if read_env('SQL_PASSWORD').get('SQL_PASSWORD') else SQL_DEFAULTS['SQL_PASSWORD']
    host =      read_env('SQL_HOST').get('SQL_HOST')            if read_env('SQL_HOST').get('SQL_HOST')         else SQL_DEFAULTS['SQL_HOST']
    port =      read_env('SQL_PORT').get('SQL_PORT')            if read_env('SQL_PORT').get('SQL_PORT')         else SQL_DEFAULTS['SQL_PORT']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'.format(
                                                username=username,
                                                password=password,
                                                host=host,
                                                port=port,
                                                database=database
                                            )


    if (read_env('USE_BINDS').get('USE_BINDS') if read_env('USE_BINDS').get('USE_BINDS') else SQL_DEFAULTS['USE_BINDS']):
        app.config['SQLALCHEMY_BINDS'] = {
                                        "{}": "mysql+pymysql://{username}:{password}@{host}:{port}/{}".format(
                                            username=username,
                                            password=password,
                                            host=host,
                                            port=port
                                        ), 
                                        "{}":"mysql+pymysql://{username}:{password}@{host}:{port}/{}".format(
                                            username=username,
                                            password=password,
                                            host=host,
                                            port=port
                                        )
                                    }
    for key in ENV_IGNORE:
        if key in app.config:
            app.config.pop(key)

    app.url_map.strict_slashes = False
    return app

def register_blueprints(app):
    dirs = get_directory_structure(
                                    root=join(root, 'app'),
                                    ignore=[
                                        'env',
                                        'Env',
                                        'venv',
                                        '.vscode',
                                        '__pycache__'
                                    ]
    )
    for folder in dirs['app']:
        for subfolder in dirs['app'][folder]:
            if subfolder == 'routes': #folder
                for blueprint in dirs['app'][folder][subfolder]:
                    if '__init__.py' in blueprint.split(sep):
                        continue
                    bpath = '.'.join(join('app', folder, subfolder, blueprint).split(sep)).replace('.py','')
                    try:
                        module = __import__(bpath, fromlist=['module'])
                        app.register_blueprint(module.module)
                        print('Route loaded: %s' % module._name_)
                    except Exception as ex:
                        print('Failed to load route <%s>: %s' % (bpath, ex))
            elif subfolder == 'routes.py':
                bpath = '.'.join(join('app', folder, subfolder).split(sep)).replace('.py','')
                module = __import__(bpath, fromlist=['module'])
                app.register_blueprint(module.module)
                print('Route loaded: %s' % module._name_)
    return app

def register_extensions(app):
    dirs = get_directory_structure(
                                    root=join(root, 'app', 'utils', 'extensions'),
                                    ignore=[
                                        'env',
                                        'Env',
                                        'venv',
                                        '.vscode',
                                        '__pycache__'
                                    ]
    )
    for file in dirs['extensions']:
        if file == '__init__.py':
            continue
        epath = '.'.join(join('app', 'utils', 'extensions', file).split(sep)).replace('.py', '')
        try:
            module = __import__(epath, fromlist=['module'])
            module.module.init_app(app)
            print('Extension loaded: %s' % module._name_)
        except Exception as ex:
            print('Failed to load extension: %s' % ex)
    return app



def create():
    app = register_blueprints(                                      \
            register_extensions(                                    \
                config(                                             \
                    Flask('__main__',                               \
                        static_folder=join(root, 'static'),         \
                        template_folder=join(root, 'templates'))    \
            )
        )
    )
    login_manager.init_app(app)
    return app




def find_extension(name):
    try:
        return app.extensions[name]
    except:
        return None

def find_blueprint(name):
    try:
        return app.blueprints[name]
    except:
        return None


def read_env(vars=[], ignore=[]):
    env = {}
    var_specific = len(vars) > 0
    try:
        for line in open(join(root, '.env')).read().split('\n'):
            if line:
                try:
                    key,value = line.split('=')
                    if var_specific and key in vars and key not in ignore:
                        env.update(
                            {
                                key.strip() : value.strip().replace('\'','')
                            }
                        )
                    else:
                        if key not in ignore:
                            env.update(
                                {
                                    key.strip() : value.strip().replace('\'','')
                                }
                            )
                except:
                    pass
    except FileNotFoundError:
        print('No env file to read.')
    return env


def get_directory_structure(root, ignore=[]):
    dir = {}
    root = root.rstrip(sep)
    start = root.rfind(sep) + 1
    for path, dirs, files in walk(root):
        if find(path, ignore):
            continue
        folders = path[start:].split(sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


def find(path, words=[]):
    for word in path.split(sep):
        if word in words:
            return True
    return False