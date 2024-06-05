import re
import time
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
import nltk
from nltk.corpus import stopwords as nltk_stopwords
import flask
import config



import telebot
import time
import sqlite3
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from model_regr import clear_text, clean_stop_words, tfidf
from model_regr import model

WEBHOOK_URL_BASE = "https://{}:{}".format(config.WEBHOOK_HOST, config.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(config.TOKEN)

stopwords = set(nltk_stopwords.words('russian'))
np.array(stopwords)




conn = sqlite3.connect('final_res.db', check_same_thread=False)
cur = conn.cursor()

table_comments = """
SELECT *
FROM comments
"""

bot = telebot.TeleBot(config.TOKEN, threaded=False)

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет!")


@bot.message_handler(commands=['search_videos'])
def search_videos(message):
    msg = bot.send_message(message.chat.id, "Пришлите ссылку на видео в YouTube")
    bot.register_next_step_handler(msg, search)


def search(message):
    bot.send_message(message.chat.id, "Начинаю парсинг текстов комментариев. Подождите пожалуйста")
    scrapped = []
    with webdriver.Chrome() as driver:
        wait = webdriver.support.ui.WebDriverWait(driver, 1)
        driver.get(message.text)

        for item in tqdm(range(200)):
            wait.until(webdriver.support.expected_conditions.visibility_of_element_located(
                (By.TAG_NAME, "body"))).send_keys(webdriver.common.keys.Keys.END)
            time.sleep(2)

        for coment in wait.until(webdriver.support.expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#content"))):
            scrapped.append(coment.text)

        lines = [x.split('\nОТВЕТИТЬ')[0].split('\n')[1] for x in scrapped[0].split('назад')][1:]
        comments_shulman = lines + scrapped[1:]
        db_comments = {}
        for coment in comments_shulman:
            if coment not in db_comments:
                if db_comments.values():
                    db_comments[coment] = max(db_comments.values()) + 1
                else:
                    db_comments[coment] = 1
                cur.execute('INSERT OR IGNORE INTO comments VALUES (?, ?)', (len(db_comments), str(coment)))
                conn.commit()

    df_comments = pd.read_sql_query(table_comments, conn)

    df_comments['text_clear'] = df_comments['comment'] \
        .apply(lambda x: clean_stop_words(clear_text(str(x)), stopwords))

    X_test_result = tfidf.transform(df_comments['text_clear'])
    y_pred = model.predict(X_test_result)
    df_comments["answer"] = y_pred
    year_num = df_comments.groupby('answer')['id'].agg('count')
    year_num.plot(kind="bar")
    plt.savefig('abr.png')
    photo = open("abr.png", 'rb')
    bot.send_photo(message.chat.id, photo)

#while True:
 #   try:
  #      bot.polling(none_stop=True)

   # except Exception as e:
    #    print(e)

     #   time.sleep(15)


# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)

        time.sleep(15)


