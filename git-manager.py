import os
import subprocess
from datetime import datetime
import urllib.request
import msvcrt

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env={**os.environ, 'LC_ALL': 'C.UTF-8'}
        )
        return (result.stdout + result.stderr).strip()
    except Exception as e:
        return f"[ERROR] {e}"

def display_menu(options, title, footer, selected):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Результат выполнения команды:")
        print("-" * 40)
        print(footer)
        print("-" * 40 + "\n")

        print(title)
        for i, option in enumerate(options):
            if i == selected:
                print(f"> {option} <")
            else:
                print(f"  {option}")

        key = msvcrt.getch()
        if key == b'\xe0':
            arrow = msvcrt.getch()
            if arrow == b'H':
                selected = (selected - 1) % len(options)
            elif arrow == b'P':
                selected = (selected + 1) % len(options)
        elif key == b'\r':
            return selected
def init_and_config():
    footer = ""
    selected = 0
    while True:
        options = [
            "Инициализировать репозиторий",
            "Установить имя пользователя",
            "Установить email пользователя",
            "Показать текущую конфигурацию",
            "Вернуться в главное меню"
        ]
        selected = display_menu(options, "\nИнициализация и конфигурация:", footer, selected)
        if selected == 0:
            footer = run_command("git init")
        elif selected == 1:
            name = input("Введите имя пользователя: ").strip()
            footer = run_command(f"git config user.name \"{name}\"")
        elif selected == 2:
            email = input("Введите email пользователя: ").strip()
            footer = run_command(f"git config user.email \"{email}\"")
        elif selected == 3:
            footer = run_command("git config --list")
        elif selected == 4:
            return footer
def run_and_log_add(command):
    output = run_command(command)
    added_files = run_command("git diff --cached --name-only")
    return f"{output}\n\n[LOG] Список добавленных файлов:\n{added_files}"

def basic_commands():
    footer = ""
    selected = 0
    while True:
        options = [
            "Статус репозитория",
            "Добавить файлы",
            "Коммит изменений",
            "История коммитов",
            "Просмотр закоммиченных файлов",
            "Удалить файлы из репозитория",
            "Авто коммит всех файлов",
            "Откат к коммиту",
            "Просмотр изменений",
            "Сравнение изменений между коммитами",
            "Удалить файл из последнего коммита",
            "Удалить файлы из индекса",
            "Вернуться в главное меню"
        ]

        selected = display_menu(options, "\nРабота с файлами и коммитами:", footer, selected)

        if selected == 0:
            footer = run_command("git status")
        elif selected == 1:
            files = input("Введите файлы или '.' для всех: ").strip()
            if not files:
                continue
            footer = run_and_log_add(f"git add {files}")
        elif selected == 2:
            msg = input("Введите сообщение коммита: ").strip()
            if not msg:
                continue
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            footer = run_command(f'git commit -m "{msg} ({ts})"')
        elif selected == 3:
            footer = run_command("git log --oneline --graph")
        elif selected == 4:
            footer = run_command("git ls-tree -r HEAD --name-only")
        elif selected == 5:
            files = input("Введите файлы (через запятую): ").strip()
            if not files:
                continue
            file_list = [f.strip() for f in files.split(',')]
            footer = ""
            for file in file_list:
                check = run_command(f"git ls-files --error-unmatch {file}")
                if not check.startswith("[ERROR]"):
                    footer += run_command(f"git rm --cached {file}") + "\n"
                else:
                    footer += f"[ERROR] {file} не отслеживается.\n"
        elif selected == 6:
            footer = run_command("git add .")
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            footer += "\n" + run_command(f'git commit -m "Auto commit ({ts})"')
        elif selected == 7:
            commits = run_command("git log --oneline").splitlines()
            for i, line in enumerate(commits):
                print(f"{i}: {line}")
            idx = input("Номер коммита: ").strip()
            if not idx.isdigit():
                continue
            chash = commits[int(idx)].split()[0]
            confirm = input(f"Откатиться к {chash}? (yes/no): ").lower()
            if confirm == "yes":
                footer = run_command(f"git reset --hard {chash}")
            else:
                footer = "Откат отменён."
        elif selected == 8:
            footer = run_command("git diff")
        elif selected == 9:
            c1 = input("Хэш первого коммита: ").strip()
            c2 = input("Хэш второго: ").strip()
            if not c1 or not c2:
                continue
            footer = run_command(f"git diff {c1} {c2}")
        elif selected == 10:
            file = input("Файл: ").strip()
            if not file:
                continue
            footer = run_command(f"git reset HEAD^ -- {file}")
            footer += "\n" + run_command("git commit --amend --no-edit")
        elif selected == 11:
            files = input("Файлы (через запятую): ").strip()
            if not files:
                continue
            for f in files.split(','):
                footer += run_command(f"git reset {f.strip()}") + "\n"
        elif selected == 12:
            return footer
def branch_management():
    footer = ""
    selected = 0
    while True:
        options = [
            "Просмотр веток",
            "Создать ветку",
            "Переключиться на ветку",
            "Удалить ветку",
            "Переименовать ветку",
            "Принудительно удалить ветку",
            "Слить ветку",
            "Отменить слияние",
            "Удалить привязку к origin",
            "Создать ветку от коммита",
            "Очистить неактуальные удалённые ветки",
            "Сравнение веток (diff)",
            "Лог разницы между ветками",
            "Вернуться в главное меню"
        ]
        selected = display_menu(options, "\nУправление ветками:", footer, selected)

        if selected == 0:
            footer = run_command("git branch -vv")
        elif selected == 1:
            name = input("Имя новой ветки: ").strip()
            footer = run_command(f"git branch {name}")
        elif selected == 2:
            name = input("Имя ветки: ").strip()
            footer = run_command(f"git checkout {name}")
        elif selected == 3:
            name = input("Удаляемая ветка: ").strip()
            footer = run_command(f"git branch -d {name}")
        elif selected == 4:
            old = input("Текущее имя: ").strip()
            new = input("Новое имя: ").strip()
            footer = run_command(f"git branch -m {old} {new}")
        elif selected == 5:
            name = input("Ветка для принудительного удаления: ").strip()
            footer = run_command(f"git branch -D {name}")
        elif selected == 6:
            name = input("Ветка для слияния: ").strip()
            footer = run_command(f"git merge {name}")
        elif selected == 7:
            footer = run_command("git merge --abort")
        elif selected == 8:
            footer = run_command("git branch --unset-upstream")
        elif selected == 9:
            chash = input("Хэш коммита: ").strip()
            name = input("Имя новой ветки: ").strip()
            footer = run_command(f"git checkout -b {name} {chash}")
        elif selected == 10:
            footer = run_command("git remote prune origin")
        elif selected == 11:
            b1 = input("Ветка 1: ").strip()
            b2 = input("Ветка 2: ").strip()
            footer = run_command(f"git diff {b1}..{b2}")
        elif selected == 12:
            b1 = input("Ветка 1: ").strip()
            b2 = input("Ветка 2: ").strip()
            footer = run_command(f"git log {b1}..{b2}")
        elif selected == 13:
            return footer
def gitignore_management():
    footer = ""
    selected = 0
    while True:
        options = [
            "Просмотр .gitignore",
            "Добавить в .gitignore",
            "Удалить из .gitignore",
            "Применить шаблон Python",
            "Вернуться в главное меню"
        ]
        selected = display_menu(options, "\nУправление .gitignore:", footer, selected)

        if selected == 0:
            if os.path.exists(".gitignore"):
                with open(".gitignore", "r", encoding="utf-8") as f:
                    footer = f.read()
            else:
                footer = ".gitignore не найден."
        elif selected == 1:
            entries = input("Введите записи (через запятую): ").strip()
            with open(".gitignore", "a", encoding="utf-8") as f:
                for entry in entries.split(','):
                    f.write(entry.strip() + "\n")
            footer = "Записи добавлены."
        elif selected == 2:
            target = input("Запись для удаления: ").strip()
            if not os.path.exists(".gitignore"):
                footer = ".gitignore не найден."
                continue
            with open(".gitignore", "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(".gitignore", "w", encoding="utf-8") as f:
                for line in lines:
                    if line.strip() != target:
                        f.write(line)
            footer = f"Удалена запись: {target}"
        elif selected == 3:
            template = [
                "__pycache__/",
                "*.py[cod]",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                ".Python",
                "env/",
                "venv/",
                ".env",
                ".venv",
                "build/",
                "develop-eggs/",
                "dist/",
                "downloads/",
                "eggs/",
                "*.egg-info/",
                "*.egg",
                ".mypy_cache/",
                ".pytest_cache/",
                ".idea/",
                ".vscode/",
                "*.log"
            ]
            with open(".gitignore", "w", encoding="utf-8") as f:
                f.write("\n".join(template) + "\n")
            footer = "Базовый шаблон Python применён."
        elif selected == 4:
            return footer

def remote_management():
    footer = ""
    selected = 0
    while True:
        options = [
            "Просмотр удалённых",
            "Добавить удалённый",
            "Удалить удалённый",
            "Получить изменения (pull)",
            "Отправить изменения (push)",
            "Ветки на удалённом GIT",
            "Вернуться в главное меню"
        ]
        selected = display_menu(options, "\nУдалённые репозитории:", footer, selected)

        if selected == 0:
            footer = run_command("git remote -v")

        elif selected == 1:
            name = input("Введите имя (например: origin): ").strip()
            url = input("Введите URL (например: https://github.com/user/repo.git): ").strip()
            footer = run_command(f"git remote add {name} {url}")

        elif selected == 2:
            name = input("Имя удалённого для удаления: ").strip()
            footer = run_command(f"git remote remove {name}")

        elif selected == 3:
            branch = run_command("git branch --show-current").strip()
            if not branch:
                branch = input("Введите имя ветки (по умолчанию main): ").strip() or "main"
            footer = run_command(f"git pull origin {branch} --allow-unrelated-histories")

        elif selected == 4:
            branch = run_command("git branch --show-current").strip()
            if not branch:
                branch = input("Введите имя ветки (по умолчанию main): ").strip() or "main"
            footer = run_command(f"git push origin {branch}")

        elif selected == 5:
            footer = run_command("git ls-remote --heads origin")

        elif selected == 6:
            return footer


def browse_and_download_remote_file():
    repo_url = input("Введите HTTPS-ссылку на репозиторий GitHub (например, https://github.com/user/repo): ").strip()
    branch = input("Введите ветку (по умолчанию main): ").strip() or "main"
    file_path = input("Введите путь к файлу (например, path/to/file.py): ").strip()

    try:
        user_repo = repo_url.replace("https://github.com/", "")
        raw_url = f"https://raw.githubusercontent.com/{user_repo}/{branch}/{file_path}"
        print(f"Скачивание: {raw_url}")

        with urllib.request.urlopen(raw_url) as response:
            if response.status == 200:
                with open(os.path.basename(file_path), "wb") as f:
                    f.write(response.read())
                return f"✅ Файл '{file_path}' успешно скачан."
            else:
                return f"[ERROR] HTTP {response.status}"
    except Exception as e:
        return f"[EXCEPTION] {e}"
def clear_repository():
    confirm = input("Очистить весь git-репозиторий? (yes/no): ").strip().lower()
    if confirm == "yes":
        script_name = os.path.basename(__file__)
        with open(".gitignore", "a", encoding="utf-8") as f:
            f.write(f"{script_name}\n")
        footer = f"{script_name} добавлен в .gitignore\n"
        footer += run_command("git rm -r --cached .")
        footer += "\nРабочие файлы оставлены."
        footer += "\n" + run_command("git reset --hard")
        footer += "\nИстория Git удалена."
        return footer
    else:
        return "Операция отменена."
def main_menu():
    footer = ""
    selected = 0
    while True:
        options = [
            "Инициализация и конфигурация",
            "Работа с файлами и коммитами",
            "Управление ветками",
            "Работа с удалёнными репозиториями",
            "Управление .gitignore",
            "Скачать файл из удалённого репозитория",
            "Очистка репозитория",
            "Выход"
        ]
        selected = display_menu(options, "\nGit Management Menu:", footer, selected)

        if selected == 0:
            footer = init_and_config()
        elif selected == 1:
            footer = basic_commands()
        elif selected == 2:
            footer = branch_management()
        elif selected == 3:
            footer = remote_management()
        elif selected == 4:
            footer = gitignore_management()
        elif selected == 5:
            footer = browse_and_download_remote_file()
        elif selected == 6:
            footer = clear_repository()
        elif selected == 7:
            print("Выход.")
            break

if __name__ == "__main__":
    main_menu()

