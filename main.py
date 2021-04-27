import telebot
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_argument("--headless")


bot = telebot.TeleBot("1761224186:AAEvD5uXlIu_npAwb7Zb5hFGnUE4y08riv4")

driver = webdriver.Chrome(options=chrome_options)


@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, незнакомец!')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBM4ZggdiLL_d0TzTEswzstCUAARmcHP4AAhQBAALuymcQhbQTQCHU1KIfBA')
    bot.send_message(message.chat.id, 'Чтобы узнать, что я умею - введи команду "/about"')


@bot.message_handler(commands= ['about'])
def about(message):
    bot.send_message(message.chat.id, 'Зачем я нужен? Я помогу найти тебе фильм/сериал/аниме, покажу его оценку, описан'
                                      'ие и дам тебе ссылку на кинопоиск')
    bot.send_message(message.chat.id, 'Чтобы воспользоваться поиском, введи команду "/search_film"')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBM_JggtWnCc7WQCPlScoqSnY7sOZuGgACOQEAAu7KZxAn8u7UTjb6mh8E')


@bot.message_handler(commands= ['search_film'])
def search_films(message):
   msg = bot.send_message(message.chat.id, 'Введите фильм, который хотите найти')
   bot.register_next_step_handler(msg, search)

@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, 'Ебало, уткни')
def search(message):
    bot.send_message(message.chat.id, 'Произвожу поиск по кинопоиску')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBM-9ggtV21L_huTFjl2l95RBvHmDAUAAC3wAD7spnEA329LwL0r38HwQ')
    kinopoisk = 'https://www.kinopoisk.ru/index.php?kp_query=' + message.text
    driver.get(kinopoisk)
    sleep(2)

    try:
        title = driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr/td[1]/div/div[2]/div/div[2]/p/a')
        rating = driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr/td[1]/div/div[2]/div/div[1]/div')
        director_country_zhanr = driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr/td[1]/div/div[2]/div/div[2]/span[2]')
        actors = driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr/td[1]/div/div[2]/div/div[2]/span[3]')
        link = driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr/td[1]/div/div[2]/div/div[2]/p/a')

        final_title = 'Фильм: ' + title.text
        final_rating = 'Оценка фильма: ' + rating.text
        final_actors = 'Главные роли: ' + actors.text
        final_director_country_zhanr = 'Страна, режиссер, жанр: ' + director_country_zhanr.text
        final_link = 'Перейти на кинопоиск: ' + link.get_attribute('href')

        bot.send_message(message.chat.id, final_title)
        bot.send_message(message.chat.id, final_rating)
        bot.send_message(message.chat.id, final_actors)
        bot.send_message(message.chat.id, final_director_country_zhanr)
        bot.send_message(message.chat.id, final_link)

        if float(rating.text) > float(6.5) and float(rating.text) < float(8.5):
            bot.send_message(message.chat.id, 'Рекомендую к просмотру :3')
        elif float(rating.text) >= float(8.5):
            bot.send_message(message.chat.id, 'Категорически рекомендую к просмотру :D')
        else:
            bot.send_message(message.chat.id, 'Можете рискнуть, но я не советую смотреть это :(')
    except:
       bot.send_message(message.chat.id, 'Извините, но по вашему запросу ничего не найдено')



bot.polling()
