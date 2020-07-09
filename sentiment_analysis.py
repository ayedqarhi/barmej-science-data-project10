from database_service import get_data, get_data_count
import re
import pickle
from sklearn.metrics import accuracy_score

def get_accuracy(real_val, pred_val):
        return accuracy_score(real_val, pred_val)

def get_total_data_count():
        count_negative = get_data_count('negative', '1000')
        count_positive = get_data_count('positive', '1000')
        return dict({0:count_negative,1:count_positive})

def clean_text(text):
	text = text.lower()
	text = re.sub("@[a-z0-9_]+", ' ', text)
	text = re.sub("[^ ]+\.[^ ]+", ' ', text)
	text = re.sub("[^ ]+@[^ ]+\.[^ ]", ' ', text)
	text = re.sub("[^a-z\' ]", ' ', text)
	text = re.sub(' +', ' ', text)
	return text


result = get_data('1000', 'asc')

review = result['review']
sentiment = result['sentiment']

print(review)

clean_review = []

for i in range(len(review)):
	clean_review.append(clean_text(review[i]))

with open('model.pickle', 'rb') as file:
	model = pickle.load(file)

with open('vectorizer.pickle', 'rb') as file:
	vectorizer = pickle.load(file)

vector = vectorizer.transform(clean_review)
pred_sent = model.predict(vector)

print('-'*30)
print('Accuracy is : ', get_accuracy(sentiment, pred_sent))
print('-'*30)
output = get_total_data_count()
print('Negative count: ', output[0])
print('Poisitive count: ', output[1])
print('-'*30)
