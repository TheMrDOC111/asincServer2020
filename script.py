import asyncio
import email
from asyncio import StreamReader, StreamWriter
from io import StringIO
import json

config_keys = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'feature class',
               'feature code', 'country code', 'cc2', 'admin1 code', 'admin2 code', 'admin3 code', 'admin4 code',
               'population', 'elevation', 'dem', 'timezone', 'modification date']

legend = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
          'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
          'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': 'y', 'ы': 'y', 'ь': "'", 'э': 'e',
          'ю': 'yu', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh',
          'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S',
          'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': 'Y', 'Ы': 'Y',
          'Ь': "'", 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'}

timezone = {'Africa/Abidjan': 0.0, 'Africa/Accra': 0.0, 'Africa/Addis_Ababa': 3.0, 'Africa/Algiers': 1.0,
            'Africa/Asmara': 3.0, 'Africa/Bamako': 0.0, 'Africa/Bangui': 1.0, 'Africa/Banjul': 0.0,
            'Africa/Bissau': 0.0, 'Africa/Blantyre': 2.0, 'Africa/Brazzaville': 1.0, 'Africa/Bujumbura': 2.0,
            'Africa/Cairo': 2.0, 'Africa/Casablanca': 1.0, 'Africa/Ceuta': 1.0, 'Africa/Conakry': 0.0,
            'Africa/Dakar': 0.0, 'Africa/Dar_es_Salaam': 3.0, 'Africa/Djibouti': 3.0, 'Africa/Douala': 1.0,
            'Africa/El_Aaiun': 1.0, 'Africa/Freetown': 0.0, 'Africa/Gaborone': 2.0, 'Africa/Harare': 2.0,
            'Africa/Johannesburg': 2.0, 'Africa/Juba': 3.0, 'Africa/Kampala': 3.0, 'Africa/Khartoum': 2.0,
            'Africa/Kigali': 2.0, 'Africa/Kinshasa': 1.0, 'Africa/Lagos': 1.0, 'Africa/Libreville': 1.0,
            'Africa/Lome': 0.0, 'Africa/Luanda': 1.0, 'Africa/Lubumbashi': 2.0, 'Africa/Lusaka': 2.0,
            'Africa/Malabo': 1.0, 'Africa/Maputo': 2.0, 'Africa/Maseru': 2.0, 'Africa/Mbabane': 2.0,
            'Africa/Mogadishu': 3.0, 'Africa/Monrovia': 0.0, 'Africa/Nairobi': 3.0, 'Africa/Ndjamena': 1.0,
            'Africa/Niamey': 1.0, 'Africa/Nouakchott': 0.0, 'Africa/Ouagadougou': 0.0, 'Africa/Porto-Novo': 1.0,
            'Africa/Sao_Tome': 0.0, 'Africa/Tripoli': 2.0, 'Africa/Tunis': 1.0, 'Africa/Windhoek': 2.0,
            'America/Adak': -10.0, 'America/Anchorage': -9.0, 'America/Anguilla': -4.0, 'America/Antigua': -4.0,
            'America/Araguaina': -3.0, 'America/Argentina/Buenos_Aires': -3.0, 'America/Argentina/Catamarca': -3.0,
            'America/Argentina/Cordoba': -3.0, 'America/Argentina/Jujuy': -3.0, 'America/Argentina/La_Rioja': -3.0,
            'America/Argentina/Mendoza': -3.0, 'America/Argentina/Rio_Gallegos': -3.0, 'America/Argentina/Salta': -3.0,
            'America/Argentina/San_Juan': -3.0, 'America/Argentina/San_Luis': -3.0, 'America/Argentina/Tucuman': -3.0,
            'America/Argentina/Ushuaia': -3.0, 'America/Aruba': -4.0, 'America/Asuncion': -3.0,
            'America/Atikokan': -5.0, 'America/Bahia': -3.0, 'America/Bahia_Banderas': -6.0, 'America/Barbados': -4.0,
            'America/Belem': -3.0, 'America/Belize': -6.0, 'America/Blanc-Sablon': -4.0, 'America/Boa_Vista': -4.0,
            'America/Bogota': -5.0, 'America/Boise': -7.0, 'America/Cambridge_Bay': -7.0, 'America/Campo_Grande': -4.0,
            'America/Cancun': -5.0, 'America/Caracas': -4.0, 'America/Cayenne': -3.0, 'America/Cayman': -5.0,
            'America/Chicago': -6.0, 'America/Chihuahua': -7.0, 'America/Costa_Rica': -6.0, 'America/Creston': -7.0,
            'America/Cuiaba': -4.0, 'America/Curacao': -4.0, 'America/Danmarkshavn': 0.0, 'America/Dawson': -8.0,
            'America/Dawson_Creek': -7.0, 'America/Denver': -7.0, 'America/Detroit': -5.0, 'America/Dominica': -4.0,
            'America/Edmonton': -7.0, 'America/Eirunepe': -5.0, 'America/El_Salvador': -6.0,
            'America/Fort_Nelson': -7.0, 'America/Fortaleza': -3.0, 'America/Glace_Bay': -4.0, 'America/Godthab': -3.0,
            'America/Goose_Bay': -4.0, 'America/Grand_Turk': -5.0, 'America/Grenada': -4.0, 'America/Guadeloupe': -4.0,
            'America/Guatemala': -6.0, 'America/Guayaquil': -5.0, 'America/Guyana': -4.0, 'America/Halifax': -4.0,
            'America/Havana': -5.0, 'America/Hermosillo': -7.0, 'America/Indiana/Indianapolis': -5.0,
            'America/Indiana/Knox': -6.0, 'America/Indiana/Marengo': -5.0, 'America/Indiana/Petersburg': -5.0,
            'America/Indiana/Tell_City': -6.0, 'America/Indiana/Vevay': -5.0, 'America/Indiana/Vincennes': -5.0,
            'America/Indiana/Winamac': -5.0, 'America/Inuvik': -7.0, 'America/Iqaluit': -5.0, 'America/Jamaica': -5.0,
            'America/Juneau': -9.0, 'America/Kentucky/Louisville': -5.0, 'America/Kentucky/Monticello': -5.0,
            'America/Kralendijk': -4.0, 'America/La_Paz': -4.0, 'America/Lima': -5.0, 'America/Los_Angeles': -8.0,
            'America/Lower_Princes': -4.0, 'America/Maceio': -3.0, 'America/Managua': -6.0, 'America/Manaus': -4.0,
            'America/Marigot': -4.0, 'America/Martinique': -4.0, 'America/Matamoros': -6.0, 'America/Mazatlan': -7.0,
            'America/Menominee': -6.0, 'America/Merida': -6.0, 'America/Metlakatla': -9.0, 'America/Mexico_City': -6.0,
            'America/Miquelon': -3.0, 'America/Moncton': -4.0, 'America/Monterrey': -6.0, 'America/Montevideo': -3.0,
            'America/Montserrat': -4.0, 'America/Nassau': -5.0, 'America/New_York': -5.0, 'America/Nipigon': -5.0,
            'America/Nome': -9.0, 'America/Noronha': -2.0, 'America/North_Dakota/Beulah': -6.0,
            'America/North_Dakota/Center': -6.0, 'America/North_Dakota/New_Salem': -6.0, 'America/Ojinaga': -7.0,
            'America/Panama': -5.0, 'America/Pangnirtung': -5.0, 'America/Paramaribo': -3.0, 'America/Phoenix': -7.0,
            'America/Port-au-Prince': -5.0, 'America/Port_of_Spain': -4.0, 'America/Porto_Velho': -4.0,
            'America/Puerto_Rico': -4.0, 'America/Punta_Arenas': -3.0, 'America/Rainy_River': -6.0,
            'America/Rankin_Inlet': -6.0, 'America/Recife': -3.0, 'America/Regina': -6.0, 'America/Resolute': -6.0,
            'America/Rio_Branco': -5.0, 'America/Santarem': -3.0, 'America/Santiago': -3.0,
            'America/Santo_Domingo': -4.0, 'America/Sao_Paulo': -3.0, 'America/Scoresbysund': -1.0,
            'America/Sitka': -9.0, 'America/St_Barthelemy': -4.0, 'America/St_Johns': -3.5, 'America/St_Kitts': -4.0,
            'America/St_Lucia': -4.0, 'America/St_Thomas': -4.0, 'America/St_Vincent': -4.0,
            'America/Swift_Current': -6.0, 'America/Tegucigalpa': -6.0, 'America/Thule': -4.0,
            'America/Thunder_Bay': -5.0, 'America/Tijuana': -8.0, 'America/Toronto': -5.0, 'America/Tortola': -4.0,
            'America/Vancouver': -8.0, 'America/Whitehorse': -8.0, 'America/Winnipeg': -6.0, 'America/Yakutat': -9.0,
            'America/Yellowknife': -7.0, 'Antarctica/Casey': 8.0, 'Antarctica/Davis': 7.0,
            'Antarctica/DumontDUrville': 10.0, 'Antarctica/Macquarie': 11.0, 'Antarctica/Mawson': 5.0,
            'Antarctica/McMurdo': 13.0, 'Antarctica/Palmer': -3.0, 'Antarctica/Rothera': -3.0, 'Antarctica/Syowa': 3.0,
            'Antarctica/Troll': 0.0, 'Antarctica/Vostok': 6.0, 'Arctic/Longyearbyen': 1.0, 'Asia/Aden': 3.0,
            'Asia/Almaty': 6.0, 'Asia/Amman': 2.0, 'Asia/Anadyr': 12.0, 'Asia/Aqtau': 5.0, 'Asia/Aqtobe': 5.0,
            'Asia/Ashgabat': 5.0, 'Asia/Atyrau': 5.0, 'Asia/Baghdad': 3.0, 'Asia/Bahrain': 3.0, 'Asia/Baku': 4.0,
            'Asia/Bangkok': 7.0, 'Asia/Barnaul': 7.0, 'Asia/Beirut': 2.0, 'Asia/Bishkek': 6.0, 'Asia/Brunei': 8.0,
            'Asia/Chita': 9.0, 'Asia/Choibalsan': 8.0, 'Asia/Colombo': 5.5, 'Asia/Damascus': 2.0, 'Asia/Dhaka': 6.0,
            'Asia/Dili': 9.0, 'Asia/Dubai': 4.0, 'Asia/Dushanbe': 5.0, 'Asia/Famagusta': 2.0, 'Asia/Gaza': 2.0,
            'Asia/Hebron': 2.0, 'Asia/Ho_Chi_Minh': 7.0, 'Asia/Hong_Kong': 8.0, 'Asia/Hovd': 7.0, 'Asia/Irkutsk': 8.0,
            'Asia/Jakarta': 7.0, 'Asia/Jayapura': 9.0, 'Asia/Jerusalem': 2.0, 'Asia/Kabul': 4.5, 'Asia/Kamchatka': 12.0,
            'Asia/Karachi': 5.0, 'Asia/Kathmandu': 5.75, 'Asia/Khandyga': 9.0, 'Asia/Kolkata': 5.5,
            'Asia/Krasnoyarsk': 7.0, 'Asia/Kuala_Lumpur': 8.0, 'Asia/Kuching': 8.0, 'Asia/Kuwait': 3.0,
            'Asia/Macau': 8.0, 'Asia/Magadan': 11.0, 'Asia/Makassar': 8.0, 'Asia/Manila': 8.0, 'Asia/Muscat': 4.0,
            'Asia/Nicosia': 2.0, 'Asia/Novokuznetsk': 7.0, 'Asia/Novosibirsk': 7.0, 'Asia/Omsk': 6.0, 'Asia/Oral': 5.0,
            'Asia/Phnom_Penh': 7.0, 'Asia/Pontianak': 7.0, 'Asia/Pyongyang': 9.0, 'Asia/Qatar': 3.0,
            'Asia/Qostanay': 6.0, 'Asia/Qyzylorda': 5.0, 'Asia/Riyadh': 3.0, 'Asia/Sakhalin': 11.0,
            'Asia/Samarkand': 5.0, 'Asia/Seoul': 9.0, 'Asia/Shanghai': 8.0, 'Asia/Singapore': 8.0,
            'Asia/Srednekolymsk': 11.0, 'Asia/Taipei': 8.0, 'Asia/Tashkent': 5.0, 'Asia/Tbilisi': 4.0,
            'Asia/Tehran': 3.5, 'Asia/Thimphu': 6.0, 'Asia/Tokyo': 9.0, 'Asia/Tomsk': 7.0, 'Asia/Ulaanbaatar': 8.0,
            'Asia/Urumqi': 6.0, 'Asia/Ust-Nera': 10.0, 'Asia/Vientiane': 7.0, 'Asia/Vladivostok': 10.0,
            'Asia/Yakutsk': 9.0, 'Asia/Yangon': 6.5, 'Asia/Yekaterinburg': 5.0, 'Asia/Yerevan': 4.0,
            'Atlantic/Azores': -1.0, 'Atlantic/Bermuda': -4.0, 'Atlantic/Canary': 0.0, 'Atlantic/Cape_Verde': -1.0,
            'Atlantic/Faroe': 0.0, 'Atlantic/Madeira': 0.0, 'Atlantic/Reykjavik': 0.0, 'Atlantic/South_Georgia': -2.0,
            'Atlantic/St_Helena': 0.0, 'Atlantic/Stanley': -3.0, 'Australia/Adelaide': 10.5, 'Australia/Brisbane': 10.0,
            'Australia/Broken_Hill': 10.5, 'Australia/Currie': 11.0, 'Australia/Darwin': 9.5, 'Australia/Eucla': 8.75,
            'Australia/Hobart': 11.0, 'Australia/Lindeman': 10.0, 'Australia/Lord_Howe': 11.0,
            'Australia/Melbourne': 11.0, 'Australia/Perth': 8.0, 'Australia/Sydney': 11.0, 'Europe/Amsterdam': 1.0,
            'Europe/Andorra': 1.0, 'Europe/Astrakhan': 4.0, 'Europe/Athens': 2.0, 'Europe/Belgrade': 1.0,
            'Europe/Berlin': 1.0, 'Europe/Bratislava': 1.0, 'Europe/Brussels': 1.0, 'Europe/Bucharest': 2.0,
            'Europe/Budapest': 1.0, 'Europe/Busingen': 1.0, 'Europe/Chisinau': 2.0, 'Europe/Copenhagen': 1.0,
            'Europe/Dublin': 0.0, 'Europe/Gibraltar': 1.0, 'Europe/Guernsey': 0.0, 'Europe/Helsinki': 2.0,
            'Europe/Isle_of_Man': 0.0, 'Europe/Istanbul': 3.0, 'Europe/Jersey': 0.0, 'Europe/Kaliningrad': 2.0,
            'Europe/Kiev': 2.0, 'Europe/Kirov': 3.0, 'Europe/Lisbon': 0.0, 'Europe/Ljubljana': 1.0,
            'Europe/London': 0.0, 'Europe/Luxembourg': 1.0, 'Europe/Madrid': 1.0, 'Europe/Malta': 1.0,
            'Europe/Mariehamn': 2.0, 'Europe/Minsk': 3.0, 'Europe/Monaco': 1.0, 'Europe/Moscow': 3.0,
            'Europe/Oslo': 1.0, 'Europe/Paris': 1.0, 'Europe/Podgorica': 1.0, 'Europe/Prague': 1.0, 'Europe/Riga': 2.0,
            'Europe/Rome': 1.0, 'Europe/Samara': 4.0, 'Europe/San_Marino': 1.0, 'Europe/Sarajevo': 1.0,
            'Europe/Saratov': 4.0, 'Europe/Simferopol': 3.0, 'Europe/Skopje': 1.0, 'Europe/Sofia': 2.0,
            'Europe/Stockholm': 1.0, 'Europe/Tallinn': 2.0, 'Europe/Tirane': 1.0, 'Europe/Ulyanovsk': 4.0,
            'Europe/Uzhgorod': 2.0, 'Europe/Vaduz': 1.0, 'Europe/Vatican': 1.0, 'Europe/Vienna': 1.0,
            'Europe/Vilnius': 2.0, 'Europe/Volgograd': 4.0, 'Europe/Warsaw': 1.0, 'Europe/Zagreb': 1.0,
            'Europe/Zaporozhye': 2.0, 'Europe/Zurich': 1.0, 'Indian/Antananarivo': 3.0, 'Indian/Chagos': 6.0,
            'Indian/Christmas': 7.0, 'Indian/Cocos': 6.5, 'Indian/Comoro': 3.0, 'Indian/Kerguelen': 5.0,
            'Indian/Mahe': 4.0, 'Indian/Maldives': 5.0, 'Indian/Mauritius': 4.0, 'Indian/Mayotte': 3.0,
            'Indian/Reunion': 4.0, 'Pacific/Apia': 14.0, 'Pacific/Auckland': 13.0, 'Pacific/Bougainville': 11.0,
            'Pacific/Chatham': 13.75, 'Pacific/Chuuk': 10.0, 'Pacific/Easter': -5.0, 'Pacific/Efate': 11.0,
            'Pacific/Enderbury': 13.0, 'Pacific/Fakaofo': 13.0, 'Pacific/Fiji': 13.0, 'Pacific/Funafuti': 12.0,
            'Pacific/Galapagos': -6.0, 'Pacific/Gambier': -9.0, 'Pacific/Guadalcanal': 11.0, 'Pacific/Guam': 10.0,
            'Pacific/Honolulu': -10.0, 'Pacific/Kiritimati': 14.0, 'Pacific/Kosrae': 11.0, 'Pacific/Kwajalein': 12.0,
            'Pacific/Majuro': 12.0, 'Pacific/Marquesas': -9.5, 'Pacific/Midway': -11.0, 'Pacific/Nauru': 12.0,
            'Pacific/Niue': -11.0, 'Pacific/Norfolk': 12.0, 'Pacific/Noumea': 11.0, 'Pacific/Pago_Pago': -11.0,
            'Pacific/Palau': 9.0, 'Pacific/Pitcairn': -8.0, 'Pacific/Pohnpei': 11.0, 'Pacific/Port_Moresby': 10.0,
            'Pacific/Rarotonga': -10.0, 'Pacific/Saipan': 10.0, 'Pacific/Tahiti': -10.0, 'Pacific/Tarawa': 12.0,
            'Pacific/Tongatapu': 13.0, 'Pacific/Wake': 12.0, 'Pacific/Wallis': 12.0}


async def handle_connection(reader: StreamReader, writer: StreamWriter) -> None:
    data = ""
    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(256), timeout=2)
            if not chunk:
                break
            data += chunk.decode('UTF-8')
        except asyncio.exceptions.TimeoutError:
            break


    try:
        data, body = data.split('\r\n\r\n', 1)
        request, headers = data.split('\r\n', 1)
        headers = parse_headers(headers)
        headers['method'], headers['path'], headers['protocol'] = request.split()
        headers['body'] = json.loads(body)
    except json.decoder.JSONDecodeError:
        response = make_headers(400, 'Bad Request', error_message('incorrect request'))
        writer.write(response.encode('UTF-8'))
        await writer.drain()
        writer.close()
        return

    if headers['path'] == "/getInformation":
        response = get_information(headers['body'])
    elif headers['path'] == "/getMoreInformation":
        response = get_more_information(headers['body'])
    elif headers['path'] == "/getCompareCity":
        response = get_compare_city(headers['body'])
    elif headers['path'] == "/getHints":
        response = get_hints(headers['body'])
    else:
        response = make_headers(404, 'Path not found')

    writer.write(response.encode('UTF-8'))
    await writer.drain()
    writer.close()


def parse_headers(headers: str) -> dict:
    message = email.message_from_file(StringIO(headers))
    return dict(message.items())


def is_invalid_request(body: dict, *args):
    for arg in args:
        if arg not in body.keys() or body[arg] is None:
            return True
    return False


def make_latin(text: str) -> str:
    for i, j in legend.items():
        text = text.replace(i, j)
    return text


def make_headers(code: int, message: str, body=None) -> str:
    response = f'HTTP/1.1 {code} {message}\r\n'
    response += f'Connection: close\r\n'
    if body:
        response += f"Content-Length: {len(body)}\r\n\r\n"
        response += body
    return response


def error_message(message: str) -> str:
    return json.dumps({'error': message})


def get_information(body: dict) -> str:
    if is_invalid_request(body, 'geonameid'):
        return make_headers(400, 'Bad Request', error_message('incorrect request'))

    for geoname in geoname_data:
        if int(geoname['geonameid']) == body['geonameid']:
            return make_headers(200, 'OK', json.dumps(geoname))

    return make_headers(400, 'Bad Request', error_message('city not found'))


def get_more_information(body: dict) -> str:
    cities = []
    lost_cities = []

    if is_invalid_request(body, 'count', 'geonameid'):
        return make_headers(400, 'Bad Request', error_message('incorrect request'))

    if len(body['geonameid']) < body['count']:
        return make_headers(400, 'Bad Request', error_message('out of bounds'))

    for i in range(body['count']):
        found = False
        for geoname in geoname_data:
            if int(geoname['geonameid']) == body['geonameid'][i]:
                cities.append(geoname)
                found = True
                break
        if not found:
            lost_cities.append(body['geonameid'][i])

    return make_headers(200, 'OK', json.dumps({"cities_information": cities, "lost_cities": lost_cities}))


def get_compare_city(body: dict) -> str:
    if is_invalid_request(body, 'city1', 'city2'):
        return make_headers(400, 'Bad Request', error_message('incorrect request'))

    latin_name1 = make_latin(body['city1'])
    latin_name2 = make_latin(body['city2'])

    city1 = None
    city2 = None

    for geoname in geoname_data:
        if latin_name1 == geoname['asciiname']:
            if city1 is not None:
                if int(city1['population']) < int(geoname['population']):
                    city1 = geoname
            else:
                city1 = geoname

        if latin_name2 == geoname['asciiname']:
            if city2:
                if int(city2['population']) < int(geoname['population']):
                    city2 = geoname
            else:
                city2 = geoname

    if city1 is None:
        return make_headers(400, 'Bad Request', error_message(body['city1'] + " not found"))

    if city2 is None:
        return make_headers(400, 'Bad Request', error_message(body['city2'] + " not found"))

    message = {'information': [{body['city1']: city1}, {body['city2']: city2}],
               'equalTimeZone': city1['timezone'] == city2['timezone'],
               'differenceTime': abs(timezone[city1['timezone']] - timezone[city2['timezone']]),
               'North': body['city1'] if city1['longitude'] < city2['longitude'] else body['city2']}
    return make_headers(200, 'OK', json.dumps(message))


def get_hints(body: dict) -> str:
    if is_invalid_request(body, 'text'):
        return make_headers(400, 'Bad Request', error_message('incorrect request'))

    text = body['text']

    hints = set()
    for geoname in geoname_data:
        if geoname['name'].startswith(text):
            hints.add(geoname['name'])

        if geoname['asciiname'].startswith(text):
            hints.add(geoname['name'])

        for elem in geoname['alternatenames'].split(','):
            if elem.startswith(text):
                hints.add(elem)

    return make_headers(200, 'OK', json.dumps({'hints': list(hints)}))


if __name__ == '__main__':
    geoname_data = []
    file = open("RU.txt", 'r', encoding='UTF-8')
    print('Reading file...')
    for line in file:
        geoname_data.append(dict(zip(config_keys, [i.strip() for i in line.split('\t')])))
    print('Reading file complete')

    loop = asyncio.get_event_loop()
    server_gen = asyncio.start_server(handle_connection, '127.0.0.1', port=8000, loop=loop)
    server = loop.run_until_complete(server_gen)
    print('Listening established on {0}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        server.close()
        loop.close()
