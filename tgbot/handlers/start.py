from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline import OperationsKeyboard
from tgbot.keyboards.reply import RegistrationKeyboards, main_menu_keyboard, answers_buttons
from tgbot.misc.db_api.database import RequestsDb
from tgbot.misc.states import FirstRegistrationStates, DepositStates
from tgbot.misc.db_api import UsersDb


async def start(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args:
        info = await RequestsDb.parse_request(args)
        await message.answer(f"{'User'} asks you to donate {info[3]} {info[2]}",
                             reply_markup=OperationsKeyboard.in_request(args))
        return
    if await UsersDb.user_exists(message.chat.id):
        await message.answer_sticker("CAACAgIAAxkBAAICT2D1mnmw-Ni0QjixE3BST9jwWHq4AAIQDgACTimoSq9L4dg1FFlAIAQ")
        await message.answer(f"Welcome back {message.chat.first_name}.\n\n"
                             f"How we can help you?",
                             reply_markup=main_menu_keyboard())
    else:
        await FirstRegistrationStates.first()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Send location",
                                          request_location=True))
        keyboard.add(types.KeyboardButton(text="Skip"))
        await message.answer("Please send your location",
                             reply_markup=keyboard)


async def entered_location(message: types.Message, state: FSMContext):
    await UsersDb.register_user(message.chat.id)
    await message.answer_sticker("CAACAgIAAxkBAAICT2D1mnmw-Ni0QjixE3BST9jwWHq4AAIQDgACTimoSq9L4dg1FFlAIAQ")
    await message.answer(f"Welcome back {message.chat.first_name}.\n\n"
                         f"How we can help you?",
                         reply_markup=main_menu_keyboard())
    print(message.location)


async def skip_location(message: types.Message, state: FSMContext):
    await UsersDb.register_user(message.chat.id)
    await message.answer_sticker("CAACAgIAAxkBAAICT2D1mnmw-Ni0QjixE3BST9jwWHq4AAIQDgACTimoSq9L4dg1FFlAIAQ")
    await message.answer(f"Welcome back {message.chat.first_name}.\n\n"
                         f"How we can help you?",
                         reply_markup=main_menu_keyboard())
    await state.finish()


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, text="Cancel", state=DepositStates.check_transaction)
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(entered_location, content_types=['location'])
    dp.register_message_handler(skip_location, state=FirstRegistrationStates.first_answer)


