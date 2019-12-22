import pandas as pd
import numpy as np

def load_dataset(train_file_path, test_file_path):

    # Loads all important files as dataframes
    train_df = pd.read_csv(train_file_path);
    test_df = pd.read_csv(test_file_path);

    # Adds a new 'Label' column with default 'Train/Test' values for both dataframes
    train_df['Label'] = 'Train'
    test_df['Label'] = 'Test'

    # Joins both dataframes
    new_df = pd.concat([train_df, test_df], ignore_index=True, sort=False)

    # Deletes 'Ticket', 'Embarked' and 'Cabin' columns
    new_df = new_df.drop(['Ticket', 'Embarked', 'Cabin'], axis=1)

    return new_df

def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:

    # Creates a new dictionary with all information about missing values
    data = {
        'Total': df.isnull().sum(),
        'Percent': df.isnull().sum() / df.shape[0] * 100
    }

    # Creates a new dataframe with the help of the dictionary
    new_df = pd.DataFrame(data, index=df.columns)

    # Sorts the dataframe in descending order
    new_df = new_df.sort_values(by='Total', ascending=False)

    return new_df

def substitute_missing_values(df: pd.DataFrame) -> pd.DataFrame:

    # Copies the specified dataframe
    new_df = df.copy()

    # Replaces all missing values in the 'Age' column by the mean
    new_df.loc[new_df['Age'].isnull(), 'Age'] = df['Age'].mean()

    # Replaces all missing values in the 'Fare' column by the median
    new_df['Fare'] = new_df['Fare'].fillna(df['Fare'].median())

    return new_df

def get_correlation(df: pd.DataFrame) -> float:

    return df['Age'].corr(df['Fare'])

def get_survived_per_class(df: pd.DataFrame, group_by_column_name: str) -> pd.DataFrame:

    # Creates a new dictionary with all averages according to the groups
    df_tmp = df.groupby(group_by_column_name)['Survived']
    data = {'Survived': df_tmp.sum() / df_tmp.count()}

    # Creates a new dataframe with the help of the dictionary
    new_df = pd.DataFrame(data)

    # Sorts the dataframe and resets indexes
    new_df = new_df.sort_values(by='Survived', ascending=False).reset_index()

    # Rounds all averages to two decimal places
    new_df['Survived'] = new_df['Survived'].round(2)

    return new_df

def get_outliers(df: pd.DataFrame) -> (int, str):

    # Calculates both quantiles including IQR
    Q1 = df['Fare'].quantile(0.25)
    Q3 = df['Fare'].quantile(0.75)
    IQR = Q3 - Q1

    # Filters out all outliers
    new_df = df.query('(@Q1 - 1.5*@IQR) < Fare < (@Q3 + 1.5*@IQR)')

    # Draws a box plot
    df.join(new_df, lsuffix='_before', rsuffix='_after').boxplot(
        column=['Fare_before', 'Fare_after']
    )

    # Gets the number of outliers
    num_of_outliers = df[
        (df['Fare'] < (Q1 - 1.5*IQR)) | (df['Fare'] > (Q3 + 1.5*IQR))
    ].shape[0]

    # Gets the name of the biggest outlier
    name = df.loc[df['Fare'] == df['Fare'].max(), 'Name'].values[0]

    return (num_of_outliers, name)

def normalise(df: pd.DataFrame, col: str) -> pd.DataFrame:

    # Copies the specified dataframe-
    new_df = df.copy()

    # Scales the 'col' column according to the 'Pclass' values
    new_df[col] = new_df.groupby('Pclass')[col].apply(
        lambda x: (x-min(x)) / (max(x)-min(x))
    )

    return new_df

def create_new_features(df: pd.DataFrame) -> pd.DataFrame:

    # Copies the specified dataframe
    new_df = df.copy()

    # Standardizes the 'Fare' column
    new_df['Fare_scaled'] = new_df['Fare'].apply(
        lambda x: (x-new_df['Fare'].mean()) / new_df['Fare'].std()
    )

    # Makes logarithms of values in the 'Age' column
    new_df['Age_log'] = new_df['Age'].apply(
        lambda x: np.log(x)
    )

    # Makes integers of values in the 'Sex' column
    new_df['Sex'] = new_df['Sex'].replace({'female': '1', 'male': '0'}).astype(int)

    return new_df

def calculate_probability(df, row):

    # Counts probabilities of survival for every age and both sexes
    df_tmp = df.loc[
        (df['Age'] > row['AgeInterval'].left) &
        (df['Age'] <= row['AgeInterval'].right) &
        (df['Sex'] == row['Sex'])
    ]

    # The denominator is zero
    if (not df_tmp['Survived'].count()):
        return 0

    return df_tmp['Survived'].sum() / df_tmp['Survived'].count()

def determine_survival(df: pd.DataFrame, n_interval: int, age: float, sex: str) -> float:

    # Replaces all missing values in the 'Age' column by the mean
    df['Age'] = df['Age'].fillna(df['Age'].mean())

    # Creates a new dictionary with all information about ages divided into intervals
    intervals = {'AgeInterval': pd.cut(df['Age'], n_interval)}

    # Creates a new dataframe with the help of the dictionary and drops duplicates
    df_both = pd.DataFrame(intervals).drop_duplicates()

    # Creates dataframes for both sexes and sorts them
    df_male = df_both.copy().sort_values(by='AgeInterval')
    df_female = df_both.copy().sort_values(by='AgeInterval')

    # Adds a new 'Sex' column for both sexes
    df_male['Sex'] = 'male'
    df_female['Sex'] = 'female'

    # Counts probabilities of survival for every age and both sexes
    df_male['Survival Probability'] = df_male.apply(
        lambda row: calculate_probability(df, row), axis=1
    )
    df_female['Survival Probability'] = df_female.apply(
        lambda row: calculate_probability(df, row), axis=1
    )

    # Joins both dataframes and merges them
    df_both = pd.concat([df_male, df_female]).sort_index(kind='merge')

    # Resets indexes
    df_both = df_both.reset_index(drop=True)

    # Gets the probability of survival for the specified age and sex
    probability = df_both.loc[
        (age > df_both.apply(lambda row: row['AgeInterval'].left, axis=1)) &
        (age <= df_both.apply(lambda row: row['AgeInterval'].right, axis=1)) &
        (sex == df_both['Sex']),
        'Survival Probability'
    ]

    if probability.empty:
        return 0
    else:
        return probability.values[0]
