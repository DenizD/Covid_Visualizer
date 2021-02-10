## MAP TYPES
MAP_TYPES = ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'CartoDB positron', 'CartoDB dark_matter']

## COORDS LOCATION FILE
LOCATIONS_FILENAME = 'app/locations.txt'

## STATIC PATH
STATIC_PATH = 'app/static/'

## SESSION KEYs
SESSION_MAP_TYPE_KEY = 'mapType'
SESSION_COUNTRY_KEY = 'country'
SESSION_ACTIVE_COVID_STATS_KEY = 'activeCovidStats'

## COVID STATS KEYs
COVID_COUNTRY_KEY = 'Country,Other'
COVID_TOTAL_CASES_KEY = 'TotalCases'
COVID_NEW_CASES_KEY = 'NewCases'
COVID_TOTAL_DEATHS_KEY = 'TotalDeaths'
COVID_NEW_DEATHS_KEY = 'NewDeaths'
COVID_TOTAL_RECOVERED_KEY = 'TotalRecovered'
COVID_NEW_RECOVERED_KEY = 'NewRecovered'
COVID_ACTIVE_CASES_KEY = 'ActiveCases'
COVID_CRITICAL_CASES_KEY = 'Serious,Critical'
COVID_TOTAL_CASES_PER1M_KEY = 'TotCases/1M pop'
COVID_DEATHS_PER1M_KEY = 'Deaths/1M pop'
COVID_POPULATION_KEY = 'Population'
COVID_STATS = [COVID_TOTAL_CASES_KEY,
               COVID_NEW_CASES_KEY,
               COVID_TOTAL_DEATHS_KEY,
               COVID_NEW_DEATHS_KEY,
               COVID_TOTAL_RECOVERED_KEY,
               COVID_NEW_RECOVERED_KEY,
               COVID_ACTIVE_CASES_KEY,
               COVID_CRITICAL_CASES_KEY,
               COVID_TOTAL_CASES_PER1M_KEY,
               COVID_DEATHS_PER1M_KEY,
               COVID_POPULATION_KEY
               ]