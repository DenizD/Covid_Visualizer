from flask import Flask, render_template, request, session, redirect, url_for
from app.covid_stats import CovidStats
from app.config import constants
import json, os
from datetime import datetime

covidStats = CovidStats()

def load_settings(filename):
    if not os.path.isfile(filename):
        open(filename, 'w+')

    with open(filename, 'r') as f:
        try:
            settings = json.load(f)
        except ValueError:
            settings = {}
    return settings

def save_settings(key, value, filename):
    settings = load_settings(filename)
    settings[key] = value

    with open(filename, 'w+') as f:
        json.dump(settings, f)

app = Flask(__name__)
app.config["SECRET_KEY"] = "covid_key"


@app.route('/map', strict_slashes=False)
def map():
    return render_template('map.html')


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
@app.route('/dashboard', methods=['GET', 'POST'], strict_slashes=False)
def dashboard():

    global covidStats

    if(not bool(session)):
        session[constants.SESSION_MAP_TYPE_KEY] = constants.MAP_TYPES[-1]
        session[constants.SESSION_COUNTRY_KEY] = 'All'
        session[constants.SESSION_ACTIVE_COVID_STATS_KEY] = constants.COVID_TOTAL_DEATHS_KEY

    if request.form.get('activeMapType') is not None:
        session[constants.SESSION_MAP_TYPE_KEY] = request.form.get('activeMapType')

    if request.form.get('activeCountry') is not None:
        session[constants.SESSION_COUNTRY_KEY] = request.form.get('activeCountry')

    if request.form.get('activeCovidStats') is not None:
        session[constants.SESSION_ACTIVE_COVID_STATS_KEY] = request.form.get('activeCovidStats')

    covidStats.init_map(activeMapType=session[constants.SESSION_MAP_TYPE_KEY])
    covidStats.update_map(activeCountry=session[constants.SESSION_COUNTRY_KEY], activeCovidStats=session[constants.SESSION_ACTIVE_COVID_STATS_KEY])

    dailyStats = covidStats.data.iloc[0][[constants.COVID_NEW_CASES_KEY,
                                         constants.COVID_NEW_DEATHS_KEY,
                                         constants.COVID_NEW_RECOVERED_KEY,
                                         constants.COVID_ACTIVE_CASES_KEY,
                                         constants.COVID_CRITICAL_CASES_KEY
                                        ]].to_dict()

    dailyStats = {dailyStat:"{:,}".format(dailyStats[dailyStat]) for dailyStat in dailyStats}

    currentDate = datetime.now().strftime('%d.%m.%Y')

    imageFileCases = os.path.join(session[constants.SESSION_COUNTRY_KEY], currentDate, 'graph-cases-daily.png')
    imageFileDeaths = os.path.join(session[constants.SESSION_COUNTRY_KEY], currentDate, 'graph-deaths-daily.png')
    imageFileRecovers = os.path.join(session[constants.SESSION_COUNTRY_KEY], currentDate, 'cases-cured-daily.png')

    return render_template('dashboard.html',
                           mapTypes=constants.MAP_TYPES,
                           activeMapType=session[constants.SESSION_MAP_TYPE_KEY],
                           countries=covidStats.countries,
                           activeCountry=session[constants.SESSION_COUNTRY_KEY],
                           covidStats = constants.COVID_STATS,
                           activeCovidStats=session[constants.SESSION_ACTIVE_COVID_STATS_KEY],
                           dailyStats=dailyStats,
                           currentDate=currentDate,
                           imageFileCases=imageFileCases,
                           imageFileDeaths=imageFileDeaths,
                           imageFileRecovers=imageFileRecovers
                           )


if __name__ == '__main__':
    app.run(debug=True)