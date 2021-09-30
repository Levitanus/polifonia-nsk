import typing as ty
import requests
import json

from enum import Enum

JsonDict = ty.Dict[str, ty.Union[str, int, ty.List[str], None]]

API_KEY = "b0MLIiMLwsA41aSnquHNUnXoCujKUjpH16B08UvTqOG8o7KQfU"

events = {
    "user_new":
        "Ученик создан",
    "user_changed":
        "Информация об ученике изменилась",
    "user_changed_state":
        "Статус ученика изменился",
    "user_birthday":
        "Ученик отмечает день рождения",
    "join_new":
        "Создана запись в группу",
    "join_changed":
        "Информация о записи в группу изменилась",
    "join_changed_state":
        "Статус записи в группу изменился",
    "class_new":
        "Группа создана",
    "class_changed":
        "Информация о группе изменилась",
    "class_start_days":
        "Старт группы менее чем через 7 дней (отправляется раз в сутки)",
    "class_start_hours":
        "Старт группы менее чем через 6 часов (отправляется раз в час)",
    "lesson_changed":
        "Информация о занятии изменилась",
    "lesson_start_days":
        "Занятие начинается менее чем через 7 дней",
    "lesson_start_hours":
        "Занятие начинается через 6 часов (отправляется раз в час)",
    "payment_new":
        "Принят платеж",
    "sub_new":
        "Создание нового абонемента",
    "debit_new":
        "Новое списание у ученика",
    "sub_lesson_in_debt":
        "Занятие для записи проведено “в долг”",
    "lesson_record_new":
        "Создана запись на занятие",
    "lesson_record_changed":
        "Информация о записи на занятие изменилась",
    "lesson_record_deleted":
        "Запись на занятие удалена",
    "sub_days_next_payment":
        "Осталось менее 5 дней до внесения очередного платежа по абонементу",
    "sub_lessons_left":
        "В абонементе осталось менее 5 посещений",
    "sub_end_days":
        "Абонемент заканчивается менее чем через 5 дней",
    "user_consecutive_visit_missed_2":
        "Ученик имеет два пропуска подряд без уважительной причины",
    "lesson_mark_set":
        "Проставлена оценка",
    "lesson_mark_deleted":
        "Оценка удалена",
    "lesson_task_new":
        "Задание создано",
    "lesson_task_changed":
        "Задание изменено",
    "task_new":
        "Задача создана",
    "task_changed":
        "Задача изменена",
    "task_deleted":
        "Задача удалена",
    "lesson_new":
        "новое занятие"
}

server = 'https://api.moyklass.com'


def get_token() -> str:
    resp = requests.post(
        f'{server}/v1/company/auth/getToken',
        headers={"Content-type": "application/json"},
        json={"apiKey": "b0MLIiMLwsA41aSnquHNUnXoCujKUjpH16B08UvTqOG8o7KQfU"},
        # verify=False,
        # },
        # params={"grant_type": "client_credentials"}
    )
    # print(resp)
    # print(resp.text)
    if resp.status_code == 200:
        data = resp.json()
        print(data)
        return data['accessToken']


def revoke_token(token: str) -> None:
    resp = requests.post(
        url=f'{server}/v1/company/auth/revokeToken',
        headers={"x-access-token": token},
        # verify=False,
    )
    # print(resp)


def get_filial_name(token: str, filialId: int) -> str:
    resp = requests.get(
        f"{server}/v1/company/filials",
        headers={"x-access-token": token},
        # verify=False,
    )
    if resp.status_code == 200:
        r = list(filter(lambda x: x["id"] == filialId, resp.json()))[0]["name"]
        return ty.cast(str, r)
    # else:
    #     raise requests.ConnectionError(resp, resp.text)


def get_room(token: str, roomId: int) -> str:
    resp = requests.get(
        f"{server}/v1/company/rooms",
        headers={"x-access-token": token},
        # verify=False,
    )
    if resp.status_code == 200:
        r = list(filter(lambda x: x["id"] == roomId, resp.json()))[0]["name"]
        return ty.cast(str, r)
    # else:
    #     raise requests.ConnectionError(resp, resp.text)


def get_class(token: str, classId: int) -> str:
    resp = requests.get(
        f"{server}/v1/company/classes",
        headers={"x-access-token": token},
        # verify=False,
    )
    if resp.status_code == 200:
        r = list(filter(lambda x: x["id"] == classId, resp.json()))[0]["name"]
        return ty.cast(str, r)
    # else:
    #     raise requests.ConnectionError(resp, resp.text)


def get_teachers(token: str, ids: ty.List[int]) -> ty.List[str]:
    resp = requests.get(
        f"{server}/v1/company/managers",
        headers={"x-access-token": token},
        # verify=False,
    )
    if resp.status_code == 200:
        teachers = []
        for teacher in resp.json():
            tid = teacher["id"]
            if list(filter(lambda x: tid == x, ids)):
                teachers.append(teacher['name'])
        r = teachers
        # print(r)
        return r
    # else:
    #     raise requests.ConnectionError(resp, resp.text)


def get_students(
    token: str, records: ty.Optional[ty.List[ty.Dict[str, ty.Union[int, str,
                                                                   bool]]]]
) -> ty.List[str]:
    if not records:
        return []
    students = []
    for record in records:
        resp = requests.get(
            f"{server}/v1/company/users/{record['userId']}",
            headers={"x-access-token": token},
            # verify=False,
        )
        if resp.status_code == 200:
            students.append(resp.json()["name"])
        # else:
        #     raise requests.ConnectionError(resp, resp.text)
    return students


def get_lesson_info(
    token: str, event_type: str, data: ty.Dict[str, ty.Union[str, int]]
) -> JsonDict:
    lesson_id = data["lessonId"]
    if event_type == "lesson_deleted":
        info = ty.cast(JsonDict, data['deletedLesson'])
        info['beginTime'] = info['begin_time']
        info['endTime'] = info['end_time']
        info['classId'] = info['class_id']
        info['records'] = None
        info['filial'] = None
    else:
        resp = requests.get(
            f"{server}/v1/company/lessons/{lesson_id}",
            headers={"x-access-token": token},
            # verify=False,
            params={"includeRecords": "true"}
        )
        # print(resp)
        info = resp.json()
        info['room'] = get_room(token, info['roomId'])
        # info['filial'] = get_filial_name(token, info['filialId'])
    # print(info)
    important = {
        "дата": info['date'],
        "начало": info['beginTime'],
        "конец": info['endTime'],
        "филиал": info['filial'],
        "аудитория": info['room'],
        "предмет": get_class(token, info['classId']),
        "преподаватели": get_teachers(token, info['teacherIds']),
        "ученики": get_students(token, info['records']),
    }
    # print(important)
    return important


def format_lesson(info: JsonDict, status: str = "Новое занятие") -> str:
    return f"""\
    {status}!
    ⋅ Предмет: "{info["предмет"]}" в <b>{info["аудитория"]}</b>
    ⋅ {info["дата"]} с {info["начало"]} до {info["конец"]}
    ⋅ преподаватели: <i>{info["преподаватели"]}</i>
    ⋅ ученики: <i>{info["ученики"]}</i>
    """


def allert_if_new_lesson(data: ty.Dict) -> ty.Optional[str]:
    status = {
        'lesson_new': "Новое занятие",
        'lesson_changed': "Изменения в занятии",
        'lesson_deleted': "Занятие отменено"
    }
    if data['event'] in ("lesson_new", "lesson_changed", "lesson_deleted"):
        token = get_token()
        try:
            info = get_lesson_info(token, data['event'], data["object"])
        except KeyError as e:
            revoke_token(token)
            # print("Cannot parse lesson: {}".format(e))
            return None
        revoke_token(token)
        return format_lesson(info, status[data['event']])
    else:
        return None


if __name__ == '__main__':
    token = get_token()
    get_lesson_info(token, "10479345")
    revoke_token(token)
