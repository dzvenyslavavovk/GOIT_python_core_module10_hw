from contacts_book_classes import AddressBook, Record

contacts = AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'User with such name is not available.'
        except ValueError:
            return 'Name and phone are not given.'
        except IndexError:
            return 'Name and phone are not given.'
    return inner

def hello():
    return 'How can I help you?'

@input_error
def add(contact):
    name, phones = split_info(contact)
    if name in contacts:
        raise ValueError('This contact already exists.')
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)   
    contacts.add_record(record)
    return f'Number {phone} with name {name} was added.'

@input_error
def change(contact):
    name, phone = split_info(contact)
    record = contacts[name]
    record.change_phones(phone)
    return f'Number {phone} with name {name} was changed.'


@input_error
def show_phone(contact):
    return contacts.search(contact.strip()).get_info()    

def show_all():
    if contacts:
        all_contacts = ''
        for key, record in contacts.get_all_record().items():
            all_contacts += f'{record.get_info()}\n'
        return all_contacts
    else:
        return 'There are no contacts.'


@input_error
def delete_contact(name):
    name = name.strip()
    contacts.remove_record(name)
    return "The contact was deleted."

def bye():
    return 'Good bye!'
    

def unknown_action():
    return 'Such command is not available'

COMMANDS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': show_phone,
    'show all': show_all,
    'delete': delete_contact,
    'good bye': bye,
    'exit': bye,
    'close': bye,
    '.':bye
    }

def change_input(user_input):
    new_input = user_input
    data = ''
    for key in COMMANDS:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            break
    if data:
        return reaction_func(new_input)(data)
    return reaction_func(new_input)()


def reaction_func(reaction):
    return COMMANDS.get(reaction, unknown_action)

def split_info(data):
    name, *phones = data.strip().split(' ')

    if name.isnumeric():
        raise ValueError('Wrong name.')
    for phone in phones:
        if not phone.isnumeric():
            raise ValueError('Wrong phones.')
    return name, phones


def main():
    print('Input one of this commands: hello, add (name phone), change (name phone), phone (phone), show all.')
    print('To stop the bot, input good bye, close, exit or .')
    while True:

        user_input = input('Input command: ')
        result = change_input(user_input)
        print(result)
        if result=='Good bye!':
            exit()

main()
