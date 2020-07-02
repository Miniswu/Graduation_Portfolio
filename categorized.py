from konlpy.tag import Twitter
from gensim.models import Word2Vec
import csv

twitter = Twitter()

file = open("/Users/chaeyeonhwang/Documents/PBL/LSTM_material2/csv/traincomments.csv", 'r', encoding='utf-8')
line = csv.reader(file)
token = []
embeddingmodel = []
category = ('중립', '부정', '긍정')


for i in line:
    sentence = twitter.pos(i[0], norm=True, stem=True)
    temp = []
    temp_embedding = []
    all_temp = []
    for k in range(len(sentence)):
        temp_embedding.append(sentence[k][0])
        temp.append(sentence[k][0] + '/' + sentence[k][1])
    all_temp.append(temp)
    embeddingmodel.append(temp_embedding)
    category_number_dic = {'중립': 0, '부정': 1, '긍정': 2}
    all_temp.append(category_number_dic.get(category))
    token.append(all_temp)
print("토큰 처리 완료")

embeddingmodel = []
for i in range(len(token)):
    temp_embeddingmodel = []
    for k in range(len(token[i][0])):
        temp_embeddingmodel.append(token[i][0][k])
    embeddingmodel.append(temp_embeddingmodel)

embedding = Word2Vec(embeddingmodel, size=300, window=5, min_count=10, iter=5, sg=1, max_vocab_size=360000000)
embedding.save('postnegpos3.embedding')