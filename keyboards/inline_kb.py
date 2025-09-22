from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да, готов!", callback_data="ready_yes")],
    [InlineKeyboardButton(text="Конечно готов!", callback_data="ready_yes")]
])

# Клавиатура для начала викторины
start_quiz_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать", callback_data="start_quiz")]
])

# Клавиатуры для вопросов
def create_question_kb(question_num: int):
    if question_num == 1:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) Нерпавильно", callback_data="q1_1")],
            [InlineKeyboardButton(text="2) Неправильно", callback_data="q1_2")],
            [InlineKeyboardButton(text="3) Я не хочу отвечать", callback_data="q1_3")],
            [InlineKeyboardButton(text="4) Кастрюля", callback_data="q1_4")]
        ])
    elif question_num == 2:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) 107,8682", callback_data="q2_1")],
            [InlineKeyboardButton(text="2) 102,8689", callback_data="q2_2")],
            [InlineKeyboardButton(text="3) САМ ДУРАК", callback_data="q2_3")],
            [InlineKeyboardButton(text="4) 10,9672", callback_data="q2_4")]
        ])
    elif question_num == 3:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) Бежать", callback_data="q3_1")],
            [InlineKeyboardButton(text="2) Переходить дорогу", callback_data="q3_2")],
            [InlineKeyboardButton(text="3) Заказать капельницу", callback_data="q3_3")],
            [InlineKeyboardButton(text="4) Звонить в полицию", callback_data="q3_4")]
        ])
    elif question_num == 4:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) не вижу белого желтка", callback_data="q4_1")],
            [InlineKeyboardButton(text="2) а можно мне другого ботодела?", callback_data="q4_2")],
            [InlineKeyboardButton(text="3) не вижу белый желток", callback_data="q4_3")],
            [InlineKeyboardButton(text="4) желток обычно жёлтый", callback_data="q4_4")]
        ])
    elif question_num == 5:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) 8,92 килограмма", callback_data="q5_1")],
            [InlineKeyboardButton(text="2) 3 локтя", callback_data="q5_2")],
            [InlineKeyboardButton(text="3) 26,24 литра", callback_data="q5_3")],
            [InlineKeyboardButton(text="4) 117 вольт", callback_data="q5_4")]
        ])
    elif question_num == 6:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) Данил", callback_data="q6_1")],
            [InlineKeyboardButton(text="2) Даниил", callback_data="q6_2")],
            [InlineKeyboardButton(text="3) Даня", callback_data="q6_3")],
            [InlineKeyboardButton(text="4) Кому не пофиг, всё подходит", callback_data="q6_4")]
        ])
    elif question_num == 7:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) цифра 9", callback_data="q7_1")],
            [InlineKeyboardButton(text="2) цифра 8", callback_data="q7_2")],
            [InlineKeyboardButton(text="3) цифра 3", callback_data="q7_3")],
            [InlineKeyboardButton(text="4) нет правильного ответа", callback_data="q7_4")]
        ])
    elif question_num == 8:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) В дурке", callback_data="q8_1")],
            [InlineKeyboardButton(text="2) На вписке", callback_data="q8_2")],
            [InlineKeyboardButton(text="3) На карусели", callback_data="q8_3")],
            [InlineKeyboardButton(text="4) Чего блин???", callback_data="q8_4")]
        ])
    elif question_num == 9:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) Андреевич", callback_data="q9_1")],
            [InlineKeyboardButton(text="2) Сергеевич", callback_data="q9_2")],
            [InlineKeyboardButton(text="3) Александрович", callback_data="q9_3")],
            [InlineKeyboardButton(text="4) Натальевич", callback_data="q9_4")]
        ])
    elif question_num == 10:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1) Февраль", callback_data="q10_1")],
            [InlineKeyboardButton(text="2) Ноябрь", callback_data="q10_2")],
            [InlineKeyboardButton(text="3) Во всех", callback_data="q10_3")],
            [InlineKeyboardButton(text="4) ИДИ НАХ...Й!!!", callback_data="q10_4")]
        ])