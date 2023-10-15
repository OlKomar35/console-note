import json
import os
from datetime import datetime


def help_print_cmd():
    print()
    print('Добавление новой заметки')
    print('add --title <Заголовок новой завметки> --msg <Тело новой заметки>')
    print()
    print('Сохранить заметку')
    print('save')
    print()
    print('Показать список всех заметок')
    print('list')
    print()
    print('Показать список заметок, созданных/отредактированных в определенную дату')
    print('list --date <Дата>')
    print()
    print('Прочитать заметку из файла')
    print('read --id <Номер>')
    print()
    print('Удалить заметку по ее номеру')
    print('remove --id <Номер>')
    print()
    print('Редактировать заметку')
    print('edit --id <Номер> --title <Заголовок новой завметки> --msg <Тело новой заметки>')
    print('или')
    print('edit --id <Номер> --title <Заголовок новой завметки>')
    print('или')
    print('edit --id <Номер> --msg <Тело новой заметки>')
    print()
    print('Выход из приложения')
    print('exit')


list_data = list()
id_ = 0
current_dir = os.getcwd()  # текущая папка
for filename in os.listdir(current_dir):
    if filename.startswith('note_') and filename.endswith('.json'):
        file_path = os.path.join(current_dir, filename)
        if os.path.isfile(file_path):  # полный путь к файлу

            # Чтение содержимого JSON-файла в строку
            with open(filename) as json_file:
                json_str = json_file.read()

            # Распарсить JSON-строку в объект Python
            data = json.loads(json_str)

            # Нахождение Id
            result = filename.split("_")
            if int(result[-1].split(".")[0]) > id_:
                id_ = int(result[-1].split(".")[0])
            list_data.append(data)

flag = True
list_id = list()
data = {}
json_string = ''

while flag:
    print()
    str_command = input('Введите нужную команду или help ')
    list_cmd = str_command.split('--')

    if list_cmd[0].replace(' ', '').lower() == 'help':
        help_print_cmd()

    elif list_cmd[0].replace(' ', '').lower() == 'add':
        if list_cmd[1].split(' ', 1)[0] == 'title' and list_cmd[2].split(' ', 1)[0] == 'msg':
            id_ += 1
            title = list_cmd[1].split(' ', 1)[1]
            msg = list_cmd[2].split(' ', 1)[1]
            date_time_now = datetime.now()
            dt_string = date_time_now.strftime("%d/%m/%Y %H:%M:%S")

            data = {
                "id": id_,
                "title": title,
                "msg": msg,
                "date": dt_string
            }
        else:
            print('Не верная команда')

    elif list_cmd[0].replace(' ', '').lower() == 'save':
        if data and id_ != 0:
            list_data.append(data)
            file_name = f"note_{id_}.json"
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        else:
            print('Нет данных для сохранения')

    elif list_cmd[0].replace(' ', '').lower() == 'list':
        size_ = len(list_cmd)

        if size_ == 1:
            if list_data:
                sorted_list = sorted(list_data, key=lambda x: x['date'])
                for item in sorted_list:
                    print(f"id:{item['id']} - {item['title']} - {item['msg']} - {item['date']} ")
                    print()
            else:
                print('Заметок нет')
        elif size_ == 2:
            date_selected = list_cmd[1].split(' ', 1)[1]
            flag_list = False
            for item in list_data:
                if item['date'].split(' ')[0] == date_selected:
                    print(f"id:{item['id']} - {item['title']} - {item['msg']} - {item['date']} ")
                    print()
                    flag_list = True
            if not flag_list:
                print('Нет заметок созданных в данную дату')
        else:
            print('Не верная команда')

    elif list_cmd[0].replace(' ', '').lower() == 'remove':
        id_remove = list_cmd[1].split(' ', 1)[1]
        file_path = f"note_{id_remove}.json"
        flag_remove = False
        for item in list_data:
            if int(item['id']) == int(id_remove):
                list_data.remove(item)
                flag_remove = True
        if flag_remove:
            try:
                os.remove(file_path)
                print(f"Заметка {id_remove} успешно удалена.")
            except OSError as e:
                print(f"Ошибка удаления файла {file_path}: {str(e)}")
        else:
            print('Заметки с таким id не существует')

    elif list_cmd[0].replace(' ', '').lower() == 'read':
        id_read = list_cmd[1].split(' ', 1)[1]
        flag_read = False
        for item in list_data:
            if int(item['id']) == int(id_read):
                print(f"id:{item['id']} - {item['title']} - {item['msg']} - {item['date']} ")
                flag_read = True
        if not flag_read:
            print('Нет заметки с таким id')

    elif list_cmd[0].replace(' ', '').lower() == 'edit':

        id_edit = list_cmd[1].split(' ', 1)[1].replace(' ', '')
        size_ = len(list_cmd)
        flag_edit = False
        index = 0
        for item in list_data:
            if int(item['id']) == int(id_edit):
                index = list_data.index(item)
                flag_edit = True

        if flag_edit:
            if size_ == 4:
                data = {
                    "id": id_edit,
                    "title": list_cmd[2].split(' ', 1)[1],
                    "msg": list_cmd[3].split(' ', 1)[1],
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }

                list_data[index] = data
                file_name = f"note_{id_edit}.json"
                with open(file_name, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)

            elif size_ == 3:

                if list_cmd[2].split(' ', 1)[0] == 'title':
                    data = {
                        "id": id_edit,
                        "title": list_cmd[2].split(' ', 1)[1],
                        "msg": list_data[index]['msg'],
                        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    }
                    list_data[index] = data
                    file_name = f"note_{id_edit}.json"
                    with open(file_name, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4)

                elif list_cmd[2].split(' ', 1)[0] == 'msg':

                    data = {
                        "id": id_edit,
                        "title": list_data[index]['title'],
                        "msg": list_cmd[2].split(' ', 1)[1],
                        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    }
                    list_data[index] = data
                    file_name = f"note_{id_edit}.json"
                    with open(file_name, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4)
                else:
                    print('Введена не верная команда')
            else:
                print('Не верная команда')
        else:
            print('Нет такого id')

    elif list_cmd[0].replace(' ', '').lower() == 'exit':
        flag = False

    else:
        print('Введина не верная команда')
