import osa

URL_TEMPERATURE = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
URL_CURRENCIES = 'http://www.webservicex.net/CurrencyConvertor.asmx?WSDL'
URL_DISTANCE = 'http://www.webservicex.net/length.asmx?WSDL'
TEMPERATURE_FILE = 'temps.txt'
CURRENCIES_FILE = 'currencies.txt'
TRAVEL_FILE = 'travel.txt'


def get_temperatures():
    values = []
    with open(TEMPERATURE_FILE, 'r') as file:
        for line in file.readlines():
            values.append(line.split(' ')[0])
    return values


def make_celsius(temperatures):
    client = osa.client.Client(URL_TEMPERATURE)
    celsius = []
    for day in temperatures:
        response = client.service.ConvertTemp(Temperature = day, FromUnit = 'degreeFahrenheit', ToUnit = 'degreeCelsius')
        celsius.append(response)
    return celsius


def parse_file(path):
    directions = {}
    with open(path, 'r') as file:
        for line in file:
            values = line.strip().split(' ')
            directions[values[0]] = [values[1], values[2]]
    return directions


def converte_in_rub(directions):
    client = osa.client.Client(URL_CURRENCIES)
    for flight, values in directions.items():
        response = client.service.ConversionRate(FromCurrency=values[1], ToCurrency='RUB')
        directions[flight] = [round(response * int(values[0]) + 0.5, 0), 'RUB']


def calculate_total_distance(directions):
    client = osa.client.Client(URL_DISTANCE)
    total_distance = 0
    for direction, values in directions.items():
        response = client.service.ChangeLengthUnit(LengthValue=values[0].replace(',', ''), fromLengthUnit='Miles', toLengthUnit='Kilometers')
        total_distance += response
    print(round(total_distance, 2))



fahrenheit = get_temperatures()
celsius = make_celsius(fahrenheit)
print(round(sum(celsius)/len(celsius), 1))

directions = parse_file(CURRENCIES_FILE)
converte_in_rub(directions)
print(directions)

directions_distance = parse_file(TRAVEL_FILE)
calculate_total_distance(directions_distance)

