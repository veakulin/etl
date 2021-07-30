# coding=utf-8

import os

import psycopg2.extensions

from AbstractETLApp import AbstractETLApp
from CycloneCsvFileReader import CycloneCsvFileReader
from CycloneHistoryDbWriter import CycloneHistoryDbWriter


class DirLoaderApp(AbstractETLApp):
    def __init__(self):
        super(DirLoaderApp, self).__init__()

    def run(self):
        with self._getDbConnection() as conn:
            conn.autocommit = False
            conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

            try:
                csvReader = CycloneCsvFileReader()
                historyWriter = CycloneHistoryDbWriter(conn)

                for fileName in os.listdir(self._config.dir):
                    with open(self._config.dir + fileName) as csv:
                        cycloneStatusList = csvReader.read(csv)
                        for cycloneStatus in cycloneStatusList:
                            historyWriter.write(cycloneStatus)
                conn.commit()
            except Exception as cause:
                conn.rollback()

    def _addExtraArgs(self, parser):
        parser.add_argument('--dir', default=os.getcwd(), type=self._dirArg)


app = DirLoaderApp()
app.run()
