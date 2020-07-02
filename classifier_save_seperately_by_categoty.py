# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:15:44 2018

@author: jbk48
@editor: lumyjuwon
"""
import time
import tensorflow as tf
from LSTM_material2 import Bi_LSTM as Bi_LSTM, Word2Vec as Word2Vec
import gensim
import numpy as np
import csv


def Convert2Vec(model_name, sentence):
    word_vec = []
    sub = []
    model = gensim.models.word2vec.Word2Vec.load(model_name)
    for word in sentence:
        if (word in model.wv.vocab):
            sub.append(model.wv[word])
        else:
            sub.append(np.random.uniform(-0.25, 0.25, 300))  # used for OOV words
    word_vec.append(sub)
    return word_vec


def Grade(sentence):
    tokens = W2V.tokenize(sentence)

    embedding = Convert2Vec('/Users/chaeyeonhwang/Documents/PBL/LSTM_material2/data/postnegpos3.embedding', tokens)
    zero_pad = W2V.Zero_padding(embedding, Batch_size, Maxseq_length, Vector_size)
    global sess
    result = sess.run(prediction, feed_dict={X: zero_pad, seq_len: [
        len(tokens)]})  # tf.argmax(prediction, 1)이 여러 prediction 값중 max 값 1개만 가져옴
    point = result.ravel()  # type is ndarray
    Tag = ["중립", "부정", "긍정"]

    for t, i in zip(Tag, point):
        percent = t + str(round(i * 100, 2)) + "%"

        if max(point) == point[0]:
            pointclass = '중립'
        elif max(point) == point[1]:
            pointclass = '부정'
        else:
            pointclass = '긍정'

    line2 = [line[0], round(point[0] * 100, 2), round(point[1] * 100, 2), round(point[2] * 100, 2),pointclass]
    array = np.array(line2)
    return array



W2V = Word2Vec.Word2Vec()

Batch_size = 1
Vector_size = 600
Maxseq_length = 100000 # Max length of training data
learning_rate = 0.001
lstm_units = 128
num_class = 3
keep_prob = 0.75

X = tf.placeholder(tf.float32, shape=[None, Maxseq_length, Vector_size], name='X')
Y = tf.placeholder(tf.float32, shape=[None, num_class], name='Y')
seq_len = tf.placeholder(tf.int32, shape=[None])

BiLSTM = Bi_LSTM.Bi_LSTM(lstm_units, num_class, keep_prob)

with tf.variable_scope("loss", reuse=tf.AUTO_REUSE):
    logits = BiLSTM.logits(X, BiLSTM.W, BiLSTM.b, seq_len)
    loss, optimizer = BiLSTM.model_build(logits, Y, learning_rate)

prediction = tf.nn.softmax(logits)  # softmax

saver = tf.train.Saver()
init = tf.global_variables_initializer()
modelName = "/Users/chaeyeonhwang/Documents/PBL/LSTM_material2/data/Bi_LSTMposneg3.model"

start_time = time.time()
sess = tf.Session()

sess.run(init)
saver.restore(sess, modelName)


f = open('/Users/chaeyeonhwang/Documents/PBL/LSTM_material2/csv/202002/202002comments.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
i = 0

for line in rdr:

    tik = Grade(line[0])

    if tik[4] == '중립':
        i = i + 1
        print(i)
        print(tik[4])
        file1 = open('/Users/chaeyeonhwang/Documents/PBL/LSTM_material2/csv/202002/[중립]comments_new.csv', 'a', newline='')
        writer1 = csv.writer(file1)
        writer1.writerow(tik)

    elif tik[4] == '부정':
        i = i + 1
        print(i)
        print(tik[4])
        file2 = open('/Users/chaeyeonhwang/Documents/PBL/LSTM_material2/csv/202002/[부정]comments_new.csv', 'a', newline='')
        writer2 = csv.writer(file2)
        writer2.writerow(tik)

    else:
        i = i + 1
        print(i)
        print(tik[4])
        file3 = open('/Users/chaeyeonhwang/Documents/PBL/LSTM_material2/csv/202002/[긍정]comments_new.csv', 'a', newline='')
        writer3 = csv.writer(file3)
        writer3.writerow(tik)


duration = time.time() - start_time
minute = int(duration / 60)
second = int(duration) % 60
print("%dminutes %dseconds" % (minute, second))

