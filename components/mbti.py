import os
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import re
import scipy

from lightgbm import LGBMClassifier
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold

# import nltk
# nltk.download('punkt')
# nltk.download('wordnet')

# Variables
mbti_cols = ['EI', 'SN', 'TF', 'JP']
path_data = 'sample_data/mbti.csv'
path_save_data = 'sample_data/mbti_clean.csv'
path_vect = 'data/vocabulary.pkl'
path_model = []
for col in mbti_cols:
    path_model.append(f'data/model_{col}.pkl')
non_sw = [
    'ain',
    'aint',
    'aren',
    'arent',
    'cant',
    'couldn',
    'coulnt',
    'dont',
    'didn',
    'didnt',
    'doesn',
    'doesnt',
    'hadn',
    'hadnt',
    'hasn',
    'hasnt',
    'haven',
    'havent',
    'isn',
    'isnt',
    'mightn',
    'mightnt',
    'mustn',
    'mustnt',
    'needn',
    'neednt',
    'not',
    'shan',
    'shant',
    'shouldn',
    'shouldnt',
    'wasn',
    'wasnt',
    'weren',
    'werent',
    'won',
    'wont',
    'wouldn',
    'wouldnt'
]


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


def load_and_save_data(mbti_cols, path_data, path_save_data):
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
        path_data (str): location and name of input data
        path_save_data (str): location and name of saved data

    Returns:
        (pandas DataFrame): processed data
    """
    if not os.path.isfile(path_save_data):
        print('Read and save data file')
        df = pd.read_csv(path_data)

        # Insert new columns as indicator for each mbti category
        for idx, col in enumerate(mbti_cols):
            df[col] = df['type'].str[idx] == col[0]

        # Process text column
        df['posts_clean'] = df['posts'].apply(clean_text)

        # Save data
        df.to_csv(path_save_data, index=False)
    else:
        print('Load saved data file')
        df = pd.read_csv(path_save_data)

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


def save_vectorizer(corpus, path_vect, params=None):
    """Vectorize corpus and saves vectorizer

    Args:
        corpus (pandas Series): input text corpus (training input)
        path_vect (str): location and file name of saved vectorizer
        params (dict): specifies parameters for vectorizer, defaults to None

    Returns:
        (sklearn CountVectorizer)
    """
    print('Initialize and save vectorizer')
    sw = [clean_text(word) for word in stopwords.words('english')]
    sw = list(set(sw) - set(non_sw))
    if params is None:
        params = dict(ngram_range=(1, 3), max_df=0.95, min_df=0.05, max_features=None, stop_words=sw)
    model = CountVectorizer(**params)
    vect = model.fit(corpus)
    # pickle.dump(vect, open(path_vect, 'wb'))
    pickle.dump(vect.get_feature_names(), open(path_vect, 'wb'))
    return vect


def load_vectorizer(path_vect):
    """Load and return saved vectorizer

    Args:
        path_vect (str): location and file name of saved vectorizer

    Returns:
        (sklearn CountVectorizer)
    """
    # vect = pd.read_pickle(path_vect)
    vocabulary = pd.read_pickle(path_vect)
    vect = CountVectorizer(vocabulary=vocabulary)
    return vect


def get_gridsearch_model(X_train, y_train, path_model):
    """Train, save and return best model after grid search and with stratified cross validation

    Args:
        X_train (pandas DataFrame): training input
        y_train (pandas Series): training output
        path_model (str): location and file name of saved model

    Returns:
        (model)
    """
    scale_pos_weight1 = len(y_train) / sum(y_train)
    scale_pos_weight2 = (len(y_train) - sum(y_train)) / sum(y_train)
    clf = LGBMClassifier()
    values = {'n_estimators': [20, 50, 100, 200],
              'max_depth': [3, 5],
              'num_leaves': [50, 100],
              'n_jobs': [8],
              'learning_rate': [0.1, 0.2, 0.3],
              'scale_pos_weight': [scale_pos_weight1, scale_pos_weight2]
              }
    grid = GridSearchCV(clf,
                        param_grid=values,
                        cv=StratifiedKFold(3),
                        scoring='balanced_accuracy')
    grid.fit(X_train, y_train)
    print('Best parameters: ', grid.best_params_)

    # Retrain model on entire data
    params = grid.best_estimator_.get_params()
    model = LGBMClassifier(**params)
    model.fit(X_train, y_train)
    pickle.dump(model, open(path_model, 'wb'))
    return model


def get_model(path_model):
    """Get saved best model after grid search and with stratified cross validation

    Args:
        path_model (str): location and file name of saved model

    Returns:
        (model)
    """
    EI_model = {
        'learning_rate': 0.1,
        'max_depth': 3,
        'n_estimators': 200,
        'n_jobs': 8,
        'num_leaves': 50,
        'scale_pos_weight': 4.34021263289556
    }
    SN_model = {
        'learning_rate': 0.1,
        'max_depth': 3,
        'n_estimators': 50,
        'n_jobs': 8,
        'num_leaves': 50,
        'scale_pos_weight': 6.244258872651357
    }
    TF_model = {
        'learning_rate': 0.1,
        'max_depth': 5,
        'n_estimators': 200,
        'n_jobs': 8,
        'num_leaves': 50,
        'scale_pos_weight': 1.1789638932496076
    }
    JP_model = {
        'learning_rate': 0.1,
        'max_depth': 3,
        'n_estimators': 100,
        'n_jobs': 8,
        'num_leaves': 50,
        'scale_pos_weight': 1.5254730713245996
    }
    model = pd.read_pickle(path_model)
    return model


def train_pipeline(train_vect=False, train_model=False):
    """Training pipeline for loading, preprocessing and model training

    Args:
        train_vect (bool): indicates whether to retrain vectorizer, defaults to False
        train_model (bool): indicates whether to retrain models, defaults to False
    """
    df = load_and_save_data(mbti_cols, path_data, path_save_data)
    X_train, X_test, y_train, y_test = get_train_test(df[['posts_clean']], df[mbti_cols])
    if train_vect:
        vect = save_vectorizer(X_train['posts_clean'], path_vect)
    else:
        vect = load_vectorizer(path_vect)
    print(f'Vocabulary size: {len(vect.get_feature_names())}')
    vector_train = vect.transform(X_train['posts_clean']).astype(np.float64)
    vector_test = vect.transform(X_test['posts_clean']).astype(np.float64)
    for idx, col in enumerate(mbti_cols):
        print(f'Predicting for: {col}')
        if train_model:
            model = get_gridsearch_model(vector_train, y_train[col], path_model[idx])
        else:
            model = get_model(path_model[idx])
        y_pred = model.predict(vector_test)

        # Metric
        metric_acc = np.round(accuracy_score(y_test[col], y_pred) * 100, 1)
        metric_bal_acc = np.round(balanced_accuracy_score(y_test[col], y_pred)*100, 1)
        metric_f1 = np.round(f1_score(y_test[col], y_pred), 3)
        print(confusion_matrix(y_test[col], y_pred))
        print(f'For {col}: Accuracy: {metric_acc}% and Balanced Accuracy: {metric_bal_acc}%')
        print(f'F1 for {col}: {metric_f1}')
        print()


def test_pipeline(input_text):
    """Testing pipeline for new input text

    Args:
        input_text (str): input text

    Returns:
        2-element tuple

        - personality (str): MBTI personality results, to be shown in title of bar plot
        - predictions (list): list of model prediction probabilities
    """
    clean_input = clean_text(input_text)
    vect = load_vectorizer(path_vect)
    vector_input = vect.transform(pd.Series(clean_input)).astype(np.float64)
    personality = ''
    predictions = []
    for idx, _ in enumerate(mbti_cols):
        m = get_model(path_model[idx])
        y_pred = m.predict_proba(vector_input)
        predictions.append(y_pred[0])

        # Decode results
        if y_pred[0][0] >= 0.5:
            personality += mbti_cols[idx][1]
        else:
            personality += mbti_cols[idx][0]

    return personality, predictions


def get_num_words(input_text):
    """Get number of input words in vocabulary

    Args:
        input_text (str): input text

    Returns:
        (int)
    """
    wordnet.ensure_loaded()
    clean_input = clean_text(input_text)
    vect = load_vectorizer(path_vect)
    vector_input = vect.transform(pd.Series(clean_input)).astype(np.float64)
    n_words = scipy.sparse.csr_matrix.count_nonzero(vector_input)
    return n_words


def get_bar_plot(predictions, personality):
    """Get figure for plot

    Adds plotly.graph_objects charts for bar plot

    Args:
        predictions (list): list of model prediction probabilities
        personality (str): MBTI personality results, to be shown in title of bar plot

    Returns:
        (dict)
    """
    y_data = ['Introversion-Extroversion', 'Intuition-Sensing', 'Feeling-Thinking', 'Perceiving-Judging']
    x_data_0 = [r[0] for r in predictions]
    x_data_1 = [r[1] for r in predictions]
    data = [go.Bar(
        y=y_data,
        x=x_data_0,
        hoverinfo='none',
        orientation='h',
        marker_color='#BE9B89',
    ), go.Bar(
        y=y_data,
        x=x_data_1,
        hoverinfo='none',
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
                text=f"{yd.split('-')[0]}<br>{int(np.round(xd * 100, 0))}%",
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
                text=f"{yd.split('-')[1]}<br>{int(np.round(xd * 100, 0))}%",
                font=dict(size=14),
                showarrow=False)
        )

    layout = dict(
        title=f'Result: {personality}',
        annotations=annotations,
        bargap=0.3,
        barmode='stack',
        margin=dict(l=50, r=50, t=30, b=30),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(
            range=[0, 1],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            fixedrange=True
        ),
        yaxis=dict(
            categoryarray=y_data[::-1],
            showticklabels=False,
            fixedrange=True
        ),
        font=dict(
            family='Source Sans Pro',
            size='15'
        )
    )
    return dict(data=data, layout=layout)
