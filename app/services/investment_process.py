from datetime import datetime

from app.constants.constants import Constant


def close_object(object_):
    """Закроет переданный объект."""
    object_.fully_invested = Constant.True_
    object_.close_date = datetime.now()


def investment_process(new_object, objects_update):
    """Принимает новый объект и список объектов для обновления, и возвращает
    список обновленных объектов."""
    results = []
    for object_ in objects_update:
        delta_new_object = new_object.full_amount - new_object.invested_amount
        delta_object = object_.full_amount - object_.invested_amount
        min_delta = min(delta_new_object, delta_object)
        object_.invested_amount += min_delta
        new_object.invested_amount += min_delta
        if delta_new_object >= delta_object:
            results.append(object_)
        if delta_new_object <= delta_object:
            results.append(new_object)
            break
    for result in results:
        close_object(result)
    return results
