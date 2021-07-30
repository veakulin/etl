# coding=utf-8

import datetime
import os
from abc import ABCMeta
from AbstractETLApp import AbstractETLApp


# Базовый класс для приложений извлекающих данные
class AbstractExtractorApp(AbstractETLApp):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(AbstractExtractorApp, self).__init__()

    # Для извлечения в любом случае нужно указать год, месяц и каталог
    # При этом приложения, выгружающие данные ЗА какой-то месяц и С какого-то месяца используют параметры по разному
    def _addExtraArgs(self, parser):
        today = datetime.date.today()
        parser.add_argument('--year',  default=today.year,  type=int)
        parser.add_argument('--month', default=today.month, type=int)
        parser.add_argument('--dir',   default=os.getcwd(), type=self._dirArg)
