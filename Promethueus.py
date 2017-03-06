# coding:utf-8
import jieba
from model import db_session, words_space, init_db
from sqlalchemy import text, desc
import requests


def cut_from_db():
    url = 'http://127.0.0.1/escorts/'
    headers = {
        'xxx-base': 'gAAAAABYvPEynmeCquTyAcldLEu8M22D_bL5xxeBghulrAPankPBcwUgjK0TIBZsJqp6_4xmXUXduZsRrZkVmd_xfvi5Ts7qYkDEvbyq7di986HVZ-dNFYJGjEHPsj_6jf0HwVxmchkVVrxN4LajmW2ruXEzFf4KyVYxKvkMagF3Bq-9AFnqodSNv-NZ1zAYX9NfatVp69lMUpfXEXjQxLtuGTpYIstQJc0bNpWbl_sIu5ooFOtJCI2H6MxQJQT4fRFhCet-46RemrONlApTz7tpQ3l1VAkN2AlRHwaA-e44B27NygBOJ4U=',
        'xxx-access-key': 'seifj28304)'
    }
    response = requests.get(url=url, headers=headers)
    words = ''
    data = response.json().get('data')
    print(data)
    for d in data:
        words = d.get('information') + ' ' + words
    word_list = cut_word(words)
    return word_list


def cut_word(word):
    return jieba.lcut(word, cut_all=True)


def get_word_vector(words):
    space = get_word_space()
    vector = []
    for word in space:
        if word.key in words:
            vector.append(1)
        else:
            vector.append(0)
    return vector


def romve_stop_word(word_list):
    with open('stop_word.txt') as file:
        f = ''.join([f.decode('utf-8') for f in file])
        return [w for w in word_list if w not in f]


def insert_db(word_list):
    for word in word_list:
        word = words_space(word)
        exsits = db_session.query(words_space).filter(
            words_space.key == word.key).one_or_none()
        if exsits:
            db_session.query(words_space).filter(
                words_space.key == word.key).update({'count': exsits.count + 1})
        else:
            word.count = 1
            db_session.add(word)
        try:
            db_session.commit()
        except Exception:
            db_session.rollback()


def get_word_space():
    return db_session.query(words_space)
if __name__ == '__main__':
    # import sys
    # word = sys.argv[1]
    # list = cut_word(word)
    # insert_db(list)
    # words = get_word_space()
    # print ' '.join([word.key for word in words])
    # print ''.join(str(get_word_vector(list)))
    init_db()
    word_list = cut_from_db()
    word_list = romve_stop_word(word_list)
    insert_db(word_list)
    space = get_word_space()
    space = space.order_by(desc(words_space.key))
    print(','.join([s.key for s in space]))
