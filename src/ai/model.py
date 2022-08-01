from sklearn.tree import DecisionTreeClassifier


def generate_model(X=[], y=[], hyperparameters={}):
    """
    Trains an AI from the dataset, them returns the model.
    """

    model = DecisionTreeClassifier()
    if hyperparameters:
        model.set_params(**hyperparameters)
    model.fit(X=X, y=y)
    return model
