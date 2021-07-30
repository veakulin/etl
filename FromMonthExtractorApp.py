# coding=utf-8

import datetime
from AbstractExtractorApp import AbstractExtractorApp
from CycloneStatusDbReader import CycloneStatusDbReader
from CycloneCsvFileWriter import CycloneCsvFileWriter


# Выгружает данные с какого-то месяца и до текущей даты
# Наверное стоит дополнительно проверять до какой даты вообще есть данные в базе
class FromMonthExtractorApp(AbstractExtractorApp):
    def __init__(self):
        super(FromMonthExtractorApp, self).__init__()

    def run(self):

        today = datetime.date.today()
        year = self._config.year
        month = self._config.month

        with self._getDbConnection() as conn:
            reader = CycloneStatusDbReader(conn)
            writer = CycloneCsvFileWriter()

            while year < today.year or (year == today.year and month <= today.month):
                data = reader.readByMonth(year, month)
                writer.write(data, self._config.dir, 'cyclones_', '.csv')
                month += 1
                if month > 12:
                    month = 1
                    year += 1

            conn.commit()


app = FromMonthExtractorApp()
app.run()
