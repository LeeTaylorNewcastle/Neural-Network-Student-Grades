import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LeakyReLU

np.random.seed(1001)

def load_data():
    return pd.read_csv('student_grades.csv')

def clean_data(df):
    """ This functions shows no values are missing """
    print(df.isnull().sum())

def data_preprocessing(df):
    """ Replace string values with integers then
        Scale all data points except G3 """
    df_prescaled = df.copy()
    df = df.replace(["other", "reputation", "course", "home", "other"], [4, 3, 2, 1, 0])
    df = df.replace(["health", "teacher", "services", "at_home"], [3, 2, 1, 0])
    df = df.replace(["GP", "MS", "M", "F", "U", "R", "LE3", "GT3", "T", "A"],
                    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    df = df.replace(["mother", "father", "other"], [2, 1, 0])
    df = df.replace(["yes", "no"], [1, 0])
    df_scaled = df.drop(['G3'], axis=1)
    df_scaled = scale(df_scaled)
    cols = df.columns.tolist()
    cols.remove('G3')
    df_scaled = pd.DataFrame(df_scaled, columns=cols, index=df.index)
    df_scaled = pd.concat([df_scaled, df['G3']], axis=1)
    df = df_scaled.copy()
    return df, df_prescaled

def split_data(df):
    x = df.loc[:, df.columns != 'G3']
    y = df.loc[:, 'G3']
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.1)
    return x_train, x_test, y_train, y_test

def build_model(input_shape, output_shape=1):
    model = Sequential()
    model.add(Dense(units=256, input_dim=input_shape))
    model.add(LeakyReLU())
    model.add(Dense(units=192))
    model.add(LeakyReLU())
    model.add(Dense(units=128))
    model.add(LeakyReLU())
    model.add(Dense(units=64))
    model.add(LeakyReLU())
    model.add(Dense(units=32))
    model.add(LeakyReLU())
    model.add(Dense(units=1))
    model.add(LeakyReLU())
    model.add(Dense(units=output_shape))
    model.compile(optimizer="adam", loss="mse", metrics=['accuracy'])
    model.summary()
    return model

def test_model(model, *data):
    if len(data) != 4: raise TypeError('Incorrect amount of data passed to test_model(...).')
    x_train, x_test, y_train, y_test = data
    train_pred = model.predict(x_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_pred = model.predict(x_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    print("Train RMSE: {:0.2f}".format(train_rmse))
    print("Test RMSE: {:0.2f}".format(test_rmse))


if __name__ == '__main__':
    gdf = load_data()
    # clean_data(df)
    gdf, _ = data_preprocessing(gdf)
    # print(gdf)
    x_train, x_test, y_train, y_test = split_data(gdf)
    model = build_model(32)
    #
    # model.fit(x_train, y_train, epochs=200, batch_size=1)
    # test_model(model, x_train, x_test, y_train, y_test)
