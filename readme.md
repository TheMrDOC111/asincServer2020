# API Methods:

## 1)Get information
> Get information about one city.

**POST request**

### /getInformation

| Parameters  | Description |
| ------ | ----------- |
| geonameid   | Integer id of record in geonames database  |

**Response**

| Parameters  | Description |
| ------ | ----------- |
| geonameid   | string id of record in geonames database |
| name   | name of geographical point (utf8) varchar(200) |
| asciiname   | name of geographical point in plain ascii characters, varchar(200) |
| alternatenames   | alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000) |
| latitude   | latitude in decimal degrees (wgs84) |
| longitude   | longitude in decimal degrees (wgs84) |
| feature class   | see http://www.geonames.org/export/codes.html, char(1) |
| feature code   |see http://www.geonames.org/export/codes.html, varchar(10) |
| country code   | ISO-3166 2-letter country code, 2 characters |
| cc2   | alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters |
| admin1 code   | fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20) |
| admin2 code   | code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) |
| admin3 code   | code for third level administrative division, varchar(20) |
| admin4 code   | code for fourth level administrative division, varchar(20) |
| population   | bigint (8 byte int)  |
| elevation   | in meters, integer |
| dem   | digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat. |
| timezone   | the iana timezone id (see file timeZone.txt) varchar(40) |
| modification date   | date of last modification in yyyy-MM-dd format |

Example:
- Request 
``` python
{
   "geonameid": 451747
}
```
 - Response
 
``` python
{
"geonameid": "451747", "name": "Zyabrikovo", "asciiname": "Zyabrikovo", "alternatenames": "",
"latitude": "56.84665", "longitude": "34.7048", "feature class": "P", "feature code": "PPL",
"country code": "RU", "cc2": "", "admin1 code": "77", "admin2 code": "", "admin3 code": "", "admin4 code": "",
"population": "0", "elevation": "", "dem": "204", "timezone": "Europe/Moscow", "modification date": "2011-07-09"
}
```

## 2)Get more information
> Get information about one, two or more geonames.

**POST request**

### /getMoreInformation

| Parameters  | Description |
| ------ | ----------- |
| count   | count of geonames |
| geonameid   | array of id |



**Response**

| Parameters  | Description |
| ------ | ----------- |
| cities_information   | array of geonames information |
| lost_cities   | array of geonames which not found in database |

Example:
- Request 
``` python
{
    "count": 3,
    "geonameid": [451747, 874880, -1]
}
```
 - Response
 
``` python
{"cities_information": [
    {"geonameid": "451747", "name": "Zyabrikovo", "asciiname": "Zyabrikovo", "alternatenames": "",
     "latitude": "56.84665", "longitude": "34.7048", "feature class": "P", "feature code": "PPL", "country code": "RU",
     "cc2": "", "admin1 code": "77", "admin2 code": "", "admin3 code": "", "admin4 code": "", "population": "0",
     "elevation": "", "dem": "204", "timezone": "Europe/Moscow", "modification date": "2011-07-09"},
    {"geonameid": "874880", "name": "Urochishche Kamennyy Stolb", "asciiname": "Urochishche Kamennyy Stolb",
     "alternatenames": "", "latitude": "43.60472", "longitude": "40.31139", "feature class": "L",
     "feature code": "AREA", "country code": "RU", "cc2": "", "admin1 code": "38", "admin2 code": "", "admin3 code": "",
     "admin4 code": "", "population": "0", "elevation": "", "dem": "1925", "timezone": "Europe/Moscow",
     "modification date": "2005-07-20"}], 
"lost_cities": [-1]}
```


## 3)Get compare city
> Compare two geonames and return information about this geonames, more northerly one and timezone difference.   

**POST request**

### /getCompareCity

| Parameters  | Description |
| ------ | ----------- |
| city1   | Name in Russian language |
| city2   | Name in Russian language|

**Response**

| Parameters  | Description |
| ------ | ----------- |
| information   | array of two geonames information |
| equalTimeZone   | TRUE if timeZone not difference else FALSE  |
| differenceTime   | difference time |
| North  | which city more northerly |

Example:
- Request 
``` python
{
    "city1": 'Омск',
    "city2": 'Санкт-Петербург'
}
```
 - Response
 
``` python
{'information': [{'Омск': {'geonameid': '1496153', 'name': 'Omsk', 'asciiname': 'Omsk',
'alternatenames': "OMS,Om'sku,Omby,Omium,Oms'k,Omsc,Omsk,Omska,Omskas,Omszk,Omva,amsk,awmsk,e mu si ke,omseukeu,omska,
omusuku,xxm skh,Ομσκ,Омбы,Омва,Омск,Омськ,Омьскъ,Օմսկ,אומסק,أومسك,امسک,اومسک,ओम्स्क,ออมสค์,ომსკი,オムスク,鄂木斯克,옴스크",
'latitude': '54.99244', 'longitude': '73.36859', 'feature class': 'P',
'feature code': 'PPLA', 'country code': 'RU', 'cc2': '', 'admin1 code': '54',
'admin2 code': '', 'admin3 code': '', 'admin4 code': '', 'population': '1129281',
'elevation': '', 'dem': '90', 'timezone': 'Asia/Omsk',
'modification date': '2019-09-05'}}, 
{'Санкт-Петербург': {'geonameid': '536203', 'name': 'Sankt-Peterburg',
'asciiname': 'Sankt-Peterburg',
'alternatenames': 'Cathair Pheadair,Gorod-Geroy Leningrad,Leningrad,Léningrad,Peterburi,Petrograd,Piiteri,Pétrograd,
Saint Petersburg,Saint-Petersbourg,Saint-Pétersbourg,San Petersburgo,Sankt Petersburg,Sankt-Peterburg,St.-Petersburg,
Szentpetervar,Szentpétervár,leningeuladeu,sangteupeteleubuleukeu,senta pitarsabarga,Ленинград,Петроград,Санкт-Петербург,
সেন্ট পিটার্সবার্গ,레닌그라드,상트페테르부르크',
'latitude': '59.91667', 'longitude': '30.25', 'feature class': 'A',
'feature code': 'ADM1', 'country code': 'RU', 'cc2': '',
'admin1 code': '66', 'admin2 code': '', 'admin3 code': '',
'admin4 code': '', 'population': '5132000', 'elevation': '', 'dem': '0',
'timezone': 'Europe/Moscow', 'modification date': '2020-05-28'}}],
'equalTimeZone': False, 'differenceTime': 3.0, 'North': 'Санкт-Петербург'}
```

## 4)Get hints
> Geting hints 

**POST request**

### /getHints

| Parameters  | Description |
| ------ | ----------- |
| text   | pattern text |


**Response**

| Parameters  | Description |
| ------ | ----------- |
| hints   | array of hints |


Example:
- Request 
``` python
{
    "text": 'Мос'
}
```
 - Response
 
``` python
{'hints': [
          'Выборг ош', 'Выборгский район', 'Выборное', 'Выборлукашиха', 'Выборг', 'Выборге', 'Выбор',
          'Выборнеповка', 'Выборково'
          ]
}
```

## Error response
> Return _400 code_ and error message if request not correct  

**Response**

| Parameters  | Description |
| ------ | ----------- |
| error   | error message |
Example:
- Request for /getInformation path
``` python
{
    "name": 451747
}
```
 - Response
 
``` python
{
    'error': 'incorrect request'
}
```