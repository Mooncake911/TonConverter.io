from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton


def get_file_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/convert'))
    kb.add(KeyboardButton('/info'))
    kb.add(KeyboardButton('/help'))
    return kb


def get_format_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(resize_keyboard=True, row_width=4).add(
        InlineKeyboardButton(text='.docx', callback_data='.docx'),
        InlineKeyboardButton(text='.pdf', callback_data='.pdf'),
        InlineKeyboardButton(text='.doc', callback_data='.doc'),
        InlineKeyboardButton(text='.jpg', callback_data='.jpg'),
        InlineKeyboardButton(text='.jpeg', callback_data='.jpeg'),
        InlineKeyboardButton(text='.gif', callback_data='.gif'),
        InlineKeyboardButton(text='.png', callback_data='.png'),
        InlineKeyboardButton(text='.bmp', callback_data='.bmp'),
        InlineKeyboardButton(text='.svg', callback_data='.svg'),
        InlineKeyboardButton(text='.html', callback_data='.html'),
        InlineKeyboardButton(text='.docm', callback_data='.docm'),
        InlineKeyboardButton(text='.dotx', callback_data='.dotx'),
        InlineKeyboardButton(text='.dot', callback_data='.dot'),
        InlineKeyboardButton(text='.md', callback_data='.md'),
        InlineKeyboardButton(text='.rtf', callback_data='.rtf'),
        InlineKeyboardButton(text='.odt', callback_data='.odt'),
        InlineKeyboardButton(text='.ott', callback_data='.ott'),
        InlineKeyboardButton(text='.txt', callback_data='.txt'),
        InlineKeyboardButton(text='.mht', callback_data='.mht'),
        InlineKeyboardButton(text='.mhtml', callback_data='.mhtml'),
        InlineKeyboardButton(text='.zip', callback_data='.zip'))
    return ikb


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))
