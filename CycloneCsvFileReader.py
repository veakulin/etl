# coding=utf-8


# Загружает список кортежей (id, date, status) из csv-файла
class CycloneCsvFileReader:
    def __init__(self):
        pass

    def read(self, file):
        for line in file.readlines():
            parts = line.rstrip().split(',')  # Уберем завершающие переносы строк. Правда rstrip еще и пробелы удаляет!
            yield parts[0], parts[1], parts[2]
