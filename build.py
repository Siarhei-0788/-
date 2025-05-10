import PyInstaller.__main__
import os
import shutil

# Очистка предыдущих сборок
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Пути к вашим файлам
script_path = 'run.py'
icon_path = 'hotel.ico'  # Убедитесь, что у вас есть файл иконки
database_path = 'hotel.db'
additional_files = [(database_path, '.')]

# Сборка EXE
PyInstaller.__main__.run([
    script_path,
    '--onefile',            # Создать один исполняемый файл
    '--windowed',           # Для GUI приложений (без консоли)
    f'--icon={icon_path}',  # Иконка приложения
    '--add-data', f'{database_path};.',  # Включить базу данных
    '--name=HotelAdminApp', # Имя исполняемого файла
    '--clean'               # Очистка временных файлов
])