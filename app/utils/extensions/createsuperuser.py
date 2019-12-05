#ignore

from sys                        import exit, argv
from getpass                    import getpass
from app.utils.models.account   import Account, find_account, find_account_by_username, find_account_by_email
from app.managers.password      import generate_hash_pass



class CreateSuperUser:
    def execute(self, app):
        with app.app_context():
            _pass = False
            while not _pass:
                username = input('Username: ')
                if len(username) <= 0:
                    print('Username required')
                    continue
                if find_account_by_username(username):
                    print('That account name already exists.')
                    continue
                break
            while not _pass:
                password = getpass()
                if len(password) < 6:
                    print('Secure password required')
                    continue
                break

            email = input('Email (optional): ')
            if email:
                if find_account_by_email(email):
                    print('That email already exists.')
                else:
                    _pass = True
                while not _pass:
                    try:
                        email = input('Email (optional): ')
                    except KeyboardInterrupt:
                        print()
                        break
                    if find_account_by_email(email):
                        print('That email already exists.')
                        continue
                    break

            a_r = Account(
                username=username,
                email=email,
                password=generate_hash_pass(username=username, password=password)
            ).save().rank()

            a_r.level = 2
            a_r.save()

            account = find_account(a_r.id)

            if account:
                print('Account created successfully')
            else:
                print('Failed to create account.')

            