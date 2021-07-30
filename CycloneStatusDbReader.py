# coding=utf-8

import calendar


class CycloneStatusDbReader:
    def __init__(self, dbConnection):
        self.__dbConnection = dbConnection
        self.__table = "cyclone"
        self.__prepareServer()

    def readByMonth(self, yearNumber, monthNumber):
        lastMonthDay = calendar.monthrange(yearNumber, monthNumber)[1]
        fromDate = int(str(yearNumber) + '%02d' % monthNumber + '01')  # Первое число месяца
        toDate = int(str(yearNumber) + '%02d' % monthNumber + str(lastMonthDay))  # Последнее число месяца

        with self.__dbConnection.cursor() as cursor:
            cursor.execute('execute getStatus (%s, %s)', (fromDate, toDate))
            # Т.к. данных немного, то выдаем сразу всю выборку. Получится список кортежей (id, date, status)
            return cursor.fetchall()

    def __prepareServer(self):
        sql = 'prepare getStatus as ' \
              'with lastMeasure as (' \
                  'select id, date, max(time) as time ' \
                  'from {0} ' \
                  'group by id, date) ' \
              'select x.id, x.date, y.status from lastMeasure as x ' \
              'left join {0} as y ' \
              'on y.id = x.id and y.date = x.date and y.time = x.time ' \
              'where x.date between $1 and $2 ' \
              'order by x.date' \
              .format(self.__table)

        with self.__dbConnection.cursor() as cursor:
            cursor.execute(sql)

