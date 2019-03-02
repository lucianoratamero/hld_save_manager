import keyboard
import base64
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from os.path import expanduser
from shutil import copy, SameFileError
from pathlib import Path


class PopupWindow(object):

    def __init__(self, root, text):
        self.top = tk.Toplevel(root)
        self.label = tk.Label(self.top, text=text)
        self.label.pack()
        self.entry = tk.Entry(self.top)
        self.entry.pack()
        self.button = tk.Button(self.top, text='Ok', command=self.cleanup)
        self.button.pack()

    def cleanup(self):
        self.value = self.entry.get()
        self.top.destroy()


class Application(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.create_widgets()

        home_folder = expanduser("~")
        self.base_save_folder = Path(f"{home_folder}\\AppData\\Local\\HyperLightDrifter")
        self.manager_save_folder = Path(f"{home_folder}\\hld_save_manager\\saves\\")

        self.setup_dirs_and_configs()

        keyboard.add_hotkey('ctrl+shift+z', self.load_save_state, args=["0"])
        keyboard.add_hotkey('ctrl+shift+x', self.load_save_state, args=["1"])
        keyboard.add_hotkey('ctrl+shift+c', self.load_save_state, args=["2"])
        keyboard.add_hotkey('ctrl+shift+v', self.load_save_state, args=["3"])

        self.update_configs_display()

    def setup_dirs_and_configs(self):
        if not os.path.exists(self.manager_save_folder):
            os.makedirs(self.manager_save_folder)
        try:
            with open(Path(f'{self.manager_save_folder}\\config.json'), 'r') as configs:
                self.configs = json.loads(configs.read())
                messagebox.showinfo("Loaded successfully", "Previous binds successfully loaded")
        except FileNotFoundError:
            self.configs = {"bound_save_states": {}}

    def get_user_input(self, text):
        popup = PopupWindow(self.root, text)
        self.master.wait_window(popup.top)
        return popup.value

    def create_save_state(self):
        filename = filedialog.askopenfilename(
            initialdir=self.base_save_folder,
            title=f"Select file for save state",
            filetypes=(("HLD save file", "*.sav"),)
        )

        if filename:
            save_name = self.get_user_input("Name for the save state:")
            if save_name:
                save_filename = Path(f"{self.manager_save_folder}\\save state - {save_name}.sav")
                try:
                    copy(filename, save_filename)
                except SameFileError:
                    pass

    def set_save_state_file(self, save_state="0"):
        filename = filedialog.askopenfilename(
            initialdir=self.manager_save_folder,
            title=f"Select file for save slot {save_state}",
            filetypes=(("HLD save file", "*.sav"),)
        )
        self.configs['bound_save_states'][save_state] = filename

        self.update_configs_display()

    def load_save_state(self, save_state="0"):
        save_state_filename = self.configs['bound_save_states'].get(save_state)
        if save_state_filename:
            copy(save_state_filename, Path(f"{self.base_save_folder}/HyperLight_RecordOfTheDrifter_{save_state}.sav"))
        else:
            messagebox.showwarning('Error', f'No save state found for slot {save_state}')

    def on_closing(self):
        with open(Path(f'{self.manager_save_folder}\\config.json'), 'w+') as configs:
            configs.write(json.dumps(self.configs))
        self.root.destroy()

    def update_configs_display(self):
        if getattr(self, 'configs_display', None):
            self.configs_display.destroy()
        self.configs_display = tk.Text(self, width=60, wrap=tk.WORD)
        self.configs_display.insert(tk.INSERT, self.configs)
        self.configs_display.pack(side="top")

    def create_widgets(self):
        self.winfo_toplevel().title("HLD Save Manager")

        self.create_save_state_button = tk.Button(self)
        self.create_save_state_button["text"] = "Create save state from save"
        self.create_save_state_button["command"] = self.create_save_state
        self.create_save_state_button.pack(side="top")

        self.save_button_0 = tk.Button(self)
        self.save_button_0["text"] = "Set save for slot 0"
        self.save_button_0["command"] = lambda: self.set_save_state_file(save_state="0")
        self.save_button_0.pack(side="top")

        self.save_button_1 = tk.Button(self)
        self.save_button_1["text"] = "Set save for slot 1"
        self.save_button_1["command"] = lambda: self.set_save_state_file(save_state="1")
        self.save_button_1.pack(side="top")

        self.save_button_2 = tk.Button(self)
        self.save_button_2["text"] = "Set save for slot 2"
        self.save_button_2["command"] = lambda: self.set_save_state_file(save_state="2")
        self.save_button_2.pack(side="top")

        self.save_button_3 = tk.Button(self)
        self.save_button_3["text"] = "Set save for slot 3"
        self.save_button_3["command"] = lambda: self.set_save_state_file(save_state="3")
        self.save_button_3.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.on_closing)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(root=root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
