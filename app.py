from flask import Flask, request, jsonify, render_template
import json
import pickle
import numpy as np
# Solution for taking out the warning:
#... \lib\site-packages\sklearn\base.py:450: UserWarning: X does not have valid feature names, but LinearRegression was fitted with feature names
#  warnings.warn(
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)

print('\nStarting Python Flask Server For Home Price Prediction...')

with open('columns.json','r') as f:
        data_columns = json.load(f)['data_columns']
        locations = data_columns[3:]

print('Loading model...')

with open('dublin_property_price_prediction.pickle', 'rb') as f:
    model = pickle.load(f)
print('Model was loaded successfully!\n')

def get_estimated_price(location, beds, baths, floor_area):
    try:
        loc_index = data_columns.index([location.lower()])
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = beds
    x[1] = baths
    x[2] = floor_area
    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', locations=locations)

@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        try:
            location = request.form['location']
        except:
            return render_template('index.html', 
            locations=locations,
            fill_message='Please, all the fields are required!')
        try:
            beds = int(request.form['beds'])
        except:
            return render_template('index.html', 
            locations=locations,
            fill_message='Please, all the fields are required!')
        try:
            baths = int(request.form['baths'])
        except:
            return render_template('index.html', 
            locations=locations,
            fill_message='Please, all the fields are required!')
        try:
            floor_area = float(request.form['floor_area'])
        except:
            return render_template('index.html', 
            locations=locations,
            fill_message='Please, "area" should be filled with positive integers numbers, only!')

        prediction = "{:,}".format(int(get_estimated_price(location, beds, baths, floor_area)))

        return render_template('prediction.html', locations=locations, 
        prediction=prediction, location=location, beds=beds,
        baths=baths, floor_area=floor_area)

################################################### Sheet   |   Prediction
#print(get_estimated_price('Dublin 7', 3, 2, 110)) # 595000  |   571131
#print(get_estimated_price('Dublin 6', 3, 3, 132)) # 725000  |   734960
#print(get_estimated_price('Dublin 3', 4, 3, 120)) # 795000  |   508424
#print(get_estimated_price('Dublin 20', 3, 1, 105)) # 575000 |   573069

if __name__ == '__main__':
    app.run(host="0.0.0.0")