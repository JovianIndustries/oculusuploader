from tkinter import *
import tkinter as ttk
from tkinter import filedialog
import webbrowser
import os
from configparser import ConfigParser
from sys import platform
from enum import Enum

URL_UTIL_WIN32 = "https://www.oculus.com/download_app/?id=1076686279105243&access_token=OC%7C1076686279105243%7C"
URL_UTIL_OSX = "https://www.oculus.com/download_app/?id=1462426033810370&access_token=OC%7C1462426033810370%7C"
LABEL_FONT = "Adobe Gothic Std"
SETTINGS = "SETTINGS"

class Platform(Enum):
    WIN32 = 1,
    LINUX = 2,
    OSX = 3

tkvar = None
sections = {}
current_section = "None"
current_platform = Platform.WIN32
config = ConfigParser()
root = Tk(className=" Upload Interface for Oculus Quest (apk)")

def set_platform():
    global current_platform
    if platform == "linux" or platform == "linux2":
        current_platform = Platform.LINUX
    elif platform == "darwin":
        current_platform = Platform.OSX
    elif platform == "win32":
        current_platform = Platform.WIN32
    print(f"Platform detected: {platform}")


def draw_main_window():
    global apk_entry, cat_entry, util_entry, channel_entry, appid_entry, appsecret_entry, root, tkvar, frame, popupMenu
    root.config(padx=20, pady=20)
    root.resizable(False, False)
    frame = Frame()

    #Dropdown
    tkvar = StringVar()
    tkvar.set(current_section)
    drop_down = Label(text="Select an app:", font=(LABEL_FONT, 12))
    drop_down.grid(column=0, row=1, sticky=E)
    popupMenu = OptionMenu(root, tkvar, current_section, *sections)
    popupMenu.config(width="20")
    popupMenu.grid(column=1, row=1, columnspan=1, pady=0, padx=15, sticky=W)
    tkvar.trace('w', change_dropdown)

    #Create app
    cat_entry = Entry(width=10)
    cat_entry.grid(column=4, row=1, columnspan=1, pady=5, padx=8, sticky=E)
    cat_button = Button(text="Create App", command=create_category)
    cat_button.grid(column=5, row=1, columnspan=1, padx=3, pady=15, sticky=NW)

    #APK Path
    apk_label = Label(text="APK Path:", font=(LABEL_FONT, 12))
    apk_label.grid(column=0, row=2, sticky=E)
    apk_entry = Entry(width=50)
    apk_entry.grid(column=1, row=2, columnspan=3, pady=5, padx=15, sticky=W)
    upload_button = Button(text="Browse", command=browse_apk)
    upload_button.grid(column=4, row=2, columnspan=1, padx=3, sticky=W)

    #Channel
    channel_label = Label(text="Channel:", font=(LABEL_FONT,12))
    channel_label.grid(column=0, row=3, sticky=E)
    channel_entry = Entry(width=40)
    channel_entry.grid(column=1, row=3, columnspan=3, pady=5, padx=15, sticky=W)

    #App Id
    appid_label = Label(text="App. Id:", font=(LABEL_FONT, 12))
    appid_label.grid(column=0, row=4, sticky=E)
    appid_entry = Entry(width=40)
    appid_entry.grid(column=1, row=4, columnspan=3, pady=5, padx=15, sticky=W)

    #App Secret
    appSecret_label = Label(text="App. Secret:", font=(LABEL_FONT, 12))
    appSecret_label.grid(column=0, row=5, sticky=E)
    appsecret_entry = Entry(width=40)
    appsecret_entry.grid(column=1, row=5, columnspan=3, pady=5, padx=15, sticky=W)
    appsecret_entry.config(show="*")

    #Ovr Util Selector
    util_label = Label(text="Ovr Util Path:", font=(LABEL_FONT, 12))
    util_label.grid(column=0, row=6, sticky=E)
    util_entry = Entry(width=50)
    util_entry.grid(column=1, row=6, columnspan=3, pady=5, padx=15, sticky=W)
    upload_button = Button(text="Browse", command=browse_util)
    upload_button.grid(column=4, row=6, columnspan=1,  padx=3, sticky=W)
    add_info_button = Button(text="Download Util", command=download_apk_util)
    add_info_button.grid(column=5, row=6, columnspan=1, padx=2, sticky=W)

    #Upload APK
    upload_button = Button(text="Upload", width=38, padx=3, command=upload_apk)
    upload_button.grid(column=1, row=8, pady=15, columnspan=1, sticky=W)

    #Save current info
    add_info_button = Button(text="Save Info", width=10, padx=3, command=save)
    add_info_button.grid(column=5, row=8, pady=15, columnspan=1, sticky=W)

    #help
    help_button = Button(text="Help", width=10, padx=3, pady=3, command=help)
    help_button.grid(column=5, row=9, pady=15, columnspan=1, sticky=W)

def change_dropdown(*args):
    global tkvar, current_section
    save()
    clear()
    current_section = tkvar.get()
    save_settings(current_section)
    load()

def save_settings(section):
    if not (config.has_section(SETTINGS)):
        config.add_section(SETTINGS)
    config.set(SETTINGS, "last_section", section)
    with open ("config.ini", "w") as configfile:
        config.write(configfile)

def load_settings():
    config.read("config.ini")
    if not (config.has_section(SETTINGS)):
        save_settings(current_section)
    last_section = config.get(SETTINGS, "last_section")
    all_sections = config.sections()
    return all_sections, last_section


def create_config(section, app_secret, app_id, channel, filename, util_path):
    if not (config.has_section(section)):
        config.add_section(section)
    config.set(section, "app_id", app_id)
    config.set(section, "app_secret", app_secret)
    config.set(section, "channel", channel)
    config.set(section, "util_path", util_path)
    with open("config.ini", "w") as configfile:
        config.write(configfile)


def read_config(section):
    config.read("config.ini")
    if not (config.has_section(section)):
        create_config(section, "", "", "", "", "")
    app_id = config.get(section, "app_id")
    app_secret = config.get(section, "app_secret")
    channel = config.get(section, "channel")
    util_path = config.get(section, "util_path")
    return app_id, app_secret, channel, util_path

def download_apk_util():
    if (current_platform == Platform.WIN32):
        webbrowser.open(URL_UTIL_WIN32)
    else:
        webbrowser.open(URL_UTIL_OSX)

def browse_apk():
    global apk_entry
    filename = filedialog.askopenfilename(
        initialdir="", title="Select a File", filetypes=(("apk files", "*.apk"), ("all files", "*.*")))
    apk_entry.delete(0, "end")
    apk_entry.insert(0, filename)
    save()

def browse_util():
    global util_entry
    if current_platform == Platform.WIN32:
        util_path = filedialog.askopenfilename(
            initialdir="", title="Select a File", filetypes=(("oculus-platform-util.exe", "*.exe"), ("all files", "*.*")))
    else:
        util_path = filedialog.askopenfilename(
            initialdir="", title="Select a File")
    util_entry.delete(0, "end")
    util_entry.insert(0, util_path)
    save()

def upload_apk():
    global channel_entry, appid_entry, appsecret_entry, apk_entry, util_entry
    if appsecret_entry.get() == "":
        print("ERROR: There is no App Secret set. You can find the App Secret in the Oculus Dashboard, select you app and select to Manage followed by API")
    if appid_entry.get() == "":
        print("ERROR: There is no App. Id set. You can find the app id in the Oculus Dashboard by selecting you app")
    if channel_entry.get() == "":
        print("ERROR: There is no Channel set for upload")
    if not os.path.isfile(util_entry.get()):
        print("ERROR: Path for the oculus-platform-util was not set. First select Download Util to download the latest oculus-platform-util executable and after that Browse to select the path to it")
        return
    if not os.path.isfile(apk_entry.get()):
        print("ERROR: There is no apk file path provided")
        return
    
    save()
    print (f"Will upload {os.path.basename(util_entry.get())}")
    if not current_platform == Platform.WIN32:
        os.system(f"chmod +x {util_entry.get()}")
    os.system(f"{util_entry.get()} upload-quest-build --app_id {appid_entry.get()} --app_secret {appsecret_entry.get()} --channel {channel_entry.get()} --apk {apk_entry.get()}")

def create_category():
    global cat_entry, current_section, tkvar, sections
    sct = cat_entry.get()
    if sct == "":
        return
    if sct in sections:
        print("There is always an app with that name")
        return
    cat_entry.delete(0, "end")
    clear()
    current_section = sct
    tkvar.set(current_section)
    sections.append(current_section)
    update_option_menu()
    save()

def update_option_menu():
    global popupMenu, tkvar
    menu = popupMenu["menu"]
    menu.delete(0, "end")
    for string in sections:
        menu.add_command(label=string, command=lambda value=string: tkvar.set(value))

def save():
    global current_section, channel_entry, appid_entry, appsecret_entry, apk_entry, util_entry
    save_settings(current_section)
    create_config(current_section, appsecret_entry.get(), appid_entry.get(), channel_entry.get(), apk_entry.get(), util_entry.get())

def load():
    global current_section, sections, channel_entry, appid_entry, appsecret_entry, apk_entry, util_entry, tkvar
    if os.path.isfile('config.ini'):
        clear()
        app_id, app_secret, channel, util_path = read_config(current_section)
        channel_entry.insert(0, channel)
        appid_entry.insert(0, app_id)
        appsecret_entry.insert(0, app_secret)
        util_entry.insert(0, util_path)
        tkvar.set(current_section)
        update_option_menu()
    else:
        save()

def clear():
    global channel_entry, appid_entry, appsecret_entry, apk_entry, util_entry
    channel_entry.delete(0, "end")
    appid_entry.delete(0, "end")
    appsecret_entry.delete(0, "end")
    util_entry.delete(0, "end")
    apk_entry.delete(0, "end")

def populate_dropdown():
    global sections, current_section
    sections, current_section = load_settings()
    if SETTINGS in sections:
        sections.remove(SETTINGS)
    if "None" in sections:
        sections.remove("None")

def help():
    help_window = Toplevel()
    help_window.title = "Help"
    l = Label(help_window, text="Instructions on how to set up this tool", font=(
        LABEL_FONT, 12))
    l.grid(row=0, column=0, padx = 25)
    t = Text(help_window, height=15, width=70)
    t.grid(row=1, column=0, padx=10, pady=10)
    
    TEXT = " 1. In the top left, write the name of you app and press Create App \n 2. You app is now selected in the top drop down menu. Add another app if you wish or need to \n 3. If you have not downloded the ovr-upload-tool, click on Download   Util and save the tool in a location that you can remeber \n 4. On the Ovr Util Path section click Browse and select the tool you  have just downloaded \n 5. Go to the Oculus Dashboard and retrieve the rest of the informa-   tion from Management/API (Channel, AppId, secret) \n 6. Don't forget to hit Save Info, alhough the program will automati-   cally save as well when you Upload \n 7. From the APK Path click and Browse the path to the apk you want to upload. \n 8. Click Upload and profit! Watch the console window for errors."
    t.insert(END, TEXT)
    t.config(state=DISABLED)

def main():
    global root
    set_platform()
    populate_dropdown()
    draw_main_window()
    load()
    root.mainloop() # meh, no other way...

if __name__ == "__main__":
    main()
