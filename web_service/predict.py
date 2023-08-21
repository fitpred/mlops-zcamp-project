import pickle
import pandas as pd
from flask import Flask, request, jsonify


cat_cols = ['brand', 'title_status', 'state']
num_cols = ['year', 'mileage']

feature_cols = cat_cols + num_cols


# load model
with open('model.pkl', 'rb') as f_in:
    model = pickle.load(f_in)


def read_data(features):
    """Read data into DataFrame"""
    df_predict = pd.DataFrame(features, index=[0])

    for i in cat_cols:
        df_predict[i] = pd.Series(df_predict[i], dtype="category")

    return df_predict


def predict(df_predict):

    if all([i in df_predict.columns for i in feature_cols]):
        preds = model.predict(df_predict)
    else:
        print('Please check featurees')

    return float(preds[0])


app = Flask('car-price-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    features = request.get_json()

    df_predict = read_data(features)
    pred = predict(df_predict)

    result = {
        'price': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)