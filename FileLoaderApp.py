# coding=utf-8

import psycopg2
from AbstractETLApp import AbstractETLApp
from CycloneCsvFileReader import CycloneCsvFileReader
from CycloneHistoryDbWriter import CycloneHistoryDbWriter


class FileLoaderApp(AbstractETLApp):
    def __init__(self):
        super(FileLoaderApp, self).__init__()

    def run(self):
        with self._getDbConnection() as conn:
            conn.autocommit = False
            conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

            try:
                csvReader = CycloneCsvFileReader()
                historyWriter = CycloneHistoryDbWriter(conn)
                with open(self._config.file) as csv:
                    data = csvReader.read(csv)
                    for record in data:
                        historyWriter.write(record)
                conn.commit()
            except Exception as cause:
                conn.rollback()
                print cause.message, '\n'

    def _addExtraArgs(self, parser):
        parser.add_argument('--file', required=True)


app = FileLoaderApp()
app.run()
