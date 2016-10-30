# -*- coding: utf-8 -*-

import os
from lxml import objectify

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split

from handler import ItemSelector


def parse_xml(path):
    print("path ", path)
    xml = objectify.parse(open(path, 'r', encoding='utf-8'))
    root = xml.getroot()
    children = root.getchildren()
    df = pd.DataFrame(columns=('id', 'name', 'category', 'about', 'description', 'fans_country_VN'))

    for i in range(0, len(children)):
        obj = children[i].getchildren()
        row = dict(zip(['id', 'name', 'category', 'about', 'description', 'fans_country_VN'],
                       [obj[0].text, obj[1].text, obj[2].text, obj[3].text, obj[4].text, obj[5].text]))
        row_s = pd.Series(row)
        row_s.name = i
        df = df.append(row_s)
    return df


gnb = GaussianNB()

dir_path = os.path.dirname(os.path.realpath(__file__))
print("dir_path ", dir_path)
train_data_dir_path = dir_path + "/data/train/"
print("train_data_dir_path ", train_data_dir_path)


def load_data():
    global page_accountant, page_chinese, page_english, page_hotel, page_restaurant, page_travel, page_other, page_vocational
    page_accountant = parse_xml(train_data_dir_path + "accountant/page_accountant.xml")
    page_chinese = parse_xml(train_data_dir_path + "chinese/page_chinese.xml")
    page_english = parse_xml(train_data_dir_path + "english/page_english.xml")
    page_hotel = parse_xml(train_data_dir_path + "hotel/page_hotel.xml")
    page_it = parse_xml(train_data_dir_path + "it/page_it.xml")
    page_other = parse_xml(train_data_dir_path + "other/page_other.xml")
    page_restaurant = parse_xml(train_data_dir_path + "restaurant/page_restaurant.xml")
    page_travel = parse_xml(train_data_dir_path + "travel/page_travel.xml")
    page_vocational = parse_xml(train_data_dir_path + "vocational/page_vocational.xml")

    page_accountant["class"] = "accountant"
    page_chinese["class"] = "chinese"
    page_english["class"] = "english"
    page_hotel["class"] = "hotel"
    page_it["class"] = "it"
    page_other["class"] = "other"
    page_restaurant["class"] = "restaurant"
    page_travel["class"] = "travel"
    page_vocational["class"] = "vocational"


load_data()

data = pd.concat([page_accountant, page_chinese, page_english, page_restaurant, page_travel, page_other, page_hotel,
                  page_vocational])

data.fillna(value="", inplace=True)

x_train, x_test, y_train, y_test = train_test_split(data, data["class"], test_size=0.33, random_state=42)

combined_features = Pipeline([("feature", FeatureUnion(
    transformer_list=[
        # Pipeline for pulling features from the post's subject line
        ('name', Pipeline([
            ('selector', ItemSelector(key='name')),
            ('tfidf', TfidfVectorizer(min_df=50)),
        ])),
        # Pipeline for standard bag-of-words model for body
        ('description', Pipeline([
            ('selector', ItemSelector(key='description')),
            ('tfidf', TfidfVectorizer(min_df=50)),
        ])),
        ('about', Pipeline([
            ('selector', ItemSelector(key='about')),
            ('tfidf', TfidfVectorizer(min_df=50)),
        ]))
    ])), ('chi', SelectKBest(score_func=chi2, k=50))])

combined_features.fit(x_train, y_train)
x_fommated = combined_features.transform(x_train)

model = gnb.fit(x_fommated.toarray(), y_train)
print('LogisticRegression score: %f' % model.score(combined_features.transform(x_test).toarray(), y_test))

confusion_matrix(y_test, model.predict(combined_features.transform(x_test).toarray()))
print(classification_report(y_test, model.predict(combined_features.transform(x_test).toarray())))

dir_path = dir_path.replace("/training", "")
model_data_dir_path = dir_path + "/model/"
print("model_data_dir_path ", model_data_dir_path)
joblib.dump(combined_features, model_data_dir_path + 'tfidf_model.pkl')
joblib.dump(model, model_data_dir_path + 'prediction_model.pkl')
