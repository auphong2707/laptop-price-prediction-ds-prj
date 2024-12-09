from preprocess import preprocess

from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, BaggingRegressor
from xgboost import XGBRFRegressor

import pandas as pd
import numpy as np

import argparse

# Export the model
import joblib
import json
import datetime


def main():
    parser = argparse.ArgumentParser()

    # Add data path
    parser.add_argument('--data', type=str, help='The path to the data')
    parser.add_argument('--cpu_specs', type=str, help='The path to the CPU specs')
    parser.add_argument('--vga_specs', type=str, help='The path to the VGA specs')
    parser.add_argument('--model', type=str, help='The model to train')

    args = parser.parse_args()

    models = {
        'mlp': MLPRegressor(),
        'rf': RandomForestRegressor(random_state=42),
        'graboost': GradientBoostingRegressor(random_state=42),
        'adaboost': AdaBoostRegressor(random_state=42),
        'xgboost': XGBRFRegressor(random_state=42),
        'bagging': BaggingRegressor(random_state=42),
    }

    param_grids = {
        'mlp': {
            'activation': ['relu'],
            'max_iter': [600],
            'beta_1': [0.9, 0.95, 0.99],
            'beta_2': [0.999, 0.9999, 0.99999],
            'epsilon': [1e-08, 1e-09, 1e-10],
        },
        'rf': {
            'n_estimators': [10, 20, 50, 100],
            'max_depth': [10, 20, 30, 40, 50],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None],
            'bootstrap': [True],
        },
        'graboost': {
            'n_estimators': [10, 20, 50, 100],
            'max_depth': [10, 20, 30, 40, 50],
            'learning_rate': [1e-4, 1e-3, 0.01, 0.1],
            'subsample': [0.6, 0.8, 1.0],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None],
        },
        'adaboost': {
            'n_estimators': [10, 20, 50, 100],
            'learning_rate': [1e-4, 1e-3, 0.01, 0.1],
        },
        'xgboost': {
            'n_estimators': [10, 50, 100],
            'max_depth': [10, 20, 30, 40, 50],
            'learning_rate': [1],
            'subsample': [0.6, 0.8, 1.0],
            'colsample_bytree': [0.6, 0.8, 1.0],
            'gamma': [0, 1, 5],
            'reg_alpha': [0, 0.1, 1],
            'reg_lambda': [1, 10, 100],
        },

       'bagging': {
            'n_estimators': [10, 20, 50, 100],
       }
    }

    # Load the data
    data = pd.read_csv(args.data)
    data.drop_duplicates(inplace=True)

    cpu_specs = pd.read_csv(args.cpu_specs)
    vga_specs = pd.read_csv(args.vga_specs)

    data = preprocess(data, cpu_specs, vga_specs)

    data_gaming = data[data['no_gpu'] == 0]
    X_gaming = data_gaming.drop('price', axis=1)
    y_gaming = data_gaming['price']

    print(X_gaming.columns)

    if any(args.model == model for model in models.keys()):
        model = models[args.model]
        param_grid = param_grids[args.model]
        cv = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            n_jobs=-1,
            scoring='neg_mean_squared_error'
        )

        cv.fit(X_gaming, y_gaming)
        
        best_score_gaming = cv.best_score_
        best_model_gaming = cv.best_estimator_
        results_gaming = cv.cv_results_
        current_month = datetime.datetime.now().strftime("%B")
        current_year = datetime.datetime.now().year
        joblib.dump(best_model_gaming, f'model_gaming_{current_month}_{current_year}.joblib')
        print('Score gaming: ', np.sqrt(-best_score_gaming))
        
    elif args.model == 'all':
        best_score_gaming = float('-inf')
        for model_name, model in models.items():
            param_grid = param_grids[model_name]
            cv = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1,
                scoring='neg_mean_squared_error'
            )

            cv.fit(X_gaming, y_gaming)
            
            if cv.best_score_ > best_score:
                best_score = cv.best_score_
                best_model = cv.best_estimator_    
                results_gaming = cv.cv_results_    
            
                current_month = datetime.datetime.now().strftime("%B")
                current_year = datetime.datetime.now().year
                joblib.dump(best_model, f'model_gaming_{current_month}_{current_year}.joblib')
            
            print('Score gaming: ', np.sqrt(-best_score_gaming))
        
    # For non-gaming laptops
    data_non_gaming = data[data['no_gpu'] == 1]
    X_non_gaming = data_non_gaming.drop('price', axis=1)
    y_non_gaming = data_non_gaming['price']
    if any(args.model == model for model in models.keys()):
        model = models[args.model]
        param_grid = param_grids[args.model]
        cv = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            n_jobs=-1,
            scoring='neg_mean_squared_error'
        )

        cv.fit(X_non_gaming, y_non_gaming)
        
        best_score_non_gaming = cv.best_score_
        best_model_non_gaming = cv.best_estimator_
        results_non_gaming = cv.cv_results_
        current_month = datetime.datetime.now().strftime("%B")
        current_year = datetime.datetime.now().year
        joblib.dump(best_model_non_gaming, f'model_non_gaming_{current_month}_{current_year}.joblib')
        print('Score non_gaming: ', np.sqrt(-best_score_non_gaming))
        
    elif args.model == 'all':
        best_score_non_gaming = float('-inf')
        for model_name, model in models.items():
            param_grid = param_grids[model_name]
            cv = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1,
                scoring='neg_mean_squared_error'
            )

            cv.fit(X_non_gaming, y_non_gaming)
            
            if cv.best_score_ > best_score:
                best_score = cv.best_score_
                best_model = cv.best_estimator_    
                results_non_gaming = cv.cv_results_    
            
                current_month = datetime.datetime.now().strftime("%B")
                current_year = datetime.datetime.now().year
                joblib.dump(best_model, f'model_non_gaming_{current_month}_{current_year}.joblib')
            
            print('Score non_gaming: ', np.sqrt(-best_score_non_gaming))

    else:
        print("Invalid model name")
        return

    # Save cross-validation results to JSON
    with open('cv_results_gaming.json', 'w') as f:
        json.dump(results_gaming, f, indent=4, default=str)
    
    with open('cv_results_non_gaming.json', 'w') as f:
        json.dump(results_non_gaming, f, indent=4, default=str)

if __name__ == "__main__":
    main()