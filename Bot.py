import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard
import Sql


# token = 'vk1.a.-QHwbJAI2dDNDaChBFEzMajbLtDa8uRk_6e7KUKJ78XlOHsvy3TZruMMZEhYC49qHl1VQx2Iq9FattQdMBqVQ0Zb5sI3qa2bFL-0qHsukOJRvdUYDQlFutvMIcRSoEnLX52jlHvwzgTeDLB0xqKYdtOEq4Y-ARnHYvmVHvTD5SCJ6VsVdGa9732tyePFp6zjhJ1kqWlWzExWP5AvpTQVVw'
token = 'vk1.a.vVTUL3FEmGVCpJb_JxI-NsmJcQt4ImcCWmxvPbpJT5uPM3YXk18defZw2UrV8k-AhcMh6fVSTAtWJYb-rGWQnx74sd4dg9GOcbD78LHP9hur6CHcvmOIRJ2VwbRwnwPh0fcGCdMt8p79N1EpljgtVPrnl392MfOo6FIYjnbagpGIK8Te-6XpvEbZYI3v31RTyAK-7b4jrmYHNmaE6vt_tg'
session = vk_api.VkApi(token = token)
list_of_users_in_vacation = []
list_of_users_in_service = []
list_of_auth_users = Sql.select_all_from_users()
list_of_admins = [198556652, 10719684]


class Game:
    list_of_game = [['тренировка', '03.04.2024', '30.03.2024 18:00', [198556652], [], [], []]]

    def set_data(self, first_value, second_value, last_value):
        self.list_of_game.append([first_value, second_value, last_value, [], [], [], []])
        print(self.list_of_game)

    def get_names(self):
        if self.list_of_game == []:
            return 'опросов нет'
        else:
            list_of_games_name = []
            for element in self.list_of_game:
                list_of_games_name.append(element[0] + ' ' + element[1])
            return list_of_games_name






game_name_value = ''
game_time_value = ''
game_ask_time_value = ''
result = ''
game_bool = False
game = Game()


ask_state = ''
name_state = False
delete_state = False
view_game_bool = False


def send_msg(user_id, msg, keyboard=None):
    post = {
        'user_id': user_id,
        'message': msg,
        'random_id': get_random_id()
    }

    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post

    session.method('messages.send', post)


for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        text = event.text.lower()
        user_id = event.user_id
        keyboard = VkKeyboard(one_time=True)

        if text == 'start':
            if Sql.search_id_in_users(user_id):
                keyboard.add_button('опросы')
                keyboard.add_line()
                if name_state == False:
                    keyboard.add_button('указать свой позывной')
                # keyboard.add_button('в отпуске')
                # keyboard.add_button('в строю')
                send_msg(user_id, 'Укажите свой позывной, если еще не указывали', keyboard)
            else:
                keyboard.add_button('подписаться')
                send_msg(user_id, 'Вам нужно подписаться', keyboard)

        if text == 'подписаться':
            send_msg(user_id, Sql.insert_in_user(user_id))

        if text == 'указать свой позывной' and Sql.search_id_in_users(user_id):
            send_msg(user_id, 'Напишите свой позывной с маленькой буквы')
            name_state = True

        if name_state == True and text != 'указать свой позывной' and text != ' ':
            Sql.insert_in_user_name(user_id, text)
            name_state = False
            send_msg(user_id, 'Ваш позывной сохранен')

        # if text == 'в отпуске' and Sql.search_id_in_users(user_id):
        #     if list_of_users_in_service.count(user_id):
        #         list_of_users_in_service.remove(user_id)
        #     list_of_users_in_vacation.append(user_id)
        #     send_msg(user_id, 'Статус сохранен')
        #
        # if text == 'в строю' and Sql.search_id_in_users(user_id):
        #     if list_of_users_in_vacation.count(user_id):
        #         list_of_users_in_vacation.remove(user_id)
        #     list_of_users_in_service.append(user_id)
        #     send_msg(user_id, 'Статус сохранен')

        if text == 'опросы' and Sql.search_id_in_users(user_id):
            if game.list_of_game == []:
                send_msg(user_id, 'Опросов нет')
            else:
                keyboard.add_button('посмотреть мои ответы в опросах')
                keyboard.add_line()
                numb = 1
                for element in game.get_names():
                    if numb < 2:
                        numb = numb + 1
                    else:
                        numb = 1
                        keyboard.add_line()
                    keyboard.add_button(element)
                send_msg(user_id, 'Выберете нужный Вам опрос', keyboard)

        if text == 'посмотреть мои ответы в опросах' and Sql.search_id_in_users(user_id):
            if game.list_of_game == []:
                send_msg(user_id, 'Опросов нет')
            else:
                for element in game.list_of_game:
                    if element[3].count(user_id):
                        send_msg(user_id, element[0] + ' ' + element[1] + ' - еду')
                    elif element[4].count(user_id):
                        send_msg(user_id, element[0] + ' ' + element[1] + ' - еду - водитель')
                    elif element[5].count(user_id):
                        send_msg(user_id, element[0] + ' ' + element[1] + ' - не еду')
                    elif element[6].count(user_id):
                        send_msg(user_id, element[0] + ' ' + element[1] + ' - думаю')
                    else:
                        send_msg(user_id, element[0] + ' ' + element[1] + ' - вы не проголосовали')

        if game.get_names().count(text) and Sql.search_id_in_users(user_id) and delete_state == False and view_game_bool == False:
            ask_state = text
            time_value = ''
            for element in game.list_of_game:
                if element[0] + ' ' + element[1] == ask_state:
                    time_value = element[2]
            keyboard.add_button('еду')
            keyboard.add_line()
            keyboard.add_button('еду - водитель')
            keyboard.add_line()
            keyboard.add_button('не еду')
            keyboard.add_line()
            keyboard.add_button('думаю')
            send_msg(user_id, 'Вы перешли в опрос игры"' + ask_state + '". Думать можно до ' + time_value, keyboard)
            time_value = ''

        if text == 'еду' and ask_state != '' and Sql.search_id_in_users(user_id):
            for element in game.list_of_game:
                if element[0] + ' ' + element[1] == ask_state:
                    element[3].append(user_id)
                    if element[4].count(user_id):
                        element[4].remove(user_id)
                    if element[5].count(user_id):
                        element[5].remove(user_id)
                    if element[6].count(user_id):
                        element[6].remove(user_id)
            send_msg(user_id, 'Выбран вариант "еду"')
            print(game.list_of_game)

        if text == 'еду - водитель' and ask_state != '' and Sql.search_id_in_users(user_id):
            for element in game.list_of_game:
                if element[0] + ' ' + element[1] == ask_state:
                    element[4].append(user_id)
                    if element[3].count(user_id):
                        element[3].remove(user_id)
                    if element[5].count(user_id):
                        element[5].remove(user_id)
                    if element[6].count(user_id):
                        element[6].remove(user_id)
            send_msg(user_id, 'Выбран вариант "еду - водитель"')
            print(game.list_of_game)

        if text == 'не еду' and ask_state != '' and Sql.search_id_in_users(user_id):
            for element in game.list_of_game:
                if element[0] + ' ' + element[1] == ask_state:
                    element[5].append(user_id)
                    if element[3].count(user_id):
                        element[3].remove(user_id)
                    if element[4].count(user_id):
                        element[4].remove(user_id)
                    if element[6].count(user_id):
                        element[6].remove(user_id)
            send_msg(user_id, 'Выбран вариант "не еду"')
            print(game.list_of_game)

        if text == 'думаю' and ask_state != '' and Sql.search_id_in_users(user_id):
            for element in game.list_of_game:
                if element[0] + ' ' + element[1] == ask_state:
                    element[6].append(user_id)
                    if element[3].count(user_id):
                        element[3].remove(user_id)
                    if element[4].count(user_id):
                        element[4].remove(user_id)
                    if element[5].count(user_id):
                        element[5].remove(user_id)
            send_msg(user_id, 'Выбран вариант "думаю"')
            print(game.list_of_game)

        if text == 'админ панель' and list_of_admins.count(user_id):
            keyboard.add_button('создать опрос')
            keyboard.add_line()
            keyboard.add_button('посмотреть результаты опроса')
            keyboard.add_line()
            keyboard.add_button('удалить опрос')
            send_msg(user_id, 'Вы в админ панеле', keyboard)

        if text == 'создать опрос' and list_of_admins.count(user_id):
            send_msg(user_id, 'Введите название игры, дату проведения игры, дату и время "думаю до", разделяя знаком ";" (пример: Тренировка ; 03.04.2024 ; 30.03.2024 18:00)')
            game_bool = True

        if game_bool == True and list_of_admins.count(user_id) and text != 'да' and text != 'нет' and text != 'создать опрос':
            result = text.split(' ; ')
            game_name_value = result[0]
            game_time_value = result[1]
            game_ask_time_value = result[2]
            keyboard.add_button('да')
            keyboard.add_button('нет')
            send_msg(user_id, 'Название игры: ' + game_name_value + '. Дата игры: ' + game_time_value + '. Дата пункта "думаю до": ' + game_ask_time_value + '. Все верно?', keyboard)

        if game_bool == True and list_of_admins.count(user_id) and text == 'да' and text != 'нет':
            game.set_data(result[0], result[1], result[2])
            game_name_value = ''
            game_time_value = ''
            game_ask_time_value = ''
            game_bool = False
            send_msg(user_id, 'Игра сохранена. Начинаю рассылку уведомлений')
            for user in list_of_auth_users:
                send_msg(user, 'Создан новый опрос')

        if game_bool == True and list_of_admins.count(user_id) and text != 'да' and text == 'нет':
            game_name_value = ''
            game_time_value = ''
            game_ask_time_value = ''
            game_bool = False
            send_msg(user_id, 'Создайте опрос еще раз')

        if text == 'удалить опрос' and list_of_admins.count(user_id):
            if game.list_of_game == []:
                send_msg(user_id, 'Опросов нет')
            else:
                numb = 1
                for element in game.get_names():
                    if numb < 2:
                        numb = numb + 1
                    else:
                        numb = 1
                        keyboard.add_line()
                    keyboard.add_button(element)
                send_msg(user_id, 'выберете опрос, который хотите удалить', keyboard)
                delete_state = True

        if game.get_names().count(text) and delete_state == True and list_of_admins.count(user_id) and text != 'выберете опрос, который хотите удалить':
            for element in game.list_of_game:
                if element[0] + ' ' + element[1] == text:
                    game.list_of_game.remove(element)
            send_msg(user_id, 'Опрос удален')
            delete_state = False
            print(game.list_of_game)

        if text == 'посмотреть результаты опроса' and list_of_admins.count(user_id):
            if game.list_of_game == []:
                send_msg(user_id, 'Опросов нет')
            else:
                numb = 1
                for element in game.get_names():
                    if numb < 2:
                        numb = numb + 1
                    else:
                        numb = 1
                        keyboard.add_line()
                    keyboard.add_button(element)
                send_msg(user_id, 'выберете опрос, результаты которого хотите посмотреть', keyboard)
                view_game_bool = True

        if game.get_names().count(text) and view_game_bool == True and list_of_admins.count(user_id) and text != 'выберете опрос, результаты которого хотите посмотреть':
            for element in game.list_of_game:
                if element[0] + ' ' + element[1] == text:
                    time_array = []
                    send_msg(user_id, 'Едут:')
                    for el in element[3]:
                        send_msg(user_id, Sql.search_id_in_users_name(el))
                        time_array.append(el)
                    send_msg(user_id, 'Едут - водители:')
                    for el in element[4]:
                        send_msg(user_id, Sql.search_id_in_users_name(el))
                        time_array.append(el)
                    send_msg(user_id, 'Не едут:')
                    for el in element[5]:
                        send_msg(user_id, Sql.search_id_in_users_name(el))
                        time_array.append(el)
                    send_msg(user_id, 'Думают:')
                    for el in element[6]:
                        send_msg(user_id, Sql.search_id_in_users_name(el))
                        time_array.append(el)
                    for el in list_of_auth_users:
                        if time_array.count(el[0]) == 0:
                            send_msg(user_id, Sql.search_id_in_users_name(el[0]) + ' - Не проголосовал')
            send_msg(user_id, 'конец списка')
            view_game_bool = False


        # send_msg(user_id, ';'.join(map(str, list_of_users)))