from flask import Flask
from flask import request
from flask import render_template
import json
app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    #load a current view of the data
    total=0
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()
    years=sorted(list(data["Canada"].keys()))

    label_years = []
    for year in years:
        if int(year) %5 == 0:
            label_years.append(year)


    Can_line_endpoints = []
    Us_line_endpoints = []
    Mex_line_endpoints = []
    for country in data:
        for i in range(len(data[country])-1): # make it easy to dynamically generate a line graph
            start_x = years[i] #generate endpoints for each line segment
            stop_x = years[i+1]
            total += data[country][years[i]]
            if country == "Canada":
                Can_line_endpoints.append([data[country][start_x],data[country][stop_x]])
            elif country == "United States":
                Us_line_endpoints.append([data[country][start_x],data[country][stop_x]])
            else:
                Mex_line_endpoints.append([data[country][start_x],data[country][stop_x]])

    print(Can_line_endpoints, Us_line_endpoints, Mex_line_endpoints)
    #render the template with the apporpriate data
    return render_template('index.html', mean = total/183, label_years = label_years, data = data, years=years, Can_line_endpoints = Can_line_endpoints, Us_line_endpoints = Us_line_endpoints, Mex_line_endpoints = Mex_line_endpoints)


@app.route('/year')
def year():
    #load a current view of the data
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()

    #check to see if year is in the query string portion of the URL
    requested_year = request.args.get('year')
    if requested_year == None:
        requested_year = "2020" #just in case

    #Filter and reformat data for ease of access in the template
    countries = list(data.keys())
    requested_data = {}
    for country in countries:
        requested_data[country] = data[country][requested_year]
    all_years = sorted(list(data[countries[0]].keys()))

    return render_template('year.html', year=requested_year, all_years=all_years, data=data)
app.run(debug=True)
