# coding=utf-8


class CycloneCsvFileWriter:
    def __init__(self):
        pass

    def write(self, data, workingDir, fileNamePrefix, fileNameSuffix):

        # Нужен итератор, чтобы вызывать next() напрямую, без цикла for
        rows = iter(data)
        row = self.__next(rows)

        # Такой двойной цикл сделан для того, чтобы не нужно было заново открывать файлы для каждой строки в выборке
        # Файлы открываются только один раз для каждой даты, если набор отсортирован по дате, а у нас он отсортирован
        while row:
            date = row[1]
            fileName = workingDir + fileNamePrefix + str(date) + fileNameSuffix
            with open(fileName, 'w+') as f:
                while row:
                    if date != row[1]:
                        break
                    line = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + '\n'
                    f.write(line)
                    row = self.__next(rows)

    def __next(self, iterator):
        try:
            return next(iterator)
        except StopIteration as cause:
            return None
