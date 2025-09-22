import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramNetworkError

from database.database import check_user, add_user
from keyboards.inline_kb import start_kb, start_quiz_kb, create_question_kb

router = Router()

class QuizStates(StatesGroup):
    waiting_for_start = State()
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()

# Правильные ответы
correct_answers = {
    1: 'q1_2', 2: 'q2_1', 3: 'q3_2', 4: 'q4_4', 5: 'q5_3',
    6: 'q6_4', 7: 'q7_1', 8: 'q8_3', 9: 'q9_1', 10: 'q10_3'
}

user_scores = {}
user_timers = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    
    # Проверяем, проходил ли пользователь викторину
    if await check_user(user_id):
        await message.answer("Ахах, губа не дура, подожди еще годик!")
        return
    
    try:
        # Отправляем приветственное сообщение с картинкой
        welcome_photo = FSInputFile("images/welcome.jpg")
        await message.answer_photo(
            photo=welcome_photo,
            caption="Привет, друже, сегодня я бы хотел тебя поздравить с днём рождения! Но, лучший подарок это тот - который ты получил честно и заслуженно. Сыграем в игру, я задам тебе несколько вопросов, около 10. Ответишь на 7 из 10 верно, получишь подарок, а если 6 из 10 или меньше - твой подарок сгорит к чертовой матери!!! Ты готов?",
            reply_markup=start_kb
        )
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")
        await message.answer(
            "Привет, друже, сегодня я бы хотел тебя поздравить с днём рождения! Но, лучший подарок это тот - который ты получил честно и заслуженно. Сыграем в игру, я задам тебе несколько вопросов, около 10. Ответишь на 7 из 10 верно, получишь подарок, а если 6 из 10 или меньше - твой подарок сгорит к чертовой матери!!! Ты готов?",
            reply_markup=start_kb
        )

@router.callback_query(F.data == "ready_yes")
async def process_ready(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Важно: отвечаем на callback сначала
    
    try:
        welcome2_photo = FSInputFile("images/welcome_2.jpg")
        await callback.message.answer_photo(
            photo=welcome2_photo,
            caption="отлично! как будешь готов, жми ниже кнопку начать, но забыл предупредить, у вопросов стоит таймер 15 секунд, если ты не успеешь - вопрос засчитывается как проигранный! вот такая я жопа))) так зато интереснее",
            reply_markup=start_quiz_kb
        )
    except Exception as e:
        print(f"Ошибка при отправке второго фото: {e}")
        await callback.message.answer(
            "отлично! как будешь готов, жми ниже кнопку начать, но забыл предупредить, у вопросов стоит таймер 15 секунд, если ты не успеешь - вопрос засчитывается как проигранный! вот такая я жопа))) так зато интереснее",
            reply_markup=start_quiz_kb
        )
    
    await state.set_state(QuizStates.waiting_for_start)

@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Отвечаем на callback
    
    user_id = callback.from_user.id
    user_scores[user_id] = 0
    await ask_question(1, callback.message, state)

async def ask_question(question_num: int, message, state: FSMContext):
    questions = {
        1: "Отлично, первый вопрос:\nКакое слово всегда пишется неправильно?",
        2: "Едем дальше, второй вопрос:\nАтомный вес серебра?",
        3: "Давай не обосрись!\nЧто нужно делать, когда видишь зелёного человечка?",
        4: "Верю в тебя, делай!\nКак правильно говорить: «не вижу белый желток» или «не вижу белого желтка»?",
        5: "Полпути, ну почти...\nЧему равна 'мера'?",
        6: "Ты хоть представляешь какой геморрой это всё придумывать?\nКак правильно пишется имя?",
        7: "Надеюсь ты уже не ответил и на наужное количество вопросов и мы знатно поржем!!!\nКакая цифра уменьшится на треть, если её перевернуть?",
        8: "Ахахахахах) спорю ты там вспотел уже))\nВы сидите в самолёте, впереди вас лошадь, сзади автомобиль. Где Вы находитесь?",
        9: "Если ты еще не проиграл...то сейчас твой шанс проиграть))\nОтчество Канкина Стаса?",
        10: "Финиш, тут можно особо не париться...Хотя нет, парься\nВ каком месяце 28 дней?"
    }
    
    try:
        photo = FSInputFile(f"images/{question_num}.jpg")
        await message.answer_photo(
            photo=photo,
            caption=questions[question_num],
            reply_markup=create_question_kb(question_num)
        )
    except Exception as e:
        print(f"Ошибка при отправке фото вопроса {question_num}: {e}")
        await message.answer(
            questions[question_num],
            reply_markup=create_question_kb(question_num)
        )
    
    # Устанавливаем состояние для текущего вопроса
    states_map = {
        1: QuizStates.question_1, 2: QuizStates.question_2, 3: QuizStates.question_3,
        4: QuizStates.question_4, 5: QuizStates.question_5, 6: QuizStates.question_6,
        7: QuizStates.question_7, 8: QuizStates.question_8, 9: QuizStates.question_9,
        10: QuizStates.question_10
    }
    await state.set_state(states_map[question_num])
    
    # Сохраняем таймер для пользователя
    user_id = message.chat.id
    if user_id in user_timers:
        user_timers[user_id].cancel()
    
    user_timers[user_id] = asyncio.create_task(
        question_timer(question_num, message, state)
    )

async def question_timer(question_num: int, message, state: FSMContext):
    await asyncio.sleep(15)
    
    # Проверяем, не ответил ли пользователь уже
    current_state = await state.get_state()
    states_map = {
        1: QuizStates.question_1, 2: QuizStates.question_2, 3: QuizStates.question_3,
        4: QuizStates.question_4, 5: QuizStates.question_5, 6: QuizStates.question_6,
        7: QuizStates.question_7, 8: QuizStates.question_8, 9: QuizStates.question_9,
        10: QuizStates.question_10
    }
    
    expected_state = states_map.get(question_num)
    if current_state == expected_state:
        # Пользователь не ответил вовремя
        user_id = message.chat.id
        await message.answer("⏰ Время вышло! Вопрос засчитан как неправильный.")
        await process_answer(question_num, None, message, state, False)

async def process_answer(question_num: int, callback: CallbackQuery, message, state: FSMContext, is_correct: bool):
    user_id = callback.from_user.id if callback else message.chat.id
    
    # Отменяем таймер для этого пользователя
    if user_id in user_timers:
        user_timers[user_id].cancel()
        del user_timers[user_id]
    
    if is_correct:
        user_scores[user_id] = user_scores.get(user_id, 0) + 1
        response_text = f"Да, ты молодец! Сразу видно чисто ботан!\nТвой счёт {user_scores[user_id]} из 10"
    else:
        user_scores[user_id] = user_scores.get(user_id, 0)
        response_text = f"Фу, честно говоря не думал что это прям такой уж сложный вопрос, ты меня разочаровал\nТвой счёт {user_scores[user_id]} из 10"
    
    target_message = callback.message if callback else message
    await target_message.answer(response_text)
    
    if question_num < 10:
        await asyncio.sleep(2)
        await ask_question(question_num + 1, target_message, state)
    else:
        await finish_quiz(user_id, target_message, state)

async def finish_quiz(user_id: int, message, state: FSMContext):
    score = user_scores.get(user_id, 0)
    
    result_text = f"ну что же, спасибо тебе за игру, твой результат - {score}/10, на самом деле навалить какой тут результат, это же всё таки день рождения. Поэтому я думаю тут плевать на подарок, главное внимание...ну будь здоров, созраняй позитив и не будь жопой. Здоровья и прочей официально банальной штуки тебе и так нажелают..."
    
    await message.answer(result_text)
    
    # Добавляем пользователя в базу
    await add_user(user_id)
    
    # Второе сообщение через 10 секунд
    await asyncio.sleep(10)
    await message.answer("Но кстати, если серьезно я тебе советую никогда не оставаться 'таким как есть', если ты остаешься таким как есть - ты стоишь на месте. Я желаю тебе не отсутсвия трудностей и проблем, а умения их преодолевать и учиться на их опыте. Главное в жизни - семья и позитив. Будь позитивен и храни семью")
    
    # Третье сообщение через 15 секунд
    await asyncio.sleep(15)
    
    try:
        ozon_photo = FSInputFile("images/ozon.jpg")
        await message.answer_photo(
            photo=ozon_photo,
            caption="ну ладно, что то я так подумал, наверное это было бы приятно в день рождения, хоть этот день и сего...в четверг... вот что мне предложишь сегодня поднять чарку за твое здоровье и потом на рабоут завтра!?!? ловко ты придумал...или еще скажи не пить?\n\nой всё, с днем рождения, друже, маленький сувенир для тебя, там разберешься"
        )
    except Exception as e:
        print(f"Ошибка при отправке фото подарка: {e}")
        await message.answer(
            "ну ладно, что то я так подумал, наверное это было бы приятно в день рождения, хоть этот день и сего...в четверг... вот что мне предложишь сегодня поднять чарку за твое здоровье и потом на рабоут завтра!?!? ловко ты придумал...или еще скажи не пить?\n\nой всё, с днем рождения, друже, маленький сувенир для тебя, там разберешься"
        )
    
    await state.clear()

# Обработчики для каждого вопроса
@router.callback_query(QuizStates.question_1, F.data.startswith('q1_'))
async def handle_question_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[1]
    await process_answer(1, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_2, F.data.startswith('q2_'))
async def handle_question_2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[2]
    await process_answer(2, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_3, F.data.startswith('q3_'))
async def handle_question_3(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[3]
    await process_answer(3, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_4, F.data.startswith('q4_'))
async def handle_question_4(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[4]
    await process_answer(4, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_5, F.data.startswith('q5_'))
async def handle_question_5(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[5]
    await process_answer(5, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_6, F.data.startswith('q6_'))
async def handle_question_6(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[6]
    await process_answer(6, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_7, F.data.startswith('q7_'))
async def handle_question_7(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[7]
    await process_answer(7, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_8, F.data.startswith('q8_'))
async def handle_question_8(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[8]
    await process_answer(8, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_9, F.data.startswith('q9_'))
async def handle_question_9(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[9]
    await process_answer(9, callback, None, state, is_correct)

@router.callback_query(QuizStates.question_10, F.data.startswith('q10_'))
async def handle_question_10(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    is_correct = callback.data == correct_answers[10]
    await process_answer(10, callback, None, state, is_correct)