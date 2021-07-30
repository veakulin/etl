# coding=utf-8

from AbstractExtractorApp import AbstractExtractorApp
from CycloneStatusDbReader import CycloneStatusDbReader
from CycloneCsvFileWriter import CycloneCsvFileWriter


# Выгружает данные за один месяц
class OneMonthExtractorApp(AbstractExtractorApp):
    def __init__(self):
        super(OneMonthExtractorApp, self).__init__()

    def run(self):
        with self._getDbConnection() as conn:
            reader = CycloneStatusDbReader(conn)
            data = reader.readByMonth(self._config.year, self._config.month)
            writer = CycloneCsvFileWriter()
            writer.write(data, self._config.dir, 'cyclones_', '.csv')
            conn.commit()


app = OneMonthExtractorApp()
app.run()
