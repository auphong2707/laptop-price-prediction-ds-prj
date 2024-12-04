from normalize import normalize

from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import MinMaxScaler

import pandas as pd

import argparse


# Export the model
import joblib
import json
import datetime


def main():
    parser = argparse.ArgumentParser()

    # Add data path
    parser.add_argument('--data', type=str, help='The path to the data')
    parser.add_argument('--model', type=str, help='The model to train')

    args = parser.parse_args()

    # Load the data
    data = pd.read_csv(args.data)
    data.drop_duplicates(inplace=True)

    X = data.drop('laptop_specs_price', axis=1)
    y = data['laptop_specs_price']

    X = normalize(X)

    models = {
        'mlp': MLPRegressor(),
        'rf': RandomForestRegressor(random_state=42),
        'ridge': Ridge(random_state=42),
    }

    param_grids = {
        'mlp': {
            'hidden_layer_sizes': [(100, 100)],
            'activation': ['identity', 'logistic', 'tanh', 'relu'],
            'max_iter': [100, 200, 300, 400, 500],
            'beta_1': [0.9, 0.95, 0.99],
            'beta_2': [0.999, 0.9999, 0.99999],
            'epsilon': [1e-08, 1e-09, 1e-10],
        },
        'rf': {
            'criterion': ['squared_error', 'absolute_error'],
            'n_estimators': [10, 50, 100, 200, 300],
            'max_depth': [10, 20, 30, 40, 50],
        },
        'ridge': {},
    }

    if any(args.model == model for model in models.keys()):
        model = models[args.model]
        param_grid = param_grids[args.model]
        cv = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            n_jobs=-1
        )

        cv.fit(X, y)

        best_model = cv.best_estimator_
        results = cv.cv_results_
    
    elif args.model == 'all':
        best_score = float('-inf')
        for model_name, model in models.items():
            param_grid = param_grids[model_name]
            cv = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1
            )

            cv.fit(X, y)
            
            if cv.best_score_ > best_score:
                best_score = cv.best_score_
                best_model = cv.best_estimator_    
                results = cv.cv_results_    
    else:
        print("Invalid model name")
        return

    # Save cross-validation results to JSON
    with open('cv_results.json', 'w') as f:
        json.dump(results, f, indent=4, default=str)

    current_month = datetime.datetime.now().strftime("%B")
    current_year = datetime.datetime.now().year
    joblib.dump(best_model, f'model_{current_month}_{current_year}.joblib')

    print(best_score)


if __name__ == "__main__":
    main()