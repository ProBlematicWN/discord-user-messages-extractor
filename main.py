import re

def extract_user_messages(input_file, output_file, username):
    # алгоритм для поиска сообщений пользователя
    message_pattern = re.compile(
        rf"^\[.*?\] {re.escape(username)}\n((?:[^[\n]*\n?)*)", re.MULTILINE
    )

    try:
        # чтение исходного файла
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = infile.read()

        # поиск всех сообщений указанного пользователя
        matches = message_pattern.findall(data)

        # сохранение сообщений в новый файл
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for message in matches:
                outfile.write(message.strip() + '\n\n')
                print(rf'Сохранено сообщение: {message}')

        # удаление пустых строк, ссылок, строк с атрибутами и сообщений, начинающихся с ':'
        with open(output_file, 'r', encoding='utf-8') as outfile:
            lines = outfile.readlines()

        with open(output_file, 'w', encoding='utf-8') as outfile:
            skip_next = False
            for i, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue

                if re.search(r"{Reactions}", line):
                    skip_next = True  # скип строки
                    continue

                if line.strip() and not re.search(r"^:|http[s]?://|{Attachments}", line):
                    outfile.write(line)

        print(f"Сообщения пользователя '{username}' успешно сохранены в '{output_file}'")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# путь к файлу, файлу выхода, пидораса
input_file = 'chat.txt'  # исходный файл с чатом
username = input('Введите имя пользователя')  # имя пользователя для поиска
output_file = username+'.txt'  # файл для сохранения сообщений

extract_user_messages(input_file, output_file, username)