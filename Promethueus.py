#coding:utf-8
import jieba
from model import db_session,words_space

def cut_from_db():
	pass
	#use api get words
def cut_word(word):
	return jieba.lcut(word,cut_all=True)
def get_word_vector(words):
	space = get_word_space()
	vector = []
	for word in space:
		if word.key in words:
			vector.append(1)
		else:
			vector.append(0)
	return vector
def insert_db(word_list):
	for word in word_list:
		word = words_space(word)
		db_session.add(word)
		try:
			db_session.commit()
		except Exception as e:
			db_session.rollback()
def get_word_space():
	return db_session.query(words_space).all()
if __name__ == '__main__':
	import sys
	word = sys.argv[1]
	fee = sys.argv[2]
	list = cut_word(word)
	insert_db(list)
	words = get_word_space()
	print ' '.join([word.key for word in words])
	print ''.join(str(get_word_vector(list)))
