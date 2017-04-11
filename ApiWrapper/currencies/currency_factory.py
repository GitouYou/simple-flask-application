from .currency import Currency

'''
    função que funciona como uma fábrica de objetos
    dada uma moeda se ela for compatível ele retorna um objeto dessa moeda

    string name : nome de uma moeda
'''


def CurrencyFactory(name):
    if name.upper() == 'USD':
        return Currency('USD')
    if name.upper() == 'EUR':
        return Currency('EUR')
    if name.upper() == 'ARS':
        return Currency('ARS')
    if name.upper() == 'BRL':
        return Currency('BRL')
    if name.upper() == 'CAD':
        return Currency('CAD')
    else:
        raise RuntimeError("Invalid type of currency: %s", name)
