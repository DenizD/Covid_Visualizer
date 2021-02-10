import covid_daily
import folium
from geopy.geocoders import Nominatim
from app.config import constants
from datetime import datetime

class CovidStats:

   def read_locations_from_file(self):
      with  open(constants.LOCATIONS_FILENAME) as myFile:
         content = myFile.readlines()
      content = [x.strip() for x in content]
      self.countries = [field.split(':')[0] for field in content]
      locations = [field.split(':')[1] for field in content]
      locations = [(float(coord.split()[0]), float(coord.split()[1])) for coord in locations]
      self.nCountries = len(self.countries)
      self.countryLocations = dict(zip(self.countries, locations))


   def write_locations_to_file(self, country):
      if self.geolocator is None:
         self.geolocator = Nominatim(user_agent="covid visualizer")

      location = self.geolocator.geocode(constants.LOCATIONS_FILENAME)
      latitude = location.latitude
      longitude = location.longitude

      with  open(constants.LOCATIONS_FILENAME, 'a') as myFile:
         myFile.write('%s:%f %f\n' % (country, latitude, longitude))


   def __init__(self):
      self.data = covid_daily.overview(as_json=False)[0:-1]
      self.read_locations_from_file()
      self.covidData = {}
      self.calculate_map_style_metrics()


   # scales the data for better visualization on the map such that max value is 1000000 for each covid stat
   # different colormap for each covid stats
   def calculate_map_style_metrics(self):
      self.covidScaleVal = {}
      self.covidColor = {}
      for statName in constants.COVID_STATS:
         self.covidScaleVal[statName] = float(1000000.0) / float(self.data[statName][1:].max())

      self.covidColor[constants.COVID_TOTAL_CASES_KEY] = 'orange'
      self.covidColor[constants.COVID_NEW_CASES_KEY] = 'darkorange'
      self.covidColor[constants.COVID_TOTAL_DEATHS_KEY] = 'red'
      self.covidColor[constants.COVID_NEW_DEATHS_KEY] = 'darkred'
      self.covidColor[constants.COVID_TOTAL_RECOVERED_KEY] = 'green'
      self.covidColor[constants.COVID_NEW_RECOVERED_KEY] = 'darkgreen'
      self.covidColor[constants.COVID_ACTIVE_CASES_KEY] = 'yellow'
      self.covidColor[constants.COVID_CRITICAL_CASES_KEY] = 'purple'
      self.covidColor[constants.COVID_TOTAL_CASES_PER1M_KEY] = 'pink'
      self.covidColor[constants.COVID_DEATHS_PER1M_KEY] = 'crimson'
      self.covidColor[constants.COVID_POPULATION_KEY] = 'blue'


   def init_map(self, activeMapType='OpenStreetMap'):
      self.lastUpdatedTime = None
      self.map = folium.Map(location=[43.681449, -13.077025], tiles=activeMapType, zoom_start=2.0)


   def update_map(self, activeCountry, activeCovidStats):

      if self.lastUpdatedTime is not None:
         currentTime = datetime.now()
         updateTimeDiff = (currentTime - self.lastUpdatedTime).total_seconds()
         # if updateTimeDiff < 60:
         #    return

      for ii in range(1, self.nCountries):
         data = self.data.iloc[ii]

         country = data[constants.COVID_COUNTRY_KEY]
         if activeCountry != self.countries[0]:
            if activeCountry != country: continue

         totalCases = data[constants.COVID_TOTAL_CASES_KEY]
         newCases = data[constants.COVID_NEW_CASES_KEY]
         totalDeaths = data[constants.COVID_TOTAL_DEATHS_KEY]
         newDeaths = data[constants.COVID_NEW_DEATHS_KEY]
         totalRecovered = data[constants.COVID_TOTAL_RECOVERED_KEY]
         newRecovered = data[constants.COVID_NEW_RECOVERED_KEY]
         activeCases = data[constants.COVID_ACTIVE_CASES_KEY]
         criticalCases = data[constants.COVID_CRITICAL_CASES_KEY]
         totalCasesPer1M = data[constants.COVID_TOTAL_CASES_PER1M_KEY]
         deathsPer1M = data[constants.COVID_DEATHS_PER1M_KEY]
         population = data[constants.COVID_POPULATION_KEY]

         self.covidData[country] = {constants.COVID_TOTAL_CASES_KEY: totalCases,
                                    constants.COVID_NEW_CASES_KEY: newCases,
                                    constants.COVID_TOTAL_DEATHS_KEY: totalDeaths,
                                    constants.COVID_NEW_DEATHS_KEY: newDeaths,
                                    constants.COVID_TOTAL_RECOVERED_KEY: totalRecovered,
                                    constants.COVID_NEW_RECOVERED_KEY: newRecovered,
                                    constants.COVID_ACTIVE_CASES_KEY: activeCases,
                                    constants.COVID_CRITICAL_CASES_KEY: criticalCases,
                                    constants.COVID_TOTAL_CASES_PER1M_KEY: totalCasesPer1M,
                                    constants.COVID_DEATHS_PER1M_KEY: deathsPer1M,
                                    constants.COVID_POPULATION_KEY: population
                                    }
         
         if country not in self.countryLocations:
            continue
         
         folium.Circle(
            location=self.countryLocations[country],
            popup=country + ': ' + "{:,}".format(data[activeCovidStats]),
            radius=float(data[activeCovidStats] * self.covidScaleVal[activeCovidStats]),
            color=self.covidColor[activeCovidStats],
            fill=True,
            fill_color=self.covidColor[activeCovidStats]
         ).add_to(self.map)
         
      self.map.save('app/templates/map.html')

      self.lastUpdatedTime = datetime.now()


if __name__ == '__main__':
   covidStats = CovidStats()
   covidStats.init_map(activeMapType='OpenStreetMap')
   covidStats.update_map(activeCountry='All', activeCovidStats=constants.COVID_TOTAL_DEATHS_KEY)

