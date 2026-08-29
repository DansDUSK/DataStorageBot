from aiogram import types, F, Router
from aiogram.filters import Command
import html
from states import Note_State, File_State, All_State
from keyboards import main_keyboard, delete_keyboard, cancel_menu, cancel_menu2, search_keyboard, get_filess
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from utils import generate_code
from basedatastorage import (add_note, get_note, search_note, delete_note, get_file_unique, get_file_user_id, save_file, delete_file_by_code,
                             search_file, all_search, delete_all_user_data)


router = Router()

# =====START=====
@router.message(Command("start"))
async def start(message: types.Message):
    try:
        await message.answer(f"👀 Привет <b>{html.escape(message.from_user.full_name)}</b>!\n\n Я твое универсальное хранилище файлов и данных, выбери взаимодействие ниже😊", reply_markup=main_keyboard())
    except TelegramBadRequest:
        await message.answer("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        
# =====MENU (ALL FUNCTION)=====
@router.callback_query(F.data == "menu")
async def start(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(f"🚀 <b>Главное меню</b>\n\nВыберите взаимодействие ниже:", reply_markup=main_keyboard())
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()

@router.callback_query(F.data == "search")
async def search(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text("🚀 Выберите ниже по каким категориям искать", reply_markup=search_keyboard()) 
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer() 
        
@router.callback_query(F.data == "get_files_all")
async def get_files_all(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text("🚀 Выберите ниже какие записи показать", reply_markup=get_filess())
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()

@router.callback_query(F.data == "delete_menu")
async def delete_menu(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text("😔 Выберите ниже что будем удалять", reply_markup=delete_keyboard())
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()     
         
# =====NOTES FUNCTION=====
# ADD NOTES
@router.callback_query(F.data == "add_note")
async def add_note_1(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("✏ Введите текст заметки:", reply_markup=cancel_menu())
        await state.set_state(Note_State.waiting_text)
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
@router.message(Note_State.waiting_text, F.text)
async def add_note_2(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("❌ <u>Заметка не может быть пустой!</u>", reply_markup=cancel_menu2())
        await state.clear()
        return
    add_note(message.from_user.id, message.text.strip())
    await message.answer("✔ Заметка сохранена", reply_markup=cancel_menu2())
    await state.clear()
    
# GET NOTES
@router.callback_query(F.data == "get_notes")
async def get_notes(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        print("👤 user_id в get_notes:", user_id)
        notes = get_note(user_id)
        print("📝 get_notes() вернула:", notes)
        text = ""
        if not notes:
            await callback.message.edit_text("😔 У вас пока нет заметок", reply_markup=cancel_menu2())
            await callback.answer()
            return
        elif notes:
            text += "📄<b>Заметки</b>\n\n"
            for note in notes:
                text += f"#{note[0]}: {note[2]} | {note[3]}\n"
            if len(notes) > 12:
                text += f"...и ещё {len(notes) - 12} заметок😎\n"
        await callback.message.edit_text(text, reply_markup=cancel_menu2())
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
# SEARCH NOTES
@router.callback_query(F.data == "search_note")
async def search_note123(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("😋 Введите ключевое слово для поиска по заметкам", reply_markup=cancel_menu2())
        await state.set_state(Note_State.waiting_search)
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
@router.message(Note_State.waiting_search, F.text)
async def search_note1(message: types.Message, state: FSMContext):
    text1 = message.text
    notes = search_note(message.from_user.id, text1)
    text = ""
    if not notes:
        await message.answer("❌ Заметок не найдено! <u>Проверьте вводимые данные</u>", reply_markup=cancel_menu2())
    else:
        text += f"🔍 <b>Найдено заметок: {len(notes)}</b>\n\n"
        for note in notes:
            text += f"`#{note[0]}:` {note[3]} — {note[2]}\n"
        await message.answer(text, reply_markup=main_keyboard())
    await state.clear()

# DELETE NOTES
@router.callback_query(F.data == "delete_note")
async def delete_note1(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("✏ <b>Введите ID</b> для удаления заметки(узнать можно с помощью показа заметки)", reply_markup=cancel_menu())
        await state.set_state(Note_State.waiting_delete)
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
@router.message(Note_State.waiting_delete, F.text)
async def delete_note2(message: types.Message, state: FSMContext):
    try:
        note_id = int(message.text)
        user_id = message.from_user.id
        # Получаем заметки для проверки
        notes = get_note(user_id)
        note_exists = any(note[0] == note_id for note in notes)
        
        if note_exists:
            delete_note(user_id, note_id)
            await message.answer(f"✔ Заметка {note_id} успешно удалена!", reply_markup=cancel_menu2())
        else:
            await message.answer(f"❌ Заметка с ID {note_id} <u>не найдена!</u>", reply_markup=cancel_menu2())
    except ValueError:
        await message.answer("❌ Ошибка! <u>Введите число для айди заметки!</u>", reply_markup=cancel_menu2())
    await state.clear()
# =====FILE FUNCTION=====
# SAVE FILE
@router.callback_query(F.data == "add_file")
async def add_file(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("✏ Введите описание файла", reply_markup=cancel_menu())
    await state.set_state(File_State.waiting_description)
    await callback.answer()
    
@router.message(File_State.waiting_description, F.text)
async def add_file2(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("📎 Отправьте файл (фото, видео, документ):")
    await state.set_state(File_State.waiting_file)

@router.message(File_State.waiting_file, F.photo | F.document | F.video)
async def add_file3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    description = data.get("description", "Без описания")

    if message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = "photo"
    elif message.video:
        file_id = message.video.file_id
        file_type = "video"
    else:
        await message.answer("❌ Неподдерживаемый формат. <u>Отправьте фото, документ или видео.</u>")
        return

    unique_code = generate_code().upper()
    save_file(message.from_user.id, file_id, file_type, description, unique_code)

    await message.answer(
        f"✅ Файл сохранён!\n\n"
        f"📌 <b>ID(уникальный код):</b> <code>{unique_code}</code>\n"
        f"📝 <b>Описание:</b> {description}\n\n"
        f"Используй /get <code>{unique_code}</code> чтобы получить файл.",
        reply_markup=cancel_menu2()
    )
    await state.clear()
    
# Обработчик для любых других сообщений в состоянии ожидания файла
@router.message(File_State.waiting_file)
async def add_file3_unknown(message: types.Message, state: FSMContext):
    await message.answer(
        "❌ Неподдерживаемый формат. <u>Отправьте фото, документ или видео.</u>",
        reply_markup=cancel_menu2()
    )
    await state.clear()  
    
# GET FILE UNIQUE
@router.message(Command("get"))
async def get_file_command(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ <b>Напиши</b>: `/get КОД`", reply_markup=cancel_menu2())
        return
    code = parts[1].strip().upper()
    result = get_file_unique(code)
    if result:
        row = result[0]
        file_id = row[2]
        file_type = row[3]
        description = row[4]
        caption = f"📎 {description}\n📌 ID: <code>{code}</code>"
        if file_type == "photo":
            await message.answer_photo(file_id, caption=caption, parse_mode="HTML")
            await message.answer("✅ Файл получен!", reply_markup=cancel_menu2())
            print(f"📤 Отправляю файл: file_id={file_id}, type={file_type}")
        elif file_type == "document":
            await message.answer_document(file_id, caption=caption, parse_mode="HTML")
            await message.answer("✅ Файл получен!", reply_markup=cancel_menu2())
            print(f"📤 Отправляю файл: file_id={file_id}, type={file_type}")
        elif file_type == "video":
            await message.answer_video(file_id, caption=caption, parse_mode="HTML")
            await message.answer("✅ Файл получен!", reply_markup=cancel_menu2())
            print(f"📤 Отправляю файл: file_id={file_id}, type={file_type}")
    else:
        await message.answer(f"❌ Файл с ID <code>{code}</code> <u>не найден.</u>", reply_markup=cancel_menu2())
        
@router.callback_query(F.data == "get_files1")
async def get_files1(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("💾 Введите <b>уникальный код файла</b>", reply_markup=cancel_menu())
        await state.set_state(File_State.waiting_search_unique_code)
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
@router.message(File_State.waiting_search_unique_code, F.text)
async def get_files11(message: types.Message, state: FSMContext):
    code = message.text.strip().upper()
    print(f"📥 Введён код: '{code}'")
    result = get_file_unique(code)
    print(f"📤 Результат поиска: {result}")
    if result:
        row = result[0]
        file_id = row[2]
        file_type = row[3]
        description = row[4]
        caption = f"📎 {description}\n📌 ID: <code>{code}</code>"
        if file_type == "photo":
            await message.answer_photo(file_id, caption=caption, parse_mode="HTML")
            await message.answer("✅ Файл получен!", reply_markup=cancel_menu2())
            print(f"📤 Отправляю файл: file_id={file_id}, type={file_type}")
        elif file_type == "document":
            await message.answer_document(file_id, caption=caption, parse_mode="HTML")
            await message.answer("✅ Файл получен!", reply_markup=cancel_menu2())
            print(f"📤 Отправляю файл: file_id={file_id}, type={file_type}")
        elif file_type == "video":
            await message.answer_video(file_id, caption=caption, parse_mode="HTML")
            await message.answer("✅ Файл получен!", reply_markup=cancel_menu2())
            print(f"📤 Отправляю файл: file_id={file_id}, type={file_type}")
    else:
        await message.answer(f"❌ Файл с ID <code>{code}</code> <u>не найден.</u>", reply_markup=cancel_menu2())
    await state.clear()
        
        
# GET FILE USER ID
@router.callback_query(F.data == "get_files")
async def get_files(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        files = get_file_user_id(user_id)
        text = ""
        if not files:
            await callback.message.edit_text("😔 У вас пока нет файлов", reply_markup=cancel_menu2())
            await callback.answer()
            return
        if files:
            text += "\n📎<b>Файлы</b>\n\n"
            for file in files:
                text += f"#{file[0]}({file[5]}): {file[3]} | {file[4]} | {file[6]}\n"
            if len(files) > 12:
                text += f"...и ещё {len(files) - 12} файлов😋"
        await callback.message.edit_text(text, reply_markup=cancel_menu2())
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
    
# SEARCH FILE
@router.callback_query(F.data == "search_file")
async def search_file1(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("😋 Введите ключевое слово для поиска по файлам", reply_markup=cancel_menu2())
        await state.set_state(File_State.waiting_search_file)
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
@router.message(File_State.waiting_search_file, F.text)
async def search_file2(message: types.Message, state: FSMContext):
    text1 = message.text
    files = search_file(message.from_user.id, text1)
    text = ""
    if not files:
        await message.answer("❌ Файлов не найдено! <u>Проверьте вводимые данные</u>", reply_markup=cancel_menu2())
    else:
        text += f"🔍 <b>Найдено файлов: {len(files)}</b>\n\n"
        for file in files:
            text += f"#{file[0]}<code>(UNIQUE CODE: {file[5]}):</code> {file[3]} — {file[4]} — {file[6]}\n"
        await message.answer(text, reply_markup=cancel_menu2())
    await state.clear()

# DELETE FILE BY CODE
@router.callback_query(F.data == "delete_file")
async def delete_file1(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("✏ Введите <b>уникальный код</b> для удаления файла(можно посмотреть в показе файлов)", reply_markup=cancel_menu())
        await state.set_state(File_State.waiting_delete_id)
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
@router.message(File_State.waiting_delete_id, F.text)
async def delete_file2(message: types.Message, state: FSMContext):
    try:
        unique_code = message.text.strip().upper()
        user_id = message.from_user.id
        deleted = delete_file_by_code(unique_code, user_id)  # ← сохраняем результат
        if deleted:
            await message.answer(f"✔ Файл <code>{unique_code}</code> успешно удалён!", reply_markup=cancel_menu2())
        else:
            await message.answer(f"❌ Файл с кодом <code>{unique_code}</code> <u>не найден!</u>", reply_markup=cancel_menu2())
    except Exception as e:
        await message.answer("❌ <b>Ошибка при удалении!</b>", reply_markup=cancel_menu2())
    await state.clear()

# =====ALL FILES AND NOTES=====
@router.callback_query(F.data == "all_files")
async def all_files(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    notes = get_note(user_id)
    files = get_file_user_id(user_id)
    text = ""
    if not notes and not files:
        await callback.message.edit_text("😔 У вас пока нет записей", reply_markup=cancel_menu2())
        await callback.answer()
        return
    if notes:
        text += "📄<b>Заметки</b>\n\n"
        for note in notes:
            text += f"#{note[0]}: {note[2]} | {note[3]}\n"
        if len(notes) > 12:
            text += f"...и ещё {len(notes) - 12} заметок😎\n"
    if files:
        text += "\n📎<b>Файлы</b>\n\n"
        for file in files:
            text += f"#{file[0]}({file[5]}): {file[3]} | {file[4]} | {file[6]}\n"
        if len(files) > 12:
            text += f"...и ещё {len(files) - 12} файлов😋"
    await callback.message.edit_text(text, reply_markup=cancel_menu2())
    await callback.answer()
# =====GLOBAL DELETE=====
@router.callback_query(F.data == "delete_all")
async def delete_all1(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("👀😔 Вы уверены что хотите удалить все данные?(Да/Нет)", reply_markup=cancel_menu2())
        await state.set_state(All_State.waiting_user_answer)
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
        await callback.answer()
@router.message(All_State.waiting_user_answer, F.text)
async def delete_all2(message: types.Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    try:
        if text.lower() == "да":
            await message.answer("🙁 Принял! Удаляю все ваши файлы")
            delete_all_user_data(user_id)
            await message.answer("✔ Удаление прошло успешно! Ждем вас снова)",  reply_markup=cancel_menu2())
        elif text.lower() == "нет":
            await message.answer("✨ Удаление отменено!", reply_markup=cancel_menu2())
        else:
            await message.answer("❌ Ошибка! Введите <b>да</b> или <b>нет</b>", reply_markup= cancel_menu2())
        await state.clear()
    except ValueError:
        await message.answer("❌ Ошибка! Вы ввели число, введите <b>да</b> или <b>нет</b>", reply_markup=cancel_menu2())
    except TelegramBadRequest:
        await message.edit_text("❌ Ошибка! <b><u>Вы уже нажали эту кнопку взаимодействия!</u></b>", reply_markup=main_keyboard())
           
# =====GLOBAL SEARCH=====
@router.callback_query(F.data == "search_all")
async def search_all(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✍️ Введите ключевое слово для поиска <b>по всем данным</b>:",
        reply_markup=cancel_menu()
    )
    await state.set_state(All_State.waiting_all_search)
    await callback.answer()

@router.message(All_State.waiting_all_search, F.text)
async def search_all_result(message: types.Message, state: FSMContext):
    keyword = message.text
    notes, files = all_search(message.from_user.id, keyword)
    if not notes and not files:
        await message.answer("❌ Ничего не найдено! <u>Проверьте вводимые данные</u>", reply_markup=cancel_menu2())
    else:
        text = f"🔍 <b>Результаты поиска:</b>\n\n"
        if notes:
            text += f"📝 <b>Заметки ({len(notes)}):</b>\n"
            for note in notes:
                text += f"`#{note[0]}` {note[3]} — {note[2]}\n"
        if files:
            text += f"\n📎 <b>Файлы ({len(files)}):</b>\n"
            for file in files:
                text += f"`{file[5]}` — {file[4]} ({file[6]})\n"
        await message.answer(text, reply_markup=cancel_menu2())
    await state.clear()
    
# =====STATS=====
# ===== STATS =====
@router.callback_query(F.data == "stats")
async def stats(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    notes = get_note(user_id)
    files = get_file_user_id(user_id)
    
    await callback.message.edit_text(
        f"📊 <b>Статистика вашего хранилища:</b>\n\n"
        f"📝 <b>Заметок</b>: {len(notes)}\n"
        f"📎 <b>Файлов</b>: {len(files)}\n"
        f"📦 <b>Всего записей</b>: {len(notes) + len(files)}",
        reply_markup=cancel_menu2(), parse_mode="HTML"
    )
    await callback.answer()
    
# ===== ABOUT DEVELOPER =====
@router.callback_query(F.data == "about_developer")
async def about_developer(callback: types.CallbackQuery):
    text = (
        "👋 <b>О разработчике</b>\n\n"
        "Меня зовут <b>DansDagger</b> (настоящее имя Даниил).\n"
        "Этот бот — мой учебный проект на <b>Aiogram</b>.\n\n"
        "🔹 <b>Технологии:</b>\n"
        "• Python 3.11+\n"
        "• Aiogram 3.x\n"
        "• SQLite\n"
        "• FSM (машина состояний)\n"
        "• HTML-форматирование\n\n"
        "🔗 <b>Контакты:</b>\n"
        "• GitHub: <a href='https://github.com/DansDUSK'>DansDUSK</a>\n"
        "• Telegram: <a href='https://t.me/daggerka'>@daggerka</a>\n\n"
        "😊 <b><u>Спасибо, что пользуешься ботом!</u></b>"
    )
    await callback.message.edit_text(text, reply_markup=cancel_menu2(), parse_mode="HTML")
    await callback.answer()