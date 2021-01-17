# config file to easily to adjust hyper parameters


# Training parameters
training_parameter = {"epochs": 500,
                      "learning_rate": 0.0001,
                      "alpha": 0.25,
                      "gamma": 2.0,
                      # "features": ["Sex", "SibSp", "Age", "Pclass", "Parch", "Fare"],
                      "features": ["Sex", "SibSp", "Age", "Pclass", "Parch"],
                      "batch_size": 16,
                      "patience": 10}

network_parameter = {"hidden_layer": 1,
                     "hidden_neurons": 64,
                     "l1": 0.001,
                     "l2": 0.001,
                     "threshold": 0.5}


cfg = {'training': training_parameter, 'network': network_parameter}
