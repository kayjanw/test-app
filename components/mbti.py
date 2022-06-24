import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import os
import re
import scipy

from dash import html
from lightgbm import LGBMClassifier
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    f1_score,
    balanced_accuracy_score,
)
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold

try:
    import tensorflow as tf
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
except ModuleNotFoundError:
    pass

# import nltk
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('wordnet')


class MBTI:
    """The MBTI object contains functions used for MBTI Personality Test tab"""

    def __init__(self):
        """Initialize class attributes

        Attributes:
            mbti_cols (list): name of new columns generated
            path_data (str): location and name of input data
            path_save_data (str): location and name of saved data
            path_vect (str): location and file name of saved vectorizer
            path_models (str): location and file name of saved models
            use_tf (bool): for modelling, whether to use tensorflow model
            n_words (int): for modelling, used in tensorflow model
            n_padding (int): for modelling, used in tensorflow model
            embedding_dim (int): for modelling, used in tensorflow model
            threshold (float): for modelling, used in tensorflow model
            non_sw (list): list of stop words to exclude
        """
        self.mbti_cols = ["EI", "SN", "TF", "JP"]
        self.path_data = "sample_data/mbti.csv"
        self.path_save_data = "sample_data/mbti_clean.csv"
        self.path_vect = "data/vocabulary.pkl"
        self.path_tokenizer = "data/tokenizer.pkl"
        self.path_models = []
        for col in self.mbti_cols:
            self.path_models.append(f"data/model_{col}.pkl")
        self.path_tf_models = []
        for col in self.mbti_cols:
            self.path_tf_models.append(f"data/model_tf_{col}.h5")

        # Parameters for modelling
        self.use_tf = False
        self.n_words = 1600
        self.n_padding = 1000
        self.embedding_dim = 64
        self.threshold = 0.5

        self.non_sw = [
            "ain",
            "aint",
            "aren",
            "arent",
            "cant",
            "couldn",
            "coulnt",
            "dont",
            "didn",
            "didnt",
            "doesn",
            "doesnt",
            "hadn",
            "hadnt",
            "hasn",
            "hasnt",
            "haven",
            "havent",
            "isn",
            "isnt",
            "mightn",
            "mightnt",
            "mustn",
            "mustnt",
            "needn",
            "neednt",
            "not",
            "shan",
            "shant",
            "shouldn",
            "shouldnt",
            "wasn",
            "wasnt",
            "weren",
            "werent",
            "won",
            "wont",
            "wouldn",
            "wouldnt",
        ]

    @staticmethod
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
            str: processed text
        """
        # Split sentences
        text = re.sub(r"\|\|\|", " ", text)

        # Make words lowercase
        text = text.lower()

        # Remove URL and usernames
        text = re.sub(r"http[^\s]*", "", text)
        text = re.sub("@[a-z0-9]+", "", text)

        # Remove digits and punctuations
        text = re.sub("[^a-z ]", "", text)

        # Remove any mention of MBTI types
        text = re.sub(r"[^\s]*[ie][ns][tf][jp][^\s]*", "", text)
        text = re.sub(r"[^\s]*mbti[^\s]*", "", text)

        # Tokenize words
        text_list = word_tokenize(text)

        # Lemmatize words
        text_list = [lemma.lemmatize(word) for word in text_list]

        # Join text into string
        text = " ".join(text_list)
        return text

    def load_and_save_data(self):
        """Reads in data, performs preprocessing and saves data
        If saved data is present, directly read in the saved data

        If saved data does not exist
            a) Reads in data
            b) Insert new columns as indicator for each mbti category
            c) Process text column
            d) Save data
        If saved data exist
            a) Reads in saved data

        Returns:
            pandas DataFrame: processed data
        """
        if not os.path.isfile(self.path_save_data):
            print("Read and save data file")
            df = pd.read_csv(self.path_data)

            # Insert new columns as indicator for each mbti category
            for idx, col in enumerate(self.mbti_cols):
                df[col] = df["type"].str[idx] == col[0]

            # Process text column
            df["posts_clean"] = df["posts"].apply(self.clean_text)

            # Save data
            df.to_csv(self.path_save_data, index=False)
        else:
            print("Load saved data file")
            df = pd.read_csv(self.path_save_data)

        return df

    @staticmethod
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
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        return X_train, X_test, y_train, y_test

    def save_vectorizer(self, corpus, params=None):
        """Fit, save and return vectorizer

        Args:
            corpus (pandas Series): input text corpus (training input)
            params (dict): specifies parameters for vectorizer, defaults to None

        Returns:
            (sklearn CountVectorizer)
        """
        sw = [self.clean_text(word) for word in stopwords.words("english")]
        sw = list(set(sw) - set(self.non_sw))
        if params is None:
            params = dict(
                ngram_range=(1, 3),
                max_df=0.95,
                min_df=0.05,
                max_features=None,
                stop_words=sw,
            )
        model = CountVectorizer(**params)
        vect = model.fit(corpus)
        # pickle.dump(vect, open(path_vect, 'wb'))
        pickle.dump(vect.get_feature_names_out(), open(self.path_vect, "wb"))
        return vect

    def load_vectorizer(self):
        """Load and return saved vectorizer

        Returns:
            sklearn CountVectorizer
        """
        # vect = pd.read_pickle(path_vect)
        vocabulary = pd.read_pickle(self.path_vect)
        vect = CountVectorizer(vocabulary=vocabulary)
        return vect

    def transform_vectorizer(self, vect, corpus):
        """Transform corpus with vectorizer

        Args:
            vect (sklearn CountVectorizer): vectorizer to be used to transform text corpus
            corpus (pandas Series): input text corpus

        Returns:
            vector_corpus (scipy csr_matrix): vectorized text corpus
        """
        vector_corpus = vect.transform(corpus).astype(np.float64)
        return vector_corpus

    def save_tokenizer(self, corpus, params=None):
        """Fit, save and return tokenizer

        Args:
            corpus (pandas Series): input text corpus (training input)
            params (dict): specifies parameters for tokenizer, defaults to None

        Returns:
            keras Tokenizer
        """
        if params is None:
            params = dict(
                num_words=self.n_words, oov_token="<OOV>", lower=True, split=" "
            )
        tokenizer = Tokenizer(**params)
        tokenizer.fit_on_texts(corpus)
        pickle.dump(tokenizer, open(self.path_tokenizer, "wb"))
        return tokenizer

    def load_tokenizer(self):
        """Load and return saved tokenizer

        Returns:
            keras Tokenizer
        """
        tokenizer = pd.read_pickle(self.path_tokenizer)
        return tokenizer

    def transform_tokenizer(self, tokenizer, corpus):
        """Transform corpus with tokenizer

        Args:
            tokenizer (keras Tokenizer): tokenizer to be used to transform text corpus
            corpus (pandas Series): input text corpus

        Returns:
            vector_corpus (numpy ndarray): tokenized text corpus
        """
        corpus_sequences = tokenizer.texts_to_sequences(corpus)
        vector_corpus = pad_sequences(
            corpus_sequences, padding="post", truncating="post", maxlen=self.n_padding
        )
        return vector_corpus

    @staticmethod
    def save_model(vector_train, y_train_series, path_model):
        """Train, save and return best model after grid search with stratified cross validation

        Args:
            vector_train (scipy csr_matrix): vectorized training input
            y_train_series (pandas Series): training output, one-column subset of y_train
            path_model (str): location and file name of saved model

        Returns:
            model
        """
        scale_pos_weight1 = len(y_train_series) / sum(y_train_series)
        scale_pos_weight2 = (len(y_train_series) - sum(y_train_series)) / sum(
            y_train_series
        )
        clf = LGBMClassifier()
        values = {
            "n_estimators": [20, 50, 100, 200],
            "max_depth": [3, 5],
            "num_leaves": [50, 100],
            "n_jobs": [8],
            "learning_rate": [0.1, 0.2, 0.3],
            "scale_pos_weight": [scale_pos_weight1, scale_pos_weight2],
        }
        grid = GridSearchCV(
            clf, param_grid=values, cv=StratifiedKFold(3), scoring="balanced_accuracy"
        )
        grid.fit(vector_train, y_train_series)
        print("Best parameters: ", grid.best_params_)

        # Retrain model on entire data
        params = grid.best_estimator_.get_params()
        model = LGBMClassifier(**params)
        model.fit(vector_train, y_train_series)
        pickle.dump(model, open(path_model, "wb"))
        return model

    @staticmethod
    def load_model(path_model):
        """Load and return saved best model after grid search with stratified cross validation

        Args:
            path_model (str): location and file name of saved model

        Returns:
            model
        """
        EI_model = {
            "learning_rate": 0.1,
            "max_depth": 3,
            "n_estimators": 200,
            "n_jobs": 8,
            "num_leaves": 50,
            "scale_pos_weight": 4.342928660826033,
        }
        SN_model = {
            "learning_rate": 0.2,
            "max_depth": 3,
            "n_estimators": 50,
            "n_jobs": 8,
            "num_leaves": 50,
            "scale_pos_weight": 7.251828631138976,
        }
        TF_model = {
            "learning_rate": 0.2,
            "max_depth": 3,
            "n_estimators": 200,
            "n_jobs": 8,
            "num_leaves": 50,
            "scale_pos_weight": 1.1789638932496076,
        }
        JP_model = {
            "learning_rate": 0.1,
            "max_depth": 3,
            "n_estimators": 200,
            "n_jobs": 8,
            "num_leaves": 50,
            "scale_pos_weight": 1.5263924281033856,
        }
        model = pd.read_pickle(path_model)
        return model

    @staticmethod
    def predict_model(model, vector_test):
        """Perform prediction on test set

        Args:
            model (model): model to be used for prediction
            vector_test (scipy csr_matrix): vectorized training input

        Returns:
            y_pred (numpy ndarray)
        """
        y_pred = model.predict(vector_test)
        return y_pred

    def save_model_tf(self, vector_train, y_train_series, path_model):
        """Train, save and return tensorflow model

        Args:
            vector_train (numpy ndarray): vectorized training input
            y_train_series (pandas Series): training output, one-column subset of y_train
            path_model (str): location and file name of saved model

        Returns:
            model
        """
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Embedding(
                    self.n_words, self.embedding_dim, input_length=self.n_padding
                ),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(6, activation="relu"),
                tf.keras.layers.Dense(1, activation="sigmoid"),
            ]
        )
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["acc"])
        model.fit(
            vector_train, y_train_series, validation_split=0.2, epochs=3, verbose=2
        )
        model.save(path_model)
        return model

    @staticmethod
    def load_model_tf(path_model):
        """Load and return saved tensorflow model

        Args:
            path_model (str): location and file name of saved model

        Returns:
            model
        """
        model = tf.keras.models.load_model(path_model)
        return model

    def predict_model_tf(self, model, vector_test):
        """Perform prediction on test set

        Args:
            model (model): model to be used for prediction
            vector_test (numpy ndarray): vectorized training input

        Returns:
            y_pred (numpy ndarray)
        """
        y_pred = model.predict(vector_test) > self.threshold
        return y_pred

    def train_pipeline(self, train_vect=False, train_model=False):
        """Training pipeline for loading, preprocessing and model training

        Args:
            train_vect (bool): indicates whether to retrain vectorizer, defaults to False
            train_model (bool): indicates whether to retrain models, defaults to False

        Returns:
            NA
        """
        df = self.load_and_save_data()
        X_train, X_test, y_train, y_test = self.get_train_test(
            X=df[["posts_clean"]], y=df[self.mbti_cols]
        )

        # Initialize/load vectorizer and transform text
        if not self.use_tf:
            if train_vect:
                print("Initialize and save vectorizer")
                vect = self.save_vectorizer(X_train["posts_clean"])
            else:
                vect = self.load_vectorizer()
            print(f"Vocabulary size: {len(vect.get_feature_names_out())}")
            vector_train = self.transform_vectorizer(vect, X_train["posts_clean"])
            vector_test = self.transform_vectorizer(vect, X_test["posts_clean"])

        else:
            if train_vect:
                print("Initialize and save tokenizer")
                tokenizer = self.save_tokenizer(X_train["posts_clean"])
            else:
                tokenizer = self.load_tokenizer()
            print(f"Vocabulary size: {self.n_words}")
            vector_train = self.transform_tokenizer(tokenizer, X_train["posts_clean"])
            vector_test = self.transform_tokenizer(tokenizer, X_test["posts_clean"])

        # Initialize/load model and get prediction
        for idx, col in enumerate(self.mbti_cols):
            print(f"Predicting for: {col}")
            if not self.use_tf:
                if train_model:
                    model = self.save_model(
                        vector_train, y_train[col], self.path_models[idx]
                    )
                else:
                    model = self.load_model(self.path_models[idx])
                y_pred = self.predict_model(model, vector_test)
            else:
                if train_model:
                    model = self.save_model_tf(
                        vector_train, y_train[col], self.path_tf_models[idx]
                    )
                else:
                    model = self.load_model_tf(self.path_tf_models[idx])
                y_pred = self.predict_model_tf(model, vector_test)

            # Metric
            metric_acc = np.round(accuracy_score(y_test[col], y_pred) * 100, 1)
            metric_bal_acc = np.round(
                balanced_accuracy_score(y_test[col], y_pred) * 100, 1
            )
            metric_f1 = np.round(f1_score(y_test[col], y_pred), 3)
            print(confusion_matrix(y_test[col], y_pred))
            print(
                f"For {col}: Accuracy: {metric_acc}% and Balanced Accuracy: {metric_bal_acc}%"
            )
            print(f"F1 for {col}: {metric_f1}")
            print()

    def get_feature_importance(self, max_num_features=10):
        """Print top feature importance for each model

        Args:
            max_num_features (int): number of top feature importance
        """
        vect = self.load_vectorizer()
        vocab = vect.vocabulary
        for idx, col in enumerate(self.mbti_cols):
            print(f"\nFeature Importance for: {col}")
            model = self.load_model(self.path_models[idx])
            fi = list(zip(model.feature_importances_, vocab))
            fi_sorted = sorted(fi, key=lambda x: x[0], reverse=True)
            for idx2 in range(max_num_features):
                print(fi_sorted[idx2])

    def vectorize_new_input(self, input_text):
        """Load saved vectorizer and transform input text

        Args:
            input_text (str): input text

        Returns:
            scipy csr_matrix: vectorized input_text
        """
        try:
            wordnet.ensure_loaded()
        except AttributeError:
            wordnet.ensure_loaded()
        clean_input = self.clean_text(input_text)
        vect = self.load_vectorizer()
        vector_input = self.transform_vectorizer(vect, pd.Series(clean_input))
        return vector_input

    def tokenize_new_input(self, input_text):
        """Load saved tokenizer and transform input text

        Args:
            input_text (str): input text

        Returns:
            numpy ndarray: tokenized input_text
        """
        try:
            wordnet.ensure_loaded()
        except AttributeError:
            wordnet.ensure_loaded()
        clean_input = self.clean_text(input_text)
        tokenizer = self.load_tokenizer()
        tokenizer_input = self.transform_tokenizer(tokenizer, pd.Series(clean_input))
        return tokenizer_input

    def test_pipeline(self, input_text):
        """Testing pipeline for new input text

        Args:
            input_text (str): input text

        Returns:
            2-element tuple

            - personality (str): MBTI personality results, to be shown in title of bar plot
            - predictions (list): list of tuple of model prediction probabilities
        """
        if not self.use_tf:
            vector_input = self.vectorize_new_input(input_text)
        else:
            vector_input = self.tokenize_new_input(input_text)

        personality = ""
        predictions = []
        for idx, _ in enumerate(self.mbti_cols):
            if not self.use_tf:
                m = MBTI.load_model(self.path_models[idx])
                y_prob = m.predict_proba(vector_input)[:, 1][0]
            else:
                m = MBTI.load_model_tf(self.path_tf_models[idx])
                y_prob = m.predict(vector_input)[0][0]
            predictions.append((1 - y_prob, y_prob))

            # Decode results
            if y_prob >= self.threshold:
                personality += self.mbti_cols[idx][0]
            else:
                personality += self.mbti_cols[idx][1]

        return personality, predictions

    def get_num_words(self, input_text):
        """Get number of input words in vocabulary

        Args:
            input_text (str): input text

        Returns:
            int
        """
        if not self.use_tf:
            vector_input = self.vectorize_new_input(input_text)
            n_words = scipy.sparse.csr_matrix.count_nonzero(vector_input)
        else:
            vector_input = self.tokenize_new_input(input_text)
            n_words = sum((vector_input > 1)[0])
        return n_words

    @staticmethod
    def get_bar_plot(predictions):
        """Get figure for plot

        Adds plotly.graph_objects charts for bar plot

        Args:
            predictions (list): list of model prediction probabilities

        Returns:
            dict
        """
        y_data = [
            "Introversion-Extroversion",
            "Intuition-Sensing",
            "Feeling-Thinking",
            "Perceiving-Judging",
        ]
        x_data_0 = [r[0] for r in predictions]
        x_data_1 = [r[1] for r in predictions]
        data = [
            go.Bar(
                y=y_data,
                x=x_data_0,
                hoverinfo="none",
                orientation="h",
                marker_color="#BE9B89",
            ),
            go.Bar(
                y=y_data,
                x=x_data_1,
                hoverinfo="none",
                orientation="h",
                marker_color="#D6CAC7",
            ),
        ]

        annotations = []
        for yd, xd in zip(y_data, x_data_0):
            annotations.append(
                dict(
                    xref="paper",
                    yref="y",
                    x=xd / 2,
                    y=yd,
                    xanchor="center",
                    text=f"{yd.split('-')[0]}<br>{int(np.round(xd * 100, 0))}%",
                    font=dict(size=14),
                    showarrow=False,
                )
            )

        for yd, xd in zip(y_data, x_data_1):
            annotations.append(
                dict(
                    xref="paper",
                    yref="y",
                    x=1 - (xd / 2),
                    y=yd,
                    xanchor="center",
                    text=f"{yd.split('-')[1]}<br>{int(np.round(xd * 100, 0))}%",
                    font=dict(size=14),
                    showarrow=False,
                )
            )

        layout = dict(
            annotations=annotations,
            bargap=0.3,
            barmode="stack",
            margin=dict(l=50, r=50, t=20, b=30),
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            xaxis=dict(
                range=[0, 1],
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                fixedrange=True,
            ),
            yaxis=dict(
                categoryarray=y_data[::-1], showticklabels=False, fixedrange=True
            ),
            font=dict(family="Source Sans Pro", size="15"),
        )
        return dict(data=data, layout=layout)

    @staticmethod
    def get_personality_details(personality):
        """Get personality details (summary and details)

        Args:
            personality (str): MBTI personality results, to retrieve detailed results

        Returns:
            list
        """
        mbti_dict = {
            "INTJ": {
                "summary": "Architect",
                "details": "Imaginative and strategic thinkers, with a plan for everything",
            },
            "INTP": {
                "summary": "Logician",
                "details": "Innovative inventors with an unquenchable thirst for knowledge",
            },
            "ENTJ": {
                "summary": "Commander",
                "details": "Bold, imaginative and strong-willed leaders, "
                   "always finding a way - or making one",
            },
            "ENTP": {
                "summary": "Debator",
                "details": "Smart and curious thinkers who cannot resist an intellectual challenge",
            },
            "INFJ": {
                "summary": "Advocate",
                "details": "Quiet and mystical, yet very inspiring and tireless idealists",
            },
            "INFP": {
                "summary": "Mediator",
                "details": "Poetic, kind and altruistic people, always eager to help a good cause",
            },
            "ENFJ": {
                "summary": "Protagonist",
                "details": "Charismatic and inspiring leaders, able to mesmerize their listeners",
            },
            "ENFP": {
                "summary": "Campaigner",
                "details": "Enthusiastic, creative and sociable free spirits, "
                   "who can always find a reason to smile",
            },
            "ISTJ": {
                "summary": "Logistician",
                "details": "Practical and fact-minded individuals, "
                   "whose reliability cannot be doubted",
            },
            "ISFJ": {
                "summary": "Defender",
                "details": "Very dedicated and warm protectors, "
                   "always ready to defend their loved ones",
            },
            "ESTJ": {
                "summary": "Executive",
                "details": "Excellent administrators, unsurpassed at managing things - or people",
            },
            "ESFJ": {
                "summary": "Consul",
                "details": "Extraordinarily caring, social and popular people, "
                   "always eager to help",
            },
            "ISTP": {
                "summary": "Virtuoso",
                "details": "Bold and practical experimenters, masters of all kinds of tools",
            },
            "ISFP": {
                "summary": "Adventurer",
                "details": "Flexible and charming artists, "
                   "always ready to explore and experience something new",
            },
            "ESTP": {
                "summary": "Entrepreneur",
                "details": "Smart, energetic and very perceptive people, "
                   "who truly enjoy living on the edge",
            },
            "ESFP": {
                "summary": "Entertainer",
                "details": "Spontaneous, energetic and enthusiastic people - "
                   "life is never boring around them",
            },
        }
        summary = f"Result: {personality} ({mbti_dict[personality]['summary']})"
        details = mbti_dict[personality]["details"]
        return [html.P(summary, style={"font-size": 20}), html.P(details)]
