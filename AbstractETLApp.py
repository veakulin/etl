# coding=utf-8

import argparse
import os
import psycopg2
from abc import ABCMeta, abstractmethod


# Базовый класс для приложений, работающих с базой данных
class AbstractETLApp(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        # Надо бы проверять корректность параметров командной строки,
        # Но т.к. задание тестовое, то оставлю этот момент на совести пользователя
        parser = argparse.ArgumentParser();
        self.__addCommonArgs(parser)
        self._addExtraArgs(parser)
        config = parser.parse_args()
        self._config = config

    def _getDbConnection(self):
        connStr = 'host={0} port={1} dbname={2} user={3} password={4}'\
            .format(self._config.host, self._config.port, self._config.database, self._config.user, self._config.password)
        return psycopg2.connect(connStr)

    # Наследнику может захотеться определить дополнительные параметры командной строки
    @abstractmethod
    def _addExtraArgs(self, parser):
        pass

    # Это для наследников, которые будут принимать из командной строки имена каталогов
    # Добавляет \ в конец имени каталога
    def _dirArg(self, arg):
        result = os.path.normpath(str(arg))
        return result if result.endswith(os.path.sep) else result+os.path.sep

    # Это нужно для любого кода работающего сетевым сервером БД
    def __addCommonArgs(self, parser):
        parser.add_argument('--host',     default='localhost')
        parser.add_argument('--port',     default='5432')
        parser.add_argument('--database', required=True)
        parser.add_argument('--user',     required=True)
        parser.add_argument('--password', required=True)

