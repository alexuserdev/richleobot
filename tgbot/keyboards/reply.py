from aiogram import types
from aiogram.dispatcher import FSMContext

answers_buttons = [
    ["Talk", "Skip"],
    ["More info", "Skip"]
]

main_menu_buttons = ["📝 Operations", "💼 Balance", "🛠 Settings", "🔎 Help"]


def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for button in main_menu_buttons:
        keyboard.insert(types.KeyboardButton(text=button))
    return keyboard


def escrow_deal_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Cancel"))
    return keyboard


class RegistrationKeyboards:
    def __init__(self, state: FSMContext):
        self.state = state
        self.index = None

    async def get_keyboard(self):
        state_now = await self.state.get_state()
        print(state_now)
        if state_now == "FirstRegistrationStates:first_answer":
            self.index = 1
        elif state_now == "FirstRegistrationStates:second_asnwer":
            self.index = 1
        else:
            self.index = 0
        return self.create_keyboard()

    def create_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in answers_buttons[self.index]:
            keyboard.insert(types.KeyboardButton(text=button))
        return keyboard