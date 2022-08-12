from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand


import asyncio
import json
import re


from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import BotCommand
from django.contrib.auth.models import User


from SECRET.KEY import API_TOKEN
# bot that will be used to register user in Django website
from website.models import Profile


class Register(StatesGroup):
    waiting_for_id = State()
    waiting_for_email = State()
    waiting_for_password = State()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="cancel", ignore_case=True), state="*")


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(register_start, commands="register", state="*")
    dp.register_message_handler(register_id, state=Register.waiting_for_id)
    dp.register_message_handler(register_email, state=Register.waiting_for_email)
    dp.register_message_handler(register_password, state=Register.waiting_for_password)


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Hi, I'm a bot that will help you register in our website writen on Django.\n"
                        "To register, please enter /register and then type your ID")


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Canceled")


async def register_start(message: types.Message):
    await message.reply("Please enter your ID")
    await Register.waiting_for_id.set()


async def register_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        # check if ID is valid by comparing it to ids in correct_ids.json
        if await check_id(message.text):
            await message.reply("Please enter your email")
            await state.update_data(id=message.text)
            await state.update_data(buyer=await get_buyer_name(message.text))
            await Register.next()
        else:
            await message.reply("ID is not valid")
            await Register.waiting_for_id.set()


async def get_buyer_name(id: str):
    # get buyer name from correct_ids.json
    with open("correct_ids.json", "r") as f:
        correct_ids = json.load(f)
    for key, value in correct_ids.items():
        if value == int(id):
            return key


async def register_email(message: types.Message, state: FSMContext):
    # check if message is valid email and not already in use
    if await check_email(message.text) and await only_one_email(message.text):
        # store email in Register state
        await state.update_data(email=message.text)
        await message.reply("Please enter your password")
        await Register.next()
    else:
        await message.reply("Email is not valid or already in use")
        await Register.waiting_for_email.set()


@sync_to_async
def create_user(email: str, password: str, id: int, buyer: str):
    user = User.objects.create_user(username=email, email=email, password=password)
    # check if buyer equals bogdan or not
    if buyer == "lovelas":
        profile = Profile(user=user, id=id, buyer=buyer)
    else:
        profile = Profile(user=user, id=id, buyer=buyer, buyer_sub_id=buyer)
    return user, profile


@sync_to_async
def save_user(user: User, profile: Profile):
    user.save()
    profile.save()


async def register_password(message: types.Message, state: FSMContext):
    # check if password mach Django requirements for password
    if check_password(message.text):
        # get email from Register state and register new user in Django website
        data = await state.get_data()
        user, profile = await create_user(data["email"], message.text, data["id"], data["buyer"])
        await save_user(user, profile)
        await message.reply("You are registered")
        await state.finish()
    else:
        await message.reply("Password is not valid")
        await Register.waiting_for_password.set()


def check_password(password: str):
    # check if password mach Django requirements for password
    if len(password) >= 8:
        return True
    else:
        return False


@sync_to_async
def only_one_email(email: str):
    # check if email is not already in use in Django website
    if User.objects.filter(email=email).exists():
        print("Email is already in use")
        return False
    else:
        print("Email is not in use")
        return True


async def check_email(email: str):
    # check if message is valid email using re
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False


@sync_to_async
def check_if_profile_with_id_exists(id: int):
    if Profile.objects.filter(id=id).exists():
        return True
    else:
        return False


async def check_id(id: str):
    # check if ID is valid by comparing it to ids in correct_ids.json
    with open("correct_ids.json", "r") as f:
        correct_ids = json.load(f)
    # check if id is digit and if it is in correct_ids.json
    if id.isdigit():
        if int(id) in correct_ids.values():
            if not await check_if_profile_with_id_exists(int(id)):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="register", description="Register in our website"),
        BotCommand(command="/cancel", description="Cancel registration"),
    ]

    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp)
    register_handlers_registration(dp)

    await set_commands(bot)

    await dp.start_polling()


class Command(BaseCommand):
    help = 'Starts the bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bot is running'))
        asyncio.run(main())
        return 0
