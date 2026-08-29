from aiogram.fsm.state import State, StatesGroup

class Note_State(StatesGroup):
    waiting_text = State()
    waiting_delete = State()
    waiting_search = State()

class File_State(StatesGroup):
    waiting_description = State()
    waiting_file = State()
    waiting_delete_id = State()
    waiting_search_file = State()
    waiting_search_unique_code = State()
    
class All_State(StatesGroup):
    waiting_user_answer = State()
    waiting_all_search = State()