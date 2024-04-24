import customtkinter as CTk
from tkinter import messagebox
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard,VkKeyboardColor




CTk.set_appearance_mode('system') #Устанавливает цвет темы приложения
CTk.set_default_color_theme('green') #Устанавливает цвет виджетов



class App(CTk.CTk):
    def __init__(self):
        super().__init__()



        # Настройки интерфейса
        self.title('Black Heather')
        self.geometry('1100x568+80+50')
        self.resizable(False, False)


        # Настройка бокового (основного) фрейма
        self.main_frame = CTk.CTkFrame(master=self, width=200, height=580)
        self.main_frame.place(x=0, y=0)


        # # Настройки кнопки 'Домашняя страница'
        # self.btn_home = CTk.CTkButton(master=self.main_frame, fg_color="transparent", text_color=("gray10", "gray90"),
        #                               hover_color=("gray70", "gray30"), text='Домашняя страница', width=200, height=40,
        #                               command=self.home_event)
        # self.btn_home.place(x=0, y=75)


if __name__ == "__main__":
    app = App()
    app.mainloop()