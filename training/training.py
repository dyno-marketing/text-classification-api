from lxml import objectify
import pandas as pd


def parse_xml(path):
    xml = objectify.parse(open(path))
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


page_accounts = parse_xml("page_accountant.xml")
page_chinese = parse_xml("page_chinese.xml")
page_english = parse_xml("page_english.xml")
page_restaurant = parse_xml("page_restaurant.xml")
page_travel = parse_xml("page_travel.xml")
other = parse_xml("page_drop.xml")

page_accounts["class"] = "accounts"
page_chinese["class"] = "chinese"
page_english["class"] = "english"
page_restaurant["class"] = "restaurant"
page_travel["class"] = "travel"
other["class"] = "other"

data = pd.concat([page_accounts, page_chinese, page_english, page_restaurant, page_travel, other])

data.fillna(value="", inplace=True)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    data, data["class"], test_size=0.33, random_state=42)

from sklearn.pipeline import Pipeline, FeatureUnion

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_footer
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_quoting
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at a provided key.

    The data is expected to be stored in a 2D data structure, where the first
    index is over features and the second is over samples.  i.e.

    >> len(data[key]) == n_samples

    Please note that this is the opposite convention to scikit-learn feature
    matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[key]).  Examples include: a dict of lists, 2D numpy array, Pandas
    DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
               'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample.  (e.g. a
    list of dicts).  If your data is structured this way, consider a
    transformer along the lines of `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    key : hashable, required
        The key corresponding to the desired value in a mappable.
    """

    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

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

combined_features.fit(X_train, y_train)

X_fommated = combined_features.transform(X_train)

from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
model = gnb.fit(X_fommated.toarray(), y_train)

print('LogisticRegression score: %f'
      % model.score(combined_features.transform(X_test).toarray(), y_test))

from sklearn.metrics import confusion_matrix

confusion_matrix(y_test, model.predict(combined_features.transform(X_test).toarray()))

from sklearn.metrics import classification_report

print(classification_report(y_test, model.predict(combined_features.transform(X_test).toarray())))

from sklearn.externals import joblib

joblib.dump(combined_features, 'tfidf_model.pkl')
joblib.dump(model, 'prediction_model.pkl')
