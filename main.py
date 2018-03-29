# Имя: GetTelegramChatMembers.py
# Автор: Klachkov (reserfodium) Valery

from telethon import TelegramClient, errors
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import getpass
import sys


# Вывод помощи
def usage():
    print(
        """
Использование: *.exe [-h][--help][filename]

-h, --help  Опции скрипта
[filename]  Создание файла со всеми участниками чата
        """)


# Парсинг аргументов командной строки
# Если надо парсить больше двух аргументов, то лучше использовать библиотеку optparse
def parse_args():
	# Если были переданы аргументы
    if len(sys.argv) > 1:
    	# Запрошен вывод помощи
        if sys.argv[1] in ["-h", "--help"]:
            usage()
            return None
        else:
            return sys.argv[1]
    else:
        return ""


def main():
    # --- ПРИВАТНЫЕ ДАННЫЕ --- #

    api_id = 259668
    api_hash = "0189067091f343f6e02bf514cf82921f"
    session_name = "session"
    chat_name = raw_input("Имя канала: ")  # Имя используемого чата

    # --- СТРОКИ --- #

    enter_phone_number = "Введите номер телефона: "
    enter_sms_code = "Введите SMS-код: "
    enter_password = "Введите пароль: "
    invalid_phone_number = "Неверный номер телефона. Проверьте введенные данные и повторите попытку"
    chat_users_string = "Пользователи чата"

    # --- ПОЛУЧЕНИЕ ИМЕНИ ФАЙЛА --- #

    parse_result = parse_args()

    # Использован флаг -h (--help)
    if parse_result is None:
        return 0
    else:
        filename = parse_result

    # --- ИНИЦИАЛИЗАЦИЯ СЕССИИ --- #

    client = TelegramClient(session_name, api_id, api_hash)

    # Инициализация сессии
    # Цикл продолжается до тех пор, пока пользователь не введет корректные данные
    while True:
        try:
            client.start(phone=lambda: input(enter_phone_number),
            			 password=lambda: getpass.getpass(enter_password),
            			 code_callback=lambda: input(enter_sms_code))
            break

        # Неверный формат номера
        except errors.rpc_error_list.PhoneNumberInvalidError:
            print(invalid_phone_number, end="\n\n")

    # --- ПОЛУЧЕНИЕ СПИСКА ПОЛЬЗОВАТЕЛЕЙ ЧАТА --- #

    offset = 0
    limit = 100
    all_users = []

    while True:
        # Получаем limit пользователей из общей массы со смещением offset
        users = client(GetParticipantsRequest(
            chat_name, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))

        # Получили всех пользователей
        if not users.users:
            break

        # Добавляем пользователей в общий массив all_users и увеличиваем смещение на длину массива извлеченных пользователей
        all_users.extend(users.users)
        offset += len(users.users)

    # --- ПОЛУЧЕНИЕ СПИСКА USERNAME'ОМ УЧАСТНИКОВ --- #

    # На выходе получаем сортированный массив юзернеймов, которые не равно None
    names = sorted([user.username for user in all_users if user.username is not None])

    # --- ВЫВОД --- #

    # Все пользователи в столбец
    printable_names = '\n'.join(str(p) for p in names)

    if filename == "":
    	# Вывод заголовка и имен
        print(chat_users_string + " @" + chat_name, end="\n\n")
        print(printable_names)
    else:
        # Запись в файл
        file = open(filename, "w")
        file.write(printable_names)
        file.close()

    # OK!
    return 0


# Точка входа
if __name__ == "__main__":
    main()  # sys.exit(main())
