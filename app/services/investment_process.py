from datetime import datetime

from app.constants.constants import Constant


def investment_process(new_object, objects_update):
    """Принимает новый объект и список объектов для обновления.<br>
    Проводит процесс инвестирования:
    - увеличение `invested_amount` как в новом объекте, так и в объектах
    переданного списка, установка значений `fully_invested` и `close_date`,
    при необходимости.
    """
    for object_ in objects_update:
        delta_new_object = new_object.full_amount - new_object.invested_amount
        delta_object = object_.full_amount - object_.invested_amount
        min_delta = min(delta_new_object, delta_object)
        object_.invested_amount += min_delta
        new_object.invested_amount += min_delta
        if delta_new_object >= delta_object:
            object_.fully_invested = Constant.True_
            object_.close_date = datetime.now()
        if delta_new_object <= delta_object:
            new_object.fully_invested = Constant.True_
            new_object.close_date = datetime.now()
            break
