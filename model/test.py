from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor

import argparse


# Ẽxport the model
import joblib


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', type=str, help='The model to train')

    args = parser.parse_args()

    model_choices = {
        'mlp': MLPRegressor(
            hidden_layer_sizes=(100, 1),
            random_state=42, 
            max_iter=200,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-08,
            random_state = 42
        ),
        'dt': DecisionTreeRegressor(
            max_depth = 100, 
            random_state=42
        ),
        'rf': RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs = -1,
        ),
        'svr': SVR(
            kernel='rbf',
            C=100,
            gamma=0.1,
        ),
        'lr': LinearRegression(),
        'lasso': Lasso(),
        'ridge': Ridge(),
        'knn': KNeighborsRegressor(
            n_neighbors=5,
            weights='uniform',
            algorithm='auto',
            leaf_size=30,
            p=2,
            metric='minkowski',
            metric_params=None,
            n_jobs=-1
        ),
    }

    X = None 
    y = None

    cv = GridSearchCV(
        estimator=model_choices[args.model],
        param_grid={
            'alpha': [0.0001, 0.001, 0.01, 0.1, 1],
            'max_iter': [100, 200, 300, 400, 500],
        },
        cv=5,
        n_jobs=-1
    )

    cv.fit(X, y)

    joblib.dump(cv.best_estimator_, 'model.joblib')


if __name__ == "__main__":
    main()