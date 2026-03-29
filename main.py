import os
import pika
from tokenize import String
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
import asyncio
TOKEN_API_KEY=os.getenv("TOKEN_API_KEY")
bot_id=os.getenv("bot_id")
moi_id=os.getenv("moi_id")
#брокер
from faststream.rabbit import RabbitBroker
broker=RabbitBroker(url=os.getenv("CLOUDAMQP_URL"))
connection_params = pika.URLParameters(os.getenv("CLOUDAMQP_URL"))
def get_connection():
    return pika.BlockingConnection(parameters=connection_params)
@broker.subscriber("PLATOKY")
async def get_platky_fromFASTAPI(data: str):
    await Bot.send_message(chat_id=os.getenv('MYUSERID'),text='ФЕВРОНИЯ СООБЩАЕТ')
    await Bot.send_message(chat_id=os.getenv('MYUSERID'),text=data)
@broker.subscriber("UROKI")
async def get_platky_fromFASTAPI(data: str):
    await Bot.send_message(chat_id=os.getenv('MYUSERID'),text='СЕКЛЕТЕЯ СООБЩАЕТ')
    await Bot.send_message(chat_id=os.getenv('MYUSERID'),text=data)
from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
# этр образ бота в программе
Bot = Bot(TOKEN_API_KEY)
# это обьект для обработки сообщений
dp=Dispatcher()
from aiogram.fsm.context import FSMContext
# импорты для машины конечных состояний
from aiogram.fsm.state import State, StatesGroup
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union
class Platovny_Personaz(StatesGroup):
    Grazdanskoje_Imja=State()
    Tvorceskiy_Psevdonim=State()
    Opisanije_Tvorcestva=State()
    Svaz_S_Platkami=State()
    Ssylka_Instagram=State()
    Ssylka_VK=State()
    Ssylka_Utub=State()
    Ssylka_Facebook=State()
    Ssylka_Telegram=State()
    Ssylka_Ondoklassniki=State()
    Ssylka_JandexDzen=State()
    Ssylka_Internet = State()
    Adress_Dejatelnosty = State()
platochny_geroy=[]
platochny_long=[]
validacija_zapisi=0
fakt_zapisi=0
id_zapisi=1
nov_id_zapisi=1
kolvo_personazey=0
from aiogram.types import BotCommand, Message
private=[BotCommand(command="banda",description="запуск работы с досье участников платочной банды"),
         BotCommand(command="vvod_personaza",description="ввод нового героя в платочную банду"),
         BotCommand(command="proverka_zapisi",description="проверка записи в буфере"),
         BotCommand(command='ocistka_zapisi',description='принудительная очистка буфера'),
         BotCommand(command="registracija_zapisi",description="регистрация участника платочной банды в базу данных"),
        BotCommand(command="start",description="вывод приветственного сообщения"),
        BotCommand(command="stop",description="аварийный останов бота"),
        BotCommand(command="exit",description="отмена поискового запроса, выход из анкеты")]
# Работа с заметками
class PlatochnaBandaSvodka(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> None:
        text = event.text
        user_id = event.from_user.id
        global nov_id_zapisi
        global id_zapisi
        global kolvo_personazey
        if text =="/vvod_personaza":
            kolvo_personazey = 0
            await self.bot.send_message(chat_id=user_id, text="Работаем с платочной бандой")
            # создание интерфейса для sql запроса
            import psycopg2 as ps
            connection = ps.connect(host="localhost", database="Palto", user="postgres", password="Uspech4815162342")
            # создание интерфейса для sql запроса
            cursor = connection.cursor()
            zapros = "SELECT * FROM Платочная_банда;"
            # отправить запрос системе управления
            cursor.execute(zapros)
            while True:
                next_row = cursor.fetchone()
                if next_row:
                    id = next_row[0]
                    kolvo_personazey = kolvo_personazey + 1
                    if id > nov_id_zapisi:
                        nov_id_zapisi = id
                else:
                    break
            connection.commit()
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            id_zapisi = nov_id_zapisi + 1
            await self.bot.send_message(chat_id=user_id, text=f"{'Доступный артикул для персонажа: '}{id_zapisi}")
            await self.bot.send_message(chat_id=user_id, text=f"{'Всего персонажей введено:'}{kolvo_personazey}")
            return await handler(event, data)
        else:
            return await handler(event, data)
dp.message.middleware(PlatochnaBandaSvodka(Bot))
@dp.message((F.text.lower()=="/start"))
@dp.message((F.text.lower()=="старт"))
@dp.message((F.text.lower()=="пуск"))
async def start_command(message: types.Message):
    await message.answer(text="Наливай,поехали!!!")
    print("Уиииииииииииииииииииииии")
@dp.message((F.text.lower()=="/stop"))
@dp.message((F.text.lower()=="авария"))
async def stop(message: types.Message, state:FSMContext):
        await state.clear()
        await message.answer("Моя остановочка")
        print("Bota ripnuli")
        raise KeyboardInterrupt
@dp.message((F.text.lower()=="/clear"))
@dp.message((F.text.lower()=="сброс"))
async def sbros_registacii(message: types.Message, state: FSMContext):
    await message.answer(text="Выход из анкетирования, отмена составления опросника")
    await state.clear()
    print("Выход из анкетирования, отмена составления опросника")
@dp.message((F.text.lower() == "/ocistka_zapisi"))
@dp.message((F.text.lower() == "очистка записи"))
async def ocistka_zapisi(message: types.Message):
    await message.answer(text="Принудительная очистка записи")
    global platochny_geroy
    global platochy_long
    global fakt_zapisi
    if len(platochny_geroy) == 0 and len(platochny_long) == 0:
        await message.answer(text="Буфер и так пустой")
        return
    else:
        platochny_geroy.clear()
        platochny_long.clear()
        fakt_zapisi = 0
        await message.answer(text="Данные в буфере стерты")
@dp.message((F.text.lower()=="/vvod_personaza"))
@dp.message((F.text.lower()=="ввод_персонажа"))
async def vvod_personaza(message: types.Message, state: FSMContext):
    await message.answer(text="Вы начали ввод нового участника платочной банды")
    await state.set_state(Platovny_Personaz.Grazdanskoje_Imja)
    await message.answer(text="Напиши гражданское имя участника платочной банды")
@dp.message((F.text.lower()=="vvod_personaza"))
@dp.message((F.text.lower()=="ввод_персонажа"))
async def vvod_personaza(message: types.Message, state: FSMContext):
    await message.answer(text="Вы начали ввод нового участника платочной банды")
    await state.set_state(Platovny_Personaz.Grazdanskoje_Imja)
    await message.answer(text="Напиши гражданское имя участника платочной банды")
@dp.message(Platovny_Personaz.Grazdanskoje_Imja, F.text)
async def grazdansoje_imja(message: types.Message,state: FSMContext):
    await state.update_data(grazdanskoje_imja=message.text)
    await message.answer(text="Укажи творческий псевдоним участника платочной банды")
    await state.set_state(Platovny_Personaz.Tvorceskiy_Psevdonim)
@dp.message(Platovny_Personaz.Tvorceskiy_Psevdonim, F.text)
async def tvorceskiy_psevdonim(message: types.Message,state: FSMContext):
    await state.update_data(tvorceskiy_psevdonim=message.text)
    await message.answer(text="Опиши творческую деятельность участника платочной банды")
    await state.set_state(Platovny_Personaz.Opisanije_Tvorcestva)
@dp.message(Platovny_Personaz.Opisanije_Tvorcestva, F.text)
async def opisanije_tvorcestva(message: types.Message,state: FSMContext):
    await state.update_data(opisanije_tvorcestva=message.text)
    await message.answer(text="Опиши, что связывает творчество данного персонажа с Павлопосадскими платками")
    await state.set_state(Platovny_Personaz.Svaz_S_Platkami)
@dp.message(Platovny_Personaz.Svaz_S_Platkami, F.text)
async def svaz_s_platkami(message: types.Message,state: FSMContext):
    await state.update_data(svjaz_s_platkami=message.text)
    await message.answer(text="Укажи ссылку на Инстаграм данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_Instagram)
@dp.message(Platovny_Personaz.Ssylka_Instagram, F.text)
async def ssylka_instagram(message: types.Message,state: FSMContext):
    await state.update_data(ssylka_instagram=message.text)
    await message.answer(text="Укажи ссылку на ВК данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_VK)
@dp.message(Platovny_Personaz.Ssylka_VK, F.text)
async def ssylka_vk(message: types.Message,state: FSMContext):
    await state.update_data(ssylka_vk=message.text)
    await message.answer(text="Укажи ссылку на Ютуб данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_Utub)
@dp.message(Platovny_Personaz.Ssylka_Utub, F.text)
async def ssylka_vk(message: types.Message,state: FSMContext):
    await state.update_data(ssylka_Utub=message.text)
    await message.answer(text="Укажи ссылку на Фейсбук данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_Facebook)
@dp.message(Platovny_Personaz.Ssylka_Facebook, F.text)
async def ssylka_facebook(message: types.Message,state: FSMContext):
    await state.update_data(ssylka_facebook=message.text)
    await message.answer(text="Укажи ссылку на Телеграм данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_Telegram)
@dp.message(Platovny_Personaz.Ssylka_Telegram, F.text)
async def ssylka_telegram(message: types.Message,state: FSMContext):
    await state.update_data(ssylka_telegram=message.text)
    await message.answer(text="Укажи ссылку на Одноклассники данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_Ondoklassniki)
@dp.message(Platovny_Personaz.Ssylka_Ondoklassniki, F.text)
async def ssylka_telegram(message: types.Message,state: FSMContext):
    await state.update_data(ssylka_odnoklassniki=message.text)
    await message.answer(text="Укажи ссылку на Яндекс Дзен данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_JandexDzen)
@dp.message(Platovny_Personaz.Ssylka_JandexDzen, F.text)
async def ssylka_JandexDzen(message: types.Message,state: FSMContext):
    await state.update_data(ssylka_jandexdzen=message.text)
    await message.answer(text="Укажи ссылку на сайт в Интернете данного участника платочной банды")
    await state.set_state(Platovny_Personaz.Ssylka_Internet)
@dp.message(Platovny_Personaz.Ssylka_Internet, F.text)
async def ssylka_Internet(message: types.Message, state: FSMContext):
    await state.update_data(ssylka_internet=message.text)
    await message.answer(text="Напиши адрес, где трудится данный участник платочной банды")
    await state.set_state(Platovny_Personaz.Adress_Dejatelnosty)
@dp.message(Platovny_Personaz.Adress_Dejatelnosty, F.text)
async def Adress_Dejatelnosty(message: types.Message, state: FSMContext):
    global platochny_geroy
    global fakt_zapisi
    await state.update_data(adress_dejatelnosty=message.text)
    data=await state.get_data()
    platochny_pesonaz=data.get('grazdanskoje_imja', None)
    platochny_geroy.append(platochny_pesonaz)
    tvorceskiy_psevdonim=data.get('tvorceskiy_psevdonim', None)
    platochny_geroy.append(tvorceskiy_psevdonim)
    opisanije_tvorcestva=data.get('opisanije_tvorcestva', None)
    platochny_geroy.append(opisanije_tvorcestva)
    svjaz_s_platkami=data.get('svjaz_s_platkami', None)
    platochny_geroy.append(svjaz_s_platkami)
    ssylka_instagram=data.get('ssylka_instagram', None)
    platochny_geroy.append(ssylka_instagram)
    ssylka_vk=data.get('ssylka_vk', None)
    platochny_geroy.append(ssylka_vk)
    ssylka_Utub=data.get('ssylka_Utub', None)
    platochny_geroy.append(ssylka_Utub)
    ssylka_facebook=data.get('ssylka_facebook', None)
    platochny_geroy.append(ssylka_facebook)
    ssylka_telegram=data.get('ssylka_telegram', None)
    platochny_geroy.append(ssylka_telegram)
    ssylka_odnoklassniki=data.get('ssylka_odnoklassniki', None)
    platochny_geroy.append(ssylka_odnoklassniki)
    ssylka_jandexdzen=data.get('ssylka_jandexdzen', None)
    platochny_geroy.append(ssylka_jandexdzen)
    ssylka_Internet=data.get('ssylka_internet', None)
    platochny_geroy.append(ssylka_Internet)
    adress_dejatelnosti=data.get('adress_dejatelnosty', None)
    platochny_geroy.append(adress_dejatelnosti)
    await message.answer(text =f"{platochny_geroy}")
    await message.answer(text="Информация о новом участнике платочной банды записана")
    fakt_zapisi=1
    await state.clear()
@dp.message((F.text.lower() == "/proverka_zapisi"))
@dp.message((F.text.lower() == "проверка записи"))
async def proverka_zapisi(message: types.Message):
    await message.answer(text="Проверка введенной записи")
    global platochny_geroy
    global validacija_zapisi
    if len(platochny_geroy) == 0:
        await message.answer(text="Нет данных для проверки")
        return
    else:
        for i in range(len(platochny_geroy)):
            if platochny_geroy[i] == "":
                await message.answer(text="Данные повреждены")
                break
            else:
                validacija_zapisi=1
    if validacija_zapisi == 1:
        await message.answer(text="Данные в порядке")
        await message.answer(text =f"{platochny_geroy}")
@dp.message((F.text.lower() == "/registracija_zapisi"))
@dp.message((F.text.lower() == "регистрация записи"))
async def proverka_zapisi(message: types.Message):
    global validacija_zapisi
    global platochny_geroy
    global platochny_long
    global fakt_zapisi
    global id_zapisi
    await message.answer(text="Регистрация сведений об участнике платочной банды в ВК")
    if fakt_zapisi == 0:
        await message.answer(text="Нечего вносить в базу данных, пожалуйста сделайте запись и попробуйте ещё раз")
        return
    elif validacija_zapisi == 0:
        await message.answer(text="Данные не прошли проверку перед внесением в БД, пожалуйста сделайте валидацию данных и попробуйте ещё раз")
        return
    elif fakt_zapisi == 1 and validacija_zapisi == 1 and len(platochny_geroy) == 13:
        platochny_long.append(id_zapisi)
        for i in range(len(platochny_geroy)):
            mysl=platochny_geroy[i]
            platochny_long.append(mysl)
        platocny_kartez = tuple(platochny_long)
        # импорт библиотеки для pq админ
        import psycopg2 as ps
        # создание подключения
        connection = ps.connect(host="localhost", database="Palto", user="postgres", password="Uspech4815162342")
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        query = '''INSERT INTO Платочная_банда (id, Гражданское_Имя, Творческий_Псевдоним, Описание_Творческой_Деятельности, Связь_Творчества_С_Павлопосадскими_Платками, 
        Ссылка_На_Инстаграм, Ссылка_На_ВК, Ссылка_На_Ютуб, Ссылка_На_Фейсбук, Ссылка_На_Телеграм, Ссылка_На_Одноклассники, Ссылка_На_Яндекс_Дзен, Ссылка_на_сайт, Адрес_Деятельности)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        # подать запрос системе управления БД
        cursor.execute(query, platocny_kartez)
        # синхронизация изменений, комит версии
        connection.commit()
        # закрытие соединенмя с ДБ для безопасности
        cursor.close()
        connection.close()
        platochny_geroy=[]
        platochny_long=[]
        fakt_zapisi=0
        id_zapisi=id_zapisi+1
        await message.answer(text="Запись успешно внесена")
def process_message(channel,method,properties,body):
    print(body)
    print(properties)
    print(channel)
    print(method)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    return None
def krolik():
    with get_connection() as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue='PLATOKY2', durable=False)
            channel.basic_consume(on_message_callback=process_message, queue='PLATOKY2')
            channel.start_consuming()
async def main():
    async with broker:
        await broker.start()
        await Bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
        await Bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(Bot) 
if __name__ == "__main__":
    asyncio.run(main())
    krolik()