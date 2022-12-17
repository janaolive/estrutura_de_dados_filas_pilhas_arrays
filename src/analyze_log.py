import csv


def analyze_log(path_to_file):
    if '.csv' not in path_to_file:
        raise FileNotFoundError(f'Extensão inválida. {path_to_file}')
    try:
        with open(path_to_file) as file:
            file_info = csv.reader(file)
            data = [item for item in file_info]
            days, clients, products = create_lists(data)
            orders = separate_clients_info(data, days, clients, products)
            most_requested_maria = maria_info(orders['maria'])
            hamburguer_arnaldo = orders['arnaldo']['orders']['hamburguer']
            never_requested_joao, nerver_was_joao = joao_info(orders['joao'])
            clients_infos(
                most_requested_maria,
                hamburguer_arnaldo,
                never_requested_joao,
                nerver_was_joao
            )
    except FileNotFoundError:
        raise FileNotFoundError(f'Arquivo inexistente. {path_to_file}')


def create_lists(data):
    days = []
    clients = []
    products = []
    for name, order, day in data:
        if day not in days:
            days.append(day)
        if name not in clients:
            clients.append(name)
        if order not in products:
            products.append(order)
    return [set(days), set(clients), set(products)]


def separate_clients_info(data, days, clients, products):
    orders = {
        client: {
            'orders': {
                product: 0 for product in products
            },
            'days': {
                day: 0 for day in days
            }
        } for client in clients
    }
    for name, order, day in data:
        orders[name]['orders'][order] += 1
        orders[name]['days'][day] += 1
    return orders


def maria_info(obj):
    most_requesties_maria = ''
    most_requesties_maria_quantity = 0
    for order, qnt in obj['orders'].items():
        if qnt > most_requesties_maria_quantity:
            most_requesties_maria = order
            most_requesties_maria_quantity = qnt
    return most_requesties_maria


def joao_info(obj):
    never_requesties = []
    nerver_was = []
    for order, qnt in obj['orders'].items():
        if not qnt:
            never_requesties.append(order)
    for day, qnt in obj['days'].items():
        if not qnt:
            nerver_was.append(day)
    return [set(never_requesties), set(nerver_was)]


def clients_infos(maria, arnaldo, joao_prod, joao_days):
    with open('data/mkt_campaign.txt', 'w') as file:
        string_to_write = f'{maria}\n{arnaldo}\n{joao_prod}\n{joao_days}'
        file.write(string_to_write)
