import os
import shutil
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Menu

# Define file categories
EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'videos': ['.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    'documents': ['.pdf', '.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'code': ['.py', '.java', '.c', '.cpp', '.js', '.html', '.css'],
    'installers': ['.exe', '.msi', '.apk', '.dmg']
}

# Functions for file organization and management
def organize_by_type(directory):
    """Organize files in the directory by their type."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file)[1].lower()
            folder_name = None

            for category, ext_list in EXTENSIONS.items():
                if file_ext in ext_list:
                    folder_name = category
                    break

            if folder_name:
                target_folder = os.path.join(directory, folder_name)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                shutil.move(file_path, os.path.join(target_folder, file))

def organize_by_date(directory):
    """Organize files in the directory by their creation date."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            creation_time = os.path.getctime(file_path)
            date_folder = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
            target_folder = os.path.join(directory, date_folder)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            shutil.move(file_path, os.path.join(target_folder, file))

def organize_code_by_language(directory):
    """Organize code files by their programming language."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file)[1].lower()
            language_folder = file_ext.lstrip('.')
            if language_folder:
                target_folder = os.path.join(directory, language_folder)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                shutil.move(file_path, os.path.join(target_folder, file))

def preview_organization(directory):
    """Preview the organization structure before applying."""
    preview = {}
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file)[1].lower()
            folder_name = None

            for category, ext_list in EXTENSIONS.items():
                if file_ext in ext_list:
                    folder_name = category
                    break

            if folder_name:
                if folder_name not in preview:
                    preview[folder_name] = []
                preview[folder_name].append(file)
    return preview

def delete_duplicates(directory):
    """Delete duplicate files."""
    seen = set()
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            if file in seen:
                os.remove(file_path)
            else:
                seen.add(file)

def backup_files(directory):
    """Backup files from the selected directory."""
    backup_folder = filedialog.askdirectory(title="Select Backup Folder")
    if not backup_folder:
        messagebox.showerror("Error", "No backup folder selected.")
        return

    try:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                shutil.copy(file_path, os.path.join(backup_folder, file))
        messagebox.showinfo("Success", "Files have been backed up successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while backing up files: {e}")

def restore_files(directory):
    """Restore files from the backup folder."""
    backup_folder = filedialog.askdirectory(title="Select Backup Folder to Restore From")
    if not backup_folder:
        messagebox.showerror("Error", "No backup folder selected.")
        return

    try:
        for file in os.listdir(backup_folder):
            backup_file_path = os.path.join(backup_folder, file)
            if os.path.isfile(backup_file_path):
                shutil.copy(backup_file_path, directory)
        messagebox.showinfo("Success", "Files have been restored successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while restoring files: {e}")

def search_and_filter(directory, search_query, filter_category):
    """Search and filter files by name or category."""
    filtered_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file)[1].lower()
            # Search by name
            if search_query.lower() in file.lower():
                if filter_category == "all" or file_ext in EXTENSIONS.get(filter_category, []):
                    filtered_files.append(file)
    return filtered_files

def search_in_directory(directory, search_query, filter_category):
    """Search files in the selected directory or the entire system if no directory is selected."""
    if directory:
        return search_and_filter(directory, search_query, filter_category)
    else:
        all_files = []
        for root_dir, _, files in os.walk("/"):  # Start from the root directory for full system search
            for file in files:
                file_path = os.path.join(root_dir, file)
                if os.path.isfile(file_path):
                    file_ext = os.path.splitext(file)[1].lower()
                    # Search by name
                    if search_query.lower() in file.lower():
                        if filter_category == "all" or file_ext in EXTENSIONS.get(filter_category, []):
                            all_files.append(file_path)
        return all_files

def main():
    def select_directory_for_search():
        nonlocal search_directory
        search_directory = filedialog.askdirectory(title="Select Directory for Search")

    def select_directory():
        directory = filedialog.askdirectory()
        if not directory:
            messagebox.showerror("Error", "No directory selected.")
            return

        # Preview organization
        preview = preview_organization(directory)
        preview_message = "Preview of file organization:\n\n"
        for category, files in preview.items():
            preview_message += f"{category.capitalize()} ({len(files)} files):\n"
            preview_message += "\n".join(files[:5]) + ("\n...\n" if len(files) > 5 else "\n")

        if not messagebox.askyesno("Preview", preview_message + "\nDo you want to proceed?"):
            return

        # Organize files
        organize_by_type(directory)
        messagebox.showinfo("Success", "Files have been organized by type.")

        if messagebox.askyesno("Organize by Date", "Do you want to further organize files by date?"):
            for category in ['images', 'videos', 'audio', 'installers']:
                subfolder = os.path.join(directory, category)
                if os.path.exists(subfolder):
                    organize_by_date(subfolder)
            messagebox.showinfo("Success", "Files have been further organized by date.")

        if messagebox.askyesno("Organize Code", "Do you want to further organize code files by language?"):
            code_folder = os.path.join(directory, 'code')
            if os.path.exists(code_folder):
                organize_code_by_language(code_folder)
            messagebox.showinfo("Success", "Code files have been further organized by language.")

    def set_light_theme():
        root.style.theme_use('flatly')

    def set_dark_theme():
        root.style.theme_use('darkly')

    def set_language_english():
        language_var.set("EN")
        root.title("File Organizer Pro")
        select_button.config(text="Select Directory")
        delete_button.config(text="Delete Duplicates")
        time_button.config(text="Organize by Time")
        themes_button.config(text="Light Theme")
        languages_button.config(text="English")
        footer_label.config(text="Created by Shayan")

    def set_language_persian():
        language_var.set("FA")
        root.title("نرم‌افزار مرتب‌سازی فایل")
        select_button.config(text="انتخاب پوشه")
        delete_button.config(text="حذف فایل‌های تکراری")
        time_button.config(text="مرتب‌سازی بر اساس زمان")
        themes_button.config(text="تم روشن")
        languages_button.config(text="فارسی")
        footer_label.config(text="ساخته شده توسط شایان")

    # Create the main GUI window
    root = ttk.Window(themename="darkly")  # Set default theme to Dark
    root.title("File Organizer Pro")
    root.geometry("600x600")

    # Language selection variable
    language_var = ttk.StringVar(value="EN")
    search_directory = None

    # Create Menu using tkinter.Menu
    menu_bar = Menu(root)

    # Add themes menu
    themes_menu = Menu(menu_bar, tearoff=0)
    themes_menu.add_command(label="Light Theme", command=set_light_theme)
    themes_menu.add_command(label="Dark Theme", command=set_dark_theme)
    menu_bar.add_cascade(label="Themes", menu=themes_menu)

    # Add languages menu
    languages_menu = Menu(menu_bar, tearoff=0)
    languages_menu.add_command(label="English", command=set_language_english)
    languages_menu.add_command(label="فارسی", command=set_language_persian)
    menu_bar.add_cascade(label="Languages", menu=languages_menu)

    # Add tools menu without delete duplicates and organize by time
    tools_menu = Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label="Backup Files", command=lambda: backup_files(filedialog.askdirectory()))
    tools_menu.add_command(label="Restore Files", command=lambda: restore_files(filedialog.askdirectory()))
    menu_bar.add_cascade(label="Tools", menu=tools_menu)

    # Add the menu to the root window
    root.config(menu=menu_bar)

    # Add a stylish title label
    title_label = ttk.Label(root, text="File Organizer Pro", font=("Helvetica", 20, "bold"), anchor=CENTER)
    title_label.pack(pady=20)

    # Search bar
    search_label = ttk.Label(root, text="Search File:")
    search_label.pack(pady=5)
    search_entry = ttk.Entry(root, width=40)
    search_entry.pack(pady=5)

    filter_label = ttk.Label(root, text="Filter by Category:")
    filter_label.pack(pady=5)
    filter_combobox = ttk.Combobox(root, values=["All", "Images", "Videos", "Audio", "Documents", "Archives", "Code", "Installers"], width=38)
    filter_combobox.set("All")
    filter_combobox.pack(pady=5)

    directory_button = ttk.Button(root, text="Select Directory for Search", command=select_directory_for_search)
    directory_button.pack(pady=10)

    def search_files():
        search_query = search_entry.get()
        filter_category = filter_combobox.get().lower()
        filtered_files = search_in_directory(search_directory, search_query, filter_category)
        messagebox.showinfo("Search Results", f"Found {len(filtered_files)} matching files:\n\n" + "\n".join(filtered_files))

    search_button = ttk.Button(root, text="Search Files", command=search_files, bootstyle=(INFO, OUTLINE), width=20)
    search_button.pack(pady=10)

    # Add a button to select a directory
    select_button = ttk.Button(root, text="Select Directory", command=select_directory, bootstyle=(SUCCESS, OUTLINE),
                               width=25)
    select_button.pack(pady=20)

    # Add a button for deleting duplicates
    delete_button = ttk.Button(root, text="Delete Duplicates",
                               command=lambda: delete_duplicates(filedialog.askdirectory()),
                               bootstyle=(WARNING, OUTLINE), width=25)
    delete_button.pack(pady=20)

    # Add a button for sorting by date
    time_button = ttk.Button(root, text="Organize by Time",
                             command=lambda: organize_by_date(filedialog.askdirectory()), bootstyle=(INFO, OUTLINE),
                             width=25)
    time_button.pack(pady=20)

    # Add a footer label
    footer_label = ttk.Label(root, text="Created by Shayan", font=("Helvetica", 10), anchor=CENTER)
    footer_label.pack(side=BOTTOM, pady=10)

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
