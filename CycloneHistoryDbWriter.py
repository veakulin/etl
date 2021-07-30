# coding=utf-8

class CycloneHistoryDbWriter:
    def __init__(self, dbConnection):
        self.__dbConnection = dbConnection
        self.__table = "cyclone_history"
        self.__prepareServer()

    def write(self, data):  # В data находится кортеж (id, date, status)
        with self.__dbConnection.cursor() as cursor:
            cursor.execute('execute checkState (%s, %s, %s)', (data[0], data[1], data[2]))
            result = cursor.fetchall()[0][0]
            if result == 0:
                cursor.execute('execute newPeriod (%s, %s, %s)', (data[0], data[1], data[2]))
            elif result == 1 or result == 3:  # Две немного разных ситуации, но решаются одинаково. См. запрос checkState.
                cursor.execute('execute closePeriod (%s, %s)', (data[0], data[1]))
                cursor.execute('execute newPeriod (%s, %s, %s)', (data[0], data[1], data[2]))
            elif result == 2:
                cursor.execute('execute updatePeriod (%s, %s)', (data[0], data[1]))
            elif result == 4:
                cursor.execute('execute deletePeriod (%s, %s)', (data[0], data[1]))
                cursor.execute('execute closePeriod (%s, %s)', (data[0], data[1]))
                cursor.execute('execute updatePeriod (%s, %s)', (data[0], data[1]))
            else:
                print 'Что-то помешало сделать запись ', data, '\n'

    #
    def __prepareServer(self):
        with self.__dbConnection.cursor() as cursor:

            sql = 'prepare checkState as ' \
                  'with lastPeriod as (' \
                      'select date_from, date_to, status from {0} where id = $1 order by date_to desc fetch first 1 row only) ' \
                  'select case when (not exists(select 1 from lastPeriod)) then 0 /* ещё нет ни одной записи по циклону */' \
                              'when ((select date_to from lastPeriod) < $2) and ' \
                                   '((select status from lastPeriod) <> $3) then 1 /* есть запись за ближайший предыдущий день с другим статусом */ ' \
                              'when ((select date_to from lastPeriod) < $2) and ' \
                                   '((select status from lastPeriod) = $3) then 2 /* есть запись за ближайший предыдущий день с таким же статусом */ ' \
                              'when ((select date_to from lastPeriod) = $2) and ' \
                                   '((select date_from from lastPeriod) < (select date_to from lastPeriod)) and ' \
                                   '(select status from lastPeriod) <> $3 then 3 /* есть запись за сегодняшний день, но это хвост многодневного периода c другим статусом */ ' \
                              'when ((select date_to from lastPeriod) = $2) and ' \
                                   '((select date_from from lastPeriod) = (select date_to from lastPeriod)) and ' \
                                   '(select status from lastPeriod) <> $3 then 4 /* есть запись только за сегодняшний день с другим статусом */ ' \
                              'else -1 /* что-то другое, скорее всего попытка перезаписать прошлое */ ' \
                              'end' \
                  .format(self.__table)
            cursor.execute(sql)

            sql = 'prepare newPeriod as ' \
                  'insert into {0} (id, date_from, date_to, status) values ($1, $2, $2, $3)' \
                  .format(self.__table)
            cursor.execute(sql)

            sql = 'prepare closePeriod as ' \
                  'with tomorrow as (' \
                      'select (extract(year from $2::text::date - 1)::text || ' \
                             'lpad(extract(month from $2::text::date - 1)::text, 2, \'0\') || ' \
                             'lpad(extract(day from $2::text::date - 1)::text, 2, \'0\'))::integer as value), ' \
                      'lastPeriod as (' \
                          'select date_to from {0} where id = $1 order by date_to desc fetch first 1 row only) ' \
                  'update {0} set date_to = (select value from tomorrow) where id = $1 and date_to = (select date_to from lastPeriod)' \
                  .format(self.__table)
            cursor.execute(sql)

            sql = 'prepare updatePeriod as ' \
                  'with lastPeriod as (' \
                      'select date_to from {0} where id = $1 order by date_to desc fetch first 1 row only) ' \
                  'update {0} set date_to = $2 where id = $1 and date_to = (select date_to from lastPeriod)' \
                  .format(self.__table)
            cursor.execute(sql)

            sql = 'prepare deletePeriod as ' \
                  'delete from {0} where id = $1 and date_from = $2 and date_to = $2' \
                  .format(self.__table)
            cursor.execute(sql)

