import os
import argparse
import joblib
import json
import datetime
import numpy as np

from preprocess import preprocess
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, BaggingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRFRegressor

import sys
sys.path.append('.')
from helper import get_latest_table


def main():
    parser = argparse.ArgumentParser()

    # Add data path
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
            'hidden_layer_sizes': [(100,), (50, 50), (100, 50, 25)],  # Varying layer sizes and depths
            'activation': ['relu'],                         # Common activation functions
            'alpha': [1e-5, 1e-4, 1e-3, 1e-2],                      # Regularization parameter
            'learning_rate': ['constant', 'adaptive'],              # Learning rate schedule
            'max_iter': [200, 500, 1000],                           # Max iterations for convergence
            'early_stopping': [True],                               # Enable early stopping
            'learning_rate_init': [0.001, 0.01, 0.1],               # Initial learning rate
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
    data = get_latest_table('laptop_specs')
    data.drop_duplicates(inplace=True)

    cpu_specs = get_latest_table('cpu_specs')
    vga_specs = get_latest_table('gpu_specs')

    # Preprocess the data
    data = preprocess(data, cpu_specs, vga_specs)
    data_has_gpu = data[data['no_gpu'] == 0]
    X_has_gpu = data_has_gpu.drop('price', axis=1)
    y_has_gpu = data_has_gpu['price']

    # Split the data
    X_has_gpu_train, X_has_gpu_test, y_has_gpu_train, y_has_gpu_test = train_test_split(X_has_gpu, y_has_gpu, test_size=0.2, random_state=42)

    # Train the model
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    save_path = f'data_analysis/results/trained_models/{current_month}_{current_year}'
    os.makedirs(save_path, exist_ok=True)

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
    
        cv.fit(X_has_gpu_train, y_has_gpu_train)
        
        best_score_has_gpu = cv.best_score_
        best_model_has_gpu = cv.best_estimator_
        results_has_gpu = cv.cv_results_
        joblib.dump(best_model_has_gpu, f'{save_path}/model_has_gpu.joblib')
        # print('Score gaming: ', np.sqrt(-best_score_has_gpu))
        
    elif args.model == 'all':
        best_score_has_gpu = float('-inf')
        for model_name, model in models.items():
            param_grid = param_grids[model_name]
            cv = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1,
                scoring='neg_mean_squared_error'
            )

            cv.fit(X_has_gpu_train, y_has_gpu_train)
            
            if cv.best_score_ > best_score_has_gpu:
                best_score_has_gpu = cv.best_score_
                best_model = cv.best_estimator_    
                results_has_gpu = cv.cv_results_    
            
                joblib.dump(best_model, f'{save_path}/model_has_gpu.joblib')
            
            # print('Score gaming: ', np.sqrt(-best_score_has_gpu))
    else: 
        print('Invalid model name')
        return
    
    y_pred_has_gpu = cv.best_estimator_.predict(X_has_gpu_test)
    print('Error ratio of gaming :', np.sqrt(mean_squared_error(y_has_gpu_test, y_pred_has_gpu))/y_has_gpu_test.mean())
    print('Error of gaming: ', np.sqrt(mean_squared_error(y_has_gpu_test, y_pred_has_gpu)))
        
    # For non-gaming laptops
    data_no_gpu = data[data['no_gpu'] == 1]
    X_no_gpu = data_no_gpu.drop('price', axis=1)
    y_no_gpu = data_no_gpu['price']

    X_no_gpu_train, X_no_gpu_test, y_no_gpu_train,  y_no_gpu_test = train_test_split(X_no_gpu, y_no_gpu, test_size=0.2, random_state=42)

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

        cv.fit(X_no_gpu_train, y_no_gpu_train)
        
        best_score_no_gpu = cv.best_score_
        best_model_no_gpu = cv.best_estimator_
        results_no_gpu = cv.cv_results_
        
        joblib.dump(best_model_no_gpu, f'{save_path}/model_no_gpu.joblib')
        # print('Score no_gpu: ', np.sqrt(-best_score_no_gpu))
        
    elif args.model == 'all':
        best_score_no_gpu = float('-inf')
        for model_name, model in models.items():
            param_grid = param_grids[model_name]
            cv = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1,
                scoring='neg_mean_squared_error'
            )

            cv.fit(X_no_gpu_train, y_no_gpu_train)
            
            if cv.best_score_ > best_score_no_gpu:
                best_score_no_gpu = cv.best_score_
                best_model = cv.best_estimator_    
                results_no_gpu = cv.cv_results_    
            
                joblib.dump(best_model, f'{save_path}/model_no_gpu.joblib')
            
            # print('Score no_gpu: ', np.sqrt(-best_score_no_gpu))
    
    y_pred_no_gpu = cv.best_estimator_.predict(X_no_gpu_test)
    print('Error ratio of no_gpu :', np.sqrt(mean_squared_error(y_no_gpu_test, y_pred_no_gpu))/y_no_gpu_test.mean())
    print('Error of no_gpu: ', np.sqrt(mean_squared_error(y_no_gpu_test, y_pred_no_gpu)))

    # Save cross-validation results to JSON
    with open(f'{save_path}/cv_results_has_gpu.json', 'w') as f:
        json.dump(results_has_gpu, f, indent=4, default=str)
    
    with open(f'{save_path}/cv_results_no_gpu.json', 'w') as f:
        json.dump(results_no_gpu, f, indent=4, default=str)

if __name__ == "__main__":
    main()