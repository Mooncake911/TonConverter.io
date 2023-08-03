# ---~Ton Converter Bot~--- #
from pathlib import Path
from aiogram import executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, InputFile, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked
import keyboards as kb
from converter import converter


TOKEN_API = '6205743629:AAE9Ua6tRqC_O21S731o-8vov8AwlQ86s4w'
ALLOWED_EXTENSIONS = {".docx", ".pdf", ".doc", ".html", ".docm", ".dotx", ".dot", ".md", ".rtf", ".odt", ".ott", ".txt",
                      ".epub", ".mht", ".mhtml", ".svg", ".bmp", ".png", ".jpg", ".jpeg", ".gif"}
HELP_COMMAND = """
<b>~- - - - - - - - - - - - - - - - - - - - -~</b>
<b>/help</b> - <em>list of commands</em>
<b>/start</b> - <em>run bot</em>
<b>/info</b> - <em>what this bot can do (in detail)</em>
<b>/convert</b> - <em>run convert process</em>
<b>/cancel</b> - <em>stop convert process</em>
<b>~- - - - - - - - - - + - - - - - - - - - -~</b>
"""


storage = MemoryStorage()
bot = Bot(TOKEN_API, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    print('Ton Converter Bot activated!')


class GetFileTask(StatesGroup):
    file = State()
    format = State()
    name = State()


# ///////////////////////////////////////////////// Block 1 ////////////////////////////////////////////////////////// #
@dp.message_handler(commands=['start', 'info'])
async def cmd_start(message: Message) -> None:
    user_full_name = message.from_user.full_name
    await bot.send_message(message.chat.id,
                           f"Hi {user_full_name}!\n"
                           f"Ton Converter Bot can convert the following types of files: "
                           f".docx, .pdf, .doc, .jpg, .jpeg, .gif, .png, .bmp, .svg, .tiff, .html, .docm, .dotx,"
                           f".dot, .md, .rtf, .odt, .ott, .txt, .mht, .mhtml, .zip. \n\n"
                           f"~ How to use? ~\n"
                           f"1. Just call /convert and send your file and then choose the needed format.\n"
                           f"2. Or You can tab the menu button.\n", reply_markup=kb.get_file_keyboard())
    await message.delete()


@dp.message_handler(commands=['help'])
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_COMMAND, parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['convert'], state=None)
async def cmd_convert(message: Message) -> None:
    await GetFileTask.file.set()
    await message.answer("Send me your file! ✉️", reply_markup=kb.get_cancel_keyboard())
    await message.delete()


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("🥶 Bot, reloaded...", reply_markup=kb.get_file_keyboard())
        return
    await message.answer("‼️The process was stopped.", reply_markup=kb.get_file_keyboard())
    await message.delete()
    await state.finish()


@dp.message_handler(Text(equals=['Thank', 'Thank u', 'Thank you', 'Thanks'], ignore_case=True))
async def thanks_fun(message: Message) -> None:
    await message.answer(f"I was happy to help. 😉\nI'm just a app, but you can support my creators with donate. ❤️💸",
                         reply_markup=kb.get_file_keyboard())
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #


# ///////////////////////////////////////////////// Block 2 ////////////////////////////////////////////////////////// #
@dp.message_handler(lambda message: not message.document or not message.photo, state=GetFileTask.file)
async def check_file(message: Message) -> Message:
    return await message.reply("What dose it mean?! 🥸\n"
                               "I can't understand humans speech(\n"
                               "I can only interpretate your commands.\n"
                               "Please, send me a file) 📄", reply_markup=kb.get_cancel_keyboard())


@dp.message_handler(lambda message: message.document or message.photo,
                    content_types=['document', 'photo'], state=GetFileTask.file)
async def load_file(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.from_user.full_name
        if message.document:
            data['file'] = message.document.file_id
        else:
            data['file'] = message.photo[0].file_id
    await GetFileTask.next()
    await message.reply(f"Please, choose the extension you want to convert 📌:",
                        reply_markup=kb.get_format_keyboard())


@dp.message_handler(state=GetFileTask.format)
async def check_format(message: Message) -> Message:
    return await message.reply("What dose it mean?! 🥸\n"
                               "I can't understand humans speech(\n"
                               "I can only interpretate your commands.\n"
                               "Please, choose a format in the table) 📎", reply_markup=kb.get_cancel_keyboard())


@dp.callback_query_handler(state=GetFileTask.format)
async def add_format(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    # Download
    async with state.proxy() as data:
        file = await bot.get_file(data['file'])
        old_file = file.file_path
    await bot.download_file(old_file, old_file)

    # Check file extension
    if Path(old_file).suffix in ALLOWED_EXTENSIONS:
        # Convert
        converter(Path(old_file), callback.data)
        await callback.answer("♻️I'm converting your file...\n Please, don't interrupt the process!", show_alert=True)
        # Send new file back
        try:
            new_file = InputFile(Path(old_file).with_suffix(callback.data))
        except FileNotFoundError:
            new_file = InputFile(Path(old_file).with_suffix('.zip'))
        await bot.send_document(callback.from_user.id, new_file, reply_markup=kb.get_file_keyboard())
        # Delete files forever!
        Path(old_file).unlink()
        Path(new_file.file.name).unlink()
    else:
        await bot.send_message(chat_id=callback.message.chat.id, reply_markup=kb.get_file_keyboard(),
                               text='If somthing went wrong 😢 or you have some idea 💡 to improve this bot:\n '
                                    'Please, wright to the support @Vadim_noodle. [🇬🇧; 🇷🇺]')
        await callback.answer(f"❌ Sorry, I don't support this [{Path(old_file).suffix}] format!", show_alert=True)

    await state.finish()
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #


# ///////////////////////////////////////////////// Block 3 ////////////////////////////////////////////////////////// #
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(message: Message) -> bool:
    print(f"Bot was blocked by user {message.from_user.id}")
    return True
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# development of https://github.com/Mooncake911
