import os
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import re
import scipy

from lightgbm import LGBMClassifier
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold

import nltk
nltk.download('punkt')
nltk.download('wordnet')


def clean_text(text, lemma=WordNetLemmatizer()):
    """Process text

    1. Split different sentences
    2. Make words lowercase
    3. Remove URLs (i.e. http) and usernames (i.e. @username)
    4. Remove digits and punctuations
    5. Remove any mention of MBTI types
    6. Tokenize words (i.e. split the words into list)
    7. Lemmatize words (i.e. reduce words to singular form)
    8. Join text into string

    Args:
        text (str): input text
        lemma: Lemmatizer (defaults to nltk WordNetLemmatizer)

    Returns:
        (str): processed text
    """
    # Split sentences
    text = re.sub('\|\|\|', ' ', text)

    # Make words lowercase
    text = text.lower()

    # Remove URL and usernames
    text = re.sub(r'http[^\s]*', '', text)
    text = re.sub('@[a-z0-9]+', '', text)

    # Remove digits and punctuations
    text = re.sub('[^a-z ]', '', text)

    # Remove any mention of MBTI types
    text = re.sub('[^\s]*[ie][ns][tf][jp][^\s]*', '', text)
    text = re.sub('[^\s]*mbti[^\s]*', '', text)

    # Tokenize words
    text_list = word_tokenize(text)

    # Lemmatize words
    text_list = [lemma.lemmatize(word) for word in text_list]

    # Join text into string
    text = ' '.join(text_list)
    return text


def load_and_save_data(mbti_cols):
    """Reads in data, performs preprocessing and saves data
    If saved data is present, directly read in the saved data

    If saved data does not exist
        a) Reads in data
        b) Insert new columns as indicator for each mbti category
        c) Process text column
        d) Save data
    If saved data exist
        a) Reads in saved data

    Args:
        mbti_cols (list): name of new columns generated

    Returns:
        (pandas DataFrame): processed data
    """
    if not os.path.isfile('sample_data/mbti_clean.csv'):
        df = pd.read_csv('sample_data/mbti.csv')

        # Insert new columns as indicator for each mbti category
        for idx, col in enumerate(mbti_cols):
            df[col] = df['type'].str[idx] == col[0]

        # Process text column
        df['posts_clean'] = df['posts'].apply(clean_text)

        # Save data
        df.to_csv('sample_data/mbti_clean.csv', index=False)
    else:
        df = pd.read_csv('sample_data/mbti_clean.csv')

    return df


def get_train_test(X, y, test_size=0.2, random_state=0):
    """Splits data into training and testing data

    Args:
        X (pandas DataFrame): processed input data
        y (pandas DataFrame): processed output data
        test_size (float): proportion of test data, defaults to 0.2
        random_state (int): fixed seed, allows reproducible result, defaults to 0

    Returns:
        4-element tuple

        - X_train (pandas DataFrame): training input
        - X_test (pandas DataFrame): testing input
        - y_train (pandas DataFrame): training output
        - y_test (pandas DataFrame): testing output
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    return X_train, X_test, y_train, y_test


def save_vectorizer(corpus, params=None):
    """Vectorize corpus and saves vectorizer

    Args:
        corpus (pandas Series): input text corpus (training input)
        params (dict): specifies parameters for vectorizer, defaults to None

    Returns:
        (sklearn CountVectorizer)
    """
    if params is None:
        params = dict(ngram_range=(1, 3), max_df=0.9, min_df=0.1, max_features=None, stop_words='english')
    model = CountVectorizer(**params)
    vect = model.fit(corpus)
    print(f'Vocabulary size: {len(vect.get_feature_names())}')
    # pickle.dump(vect, open('data/vect.pkl', 'wb'))
    pickle.dump(vect.get_feature_names(), open('data/vocabulary.pkl', 'wb'))
    return vect


def load_vectorizer():
    """Load and return saved vectorizer

    Returns:
        (sklearn CountVectorizer)
    """
    # vect = pd.read_pickle('data/vect.pkl')
    vocabulary = pd.read_pickle('data/vocabulary.pkl')
    vect = CountVectorizer(vocabulary=vocabulary)
    return vect


def get_model(X_train, y_train, params=None):
    """Get model after fitting

    Args:
        X_train (pandas DataFrame): training input
        y_train (pandas Series): training output
        params (dict): specifies parameters for model, defaults to None

    Returns:
        (model)
    """
    if params is None:
        params = dict(n_estimators=50, max_depth=3, nthread=8, learning_rate=0.2)
    params['scale_pos_weight'] = len(y_train) / sum(y_train)
    model = LGBMClassifier(**params)
    model.fit(X_train, y_train)
    return model


def get_gridsearch_model(X_train, y_train, model_name):
    """Get, save and return best model after grid search and with stratified cross validation

    Args:
        X_train (pandas DataFrame): training input
        y_train (pandas Series): training output
        model_name (str): name of model to save

    Returns:
        (model)
    """
    scale_pos_weight = len(y_train) / sum(y_train)
    clf = LGBMClassifier()
    values = {'n_estimators': [20, 50, 100, 200],
              'max_depth': [3, 5],
              'num_leaves': [50, 100],
              'n_jobs': [8],
              'learning_rate': [0.1, 0.2, 0.3],
              'scale_pos_weight': [scale_pos_weight]
              }
    grid = GridSearchCV(clf,
                        param_grid=values,
                        cv=StratifiedKFold(3),
                        scoring='f1')
    grid.fit(X_train, y_train)
    print('Best parameters: ', grid.best_params_)
    pickle.dump(grid.best_estimator_, open(f'data/model_{model_name}.pkl', 'wb'))
    return grid.best_estimator_


def train_pipeline():
    """Training pipeline for loading, preprocessing and model training
    """
    indicator_cols = ['EI', 'SN', 'TF', 'JP']
    df = load_and_save_data(indicator_cols)
    X_train, X_test, y_train, y_test = get_train_test(X=df[['posts_clean']],
                                                      y=df[indicator_cols])
    # vect = save_vectorizer(X_train['posts_clean'])
    vect = load_vectorizer()
    vector_train = vect.transform(X_train['posts_clean']).astype(np.float64)
    vector_test = vect.transform(X_test['posts_clean']).astype(np.float64)
    for idx, col in enumerate(indicator_cols):
        print(f'Predicting for: {col}')
        model = get_gridsearch_model(vector_train, y_train[col], col)
        y_pred = model.predict(vector_test)
        print(confusion_matrix(y_test[col], y_pred))
        print(f'Accuracy for {col}: ', accuracy_score(y_test[col], y_pred))
        print(f'Recall for {col}: ', recall_score(y_test[col], y_pred))
        print(f'F1 for {col}: ', f1_score(y_test[col], y_pred))
        print()


def test_pipeline(input_text):
    """Testing pipeline for new input text

    Args:
        input_text (str): input text

    Returns:
        2-element tuple

        - n_words (int): number of words in text that are in vocabulary
        - results (list): list of model prediction probabilities
    """
    indicator_cols = ['EI', 'SN', 'TF', 'JP']
    clean_input = clean_text(input_text)
    vect = load_vectorizer()
    vector_input = vect.transform(pd.Series(clean_input)).astype(np.float64)
    n_words = scipy.sparse.csr_matrix.count_nonzero(vector_input)
    predictions = []
    for col in indicator_cols:
        m = pd.read_pickle(f'data/model_{col}.pkl')
        y_pred = m.predict_proba(vector_input)
        predictions.append(y_pred[0])

    # Decode results
    personality = ''
    for idx, r in enumerate(predictions):
        if r[0] >= 0.5:
            personality += indicator_cols[idx][1]
        else:
            personality += indicator_cols[idx][0]
    return n_words, personality, predictions


def get_bar_plot(results):
    """Get figure for plot

    Adds plotly.graph_objects charts for bar plot

    Args:
        results (list): List of probabilities for each personality trait

    Returns:
        (dict)
    """
    y_data = ['Introversion-Extroversion', 'Intuition-Sensing', 'Feeling-Thinking', 'Perceiving-Judging']
    x_data_0 = [r[0] for r in results]
    x_data_1 = [r[1] for r in results]
    data = [go.Bar(
        y=y_data,
        x=x_data_0,
        hovertext=['Introversion', 'Intuition', 'Feeling', 'Perceiving'],
        hoverinfo='text',
        orientation='h',
        marker_color='#BE9B89',
    ), go.Bar(
        y=y_data,
        x=x_data_1,
        hovertext=['Extroversion', 'Sensing', 'Thinking', 'Judging'],
        hoverinfo='text',
        orientation='h',
        marker_color='#D6CAC7',
    )]

    annotations = []
    for yd, xd in zip(y_data, x_data_0):
        annotations.append(
            dict(
                xref='paper',
                yref='y',
                x=xd / 2,
                y=yd,
                xanchor='center',
                text=str(int(np.round(xd * 100, 0))) + '%',
                font=dict(size=14),
                showarrow=False
            )
        )

    for yd, xd in zip(y_data, x_data_1):
        annotations.append(
            dict(
                xref='paper',
                yref='y',
                x=1 - (xd / 2),
                y=yd,
                xanchor='center',
                text=str(int(np.round(xd * 100))) + '%',
                font=dict(size=14),
                showarrow=False)
        )

    layout = dict(
        annotations=annotations,
        bargap=0.3,
        barmode='stack',
        margin=dict(l=170, r=50, t=30, b=30),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(
            range=[0, 1],
            showticklabels=False
        ),
        yaxis=dict(
            categoryarray=y_data[::-1]
        ),
        font=dict(
            family='Source Sans Pro',
            size='15'
        )
    )
    return dict(data=data, layout=layout)
