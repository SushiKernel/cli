import subprocess
from datetime import datetime, timezone
import threading
import sys
import pytz
from os import system
from time import sleep


def time_say():
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    utc_now = datetime.now(timezone.utc)
    brasilia_now = utc_now.astimezone(brasilia_tz)
    now = brasilia_now.strftime('%H:%M')
    print(f"⏱︎ {COLOR_RESET}Time: ", now)

    morning_start = "06:00"
    afternoon_start = "12:00"
    evening_start = "17:00"
    night_start = "20:00"

    if now >= night_start or now < morning_start:
        say = COLOR_RED + "Good Night!"
        return say
    elif afternoon_start <= now < evening_start:
        say = COLOR_YELLOW + "Good Afternoon"
        return say
    elif morning_start <= now < afternoon_start:
        say = COLOR_CYAN + "Good Morning!"
        return say
    else:
        say = COLOR_BOLD + "Good Evening!"
        return say


def clear():
    """Clear of the OutPut."""
    system("clear")


def define_colors():
    global COLOR_RESET, COLOR_PURPLE, COLOR_YELLOW, COLOR_GREEN, COLOR_RED, COLOR_CYAN, COLOR_BOLD, COLOR_UNDERLINE, COLOR_BLINK, COLOR_REVERSE, COLOR_HIDDEN, COLOR_BLACK, COLOR_BLUE, COLOR_WHITE
    COLOR_RESET = "\033[0m"       # Reset de cor
    COLOR_BOLD = "\033[1m"        # Negrito
    COLOR_UNDERLINE = "\033[4m"   # Sublinhado
    COLOR_BLINK = "\033[5m"       # Piscando
    COLOR_REVERSE = "\033[7m"     # Inverter cores
    COLOR_HIDDEN = "\033[8m"      # Ocultar texto
    COLOR_BLACK = "\033[30m"      # Preto
    COLOR_RED = "\033[31m"        # Vermelho
    COLOR_GREEN = "\033[32m"      # Verde
    COLOR_YELLOW = "\033[33m"     # Amarelo
    COLOR_BLUE = "\033[34m"       # Azul
    COLOR_PURPLE = "\033[35m"     # Roxo
    COLOR_CYAN = "\033[36m"       # Ciano
    COLOR_WHITE = "\033[37m"      # Branco


def menu():
    clear()
    define_colors()

    print(f"{COLOR_BOLD + COLOR_PURPLE}  ☆彡(ノ^ ^)ノ     Waifu Git Helper         ヽ(^ ^ヽ)☆彡")
    print(f"{COLOR_BOLD + COLOR_CYAN}  ★~(◠‿◕✿)        1. CherryPick & Push           ✿◕‿◠)~★")
    print(f"{COLOR_BOLD + COLOR_RED}  ★~(◠‿◕✿)        2. Multiple CherryPick & Push  ✿◕‿◠)~★")
    print(f"{COLOR_BOLD + COLOR_GREEN}  ★~(◠‿◕✿)        3. Create Patch                ✿◕‿◠)~★")
    print(f"{COLOR_BOLD + COLOR_YELLOW}  ★~(◠‿◕✿)        4. Apply Patch                 ✿◕‿◠)~★")
    print(f"{COLOR_BOLD + COLOR_BLUE}  ★~(◠‿◕✿)        5. Install Packages            ✿◕‿◠)~★")
    print(f"{COLOR_BOLD + COLOR_CYAN}  ★~(◠‿◕✿)        6. Install Custom Packages     ✿◕‿◠)~★")
    print(f"{COLOR_BOLD + COLOR_BLUE}  ★~(◠‿◕✿)        7. Exit                        ✿◕‿◠)~★")
    print(COLOR_RESET)

    choice = input(f"{COLOR_RESET}{time_say()} {COLOR_YELLOW}Akari-Sama{
                   COLOR_RESET}.\n\n{COLOR_RESET}choose what want to do-nyan {COLOR_CYAN}")

    if choice == '1':
        commit_hash_push()
    elif choice == '2':
        commit_hashes_push()
    elif choice == '3':
        create_patch_hash()
    elif choice == '4':
        apply_patch()
    elif choice == '5':
        install_packages()
    elif choice == '6':
        custom_install_packages()
    elif choice == '7' or choice == "exit":
        print(COLOR_GREEN + "Goodbye! Have a nice day! ｡◕‿◕｡" + COLOR_RESET)
        exit()
    else:
        print(COLOR_RED + "Invalid choice! Please choose again." + COLOR_RESET)
        menu()


def run_command(command):
    result = subprocess.run(command, shell=True,
                            text=True, capture_output=True)
    return result


def commit_in_branch(commit_hash, branch):
    result = run_command(f"git log {branch} --pretty=format:%H")
    return commit_hash in result.stdout.split()


def apply_commit_to_branch(commit_hash, branch):
    if commit_in_branch(commit_hash, branch):
        print(COLOR_YELLOW + f"Commit {commit_hash} is already present in the branch {
              branch}. Pushing..." + COLOR_RESET)
        push_result = run_command(f"git push origin {branch}")
        if push_result.returncode == 0:
            print(COLOR_GREEN +
                  f"Branch {branch} sent successfully" + COLOR_RESET)
        else:
            print(COLOR_RED +
                  f"Error when pushing branch {branch}." + COLOR_RESET)
        return

    checkout_result = run_command(f"git checkout {branch}")
    if checkout_result.returncode != 0:
        print(COLOR_RED + f"Error when switching to branch {
              branch}. Jumping to the next branch." + COLOR_RESET)
        return

    cherry_pick_result = run_command(f"git cherry-pick {commit_hash}")
    if cherry_pick_result.returncode == 0:
        print(COLOR_GREEN +
              f"Cherry-pick successfully applied to the branch {branch}" + COLOR_RESET)
        push_result = run_command(f"git push origin {branch}")
        if push_result.returncode == 0:
            print(COLOR_GREEN +
                  f"Branch {branch} sent successfully." + COLOR_RESET)
        else:
            print(COLOR_RED +
                  f"Error when pushing branch {branch}." + COLOR_RESET)
    else:
        print(COLOR_RED + f"Error when cherry-picking the branch {
              branch}. Trying to resolve conflicts." + COLOR_RESET)
        run_command("git cherry-pick --abort")
        print(
            COLOR_RED + f"Cherry-pick aborted on branch {branch} due to conflicts." + COLOR_RESET)


def commit_hash_push():
    while True:
        commit_hash = input(COLOR_RESET + "Commit hash: ").strip()
        if commit_hash:
            break
        else:
            print(
                COLOR_RED + "Commit hash cannot be empty. Please enter a valid commit hash." + COLOR_RESET)

    branches = [
        "fourteen",
        "fourteen_dynamic_noksu",
        "fourteen_dynamic",
        "noksu"
    ]

    for branch in branches:
        print(COLOR_CYAN + f"Cherry-picking the branch {branch}" + COLOR_RESET)
        apply_commit_to_branch(commit_hash, branch)

    run_command("git checkout fourteen")


def commit_hashes_push():
    while True:
        commit_hashes_input = input(
            COLOR_RESET + "Enter commit hashes separated by space (or 'done' to finish): ").strip()
        if commit_hashes_input.lower() == 'done':
            print(COLOR_RED +
                  "No commit hashes entered. Returning to menu." + COLOR_RESET)
            menu()
            return
        elif commit_hashes_input:
            commit_hashes = commit_hashes_input.split()
            break
        else:
            print(
                COLOR_RED + "Commit hashes cannot be empty. Please enter valid commit hashes." + COLOR_RESET)

    branches = [
        "fourteen",
        "fourteen_dynamic_noksu",
        "fourteen_dynamic",
        "noksu"
    ]

    for branch in branches:
        print(COLOR_CYAN + f"Cherry-picking the branch {branch}" + COLOR_RESET)
        for commit_hash in commit_hashes:
            apply_commit_to_branch(commit_hash, branch)

    run_command("git checkout fourteen")


def create_patch_hash():
    hash = str(input(COLOR_RESET + "Commit hash: ")).strip()
    name_patch = str(input(COLOR_RESET + "Name of the patch? "))
    result = run_command(f"git diff {hash}^! > {name_patch}.patch")

    if result.returncode == 0:
        print(COLOR_GREEN +
              f"{name_patch}.patch successfully created." + COLOR_RESET)
    else:
        print(COLOR_YELLOW + f"An error occurred, try again...")


def apply_patch():
    path = str(input(COLOR_RESET + "Path: "))
    patch = str(input("Patch: "))
    result = run_command(COLOR_RESET + f"patch {path} < {patch}.patch")

    if result.returncode == 0:
        print(COLOR_GREEN + f"Apply {patch} with successfully!" + COLOR_RESET)
    else:
        print(COLOR_RED + f"Error to apply {patch}" + COLOR_RESET)


def detect_os(os_name):
    os_name = run_command(
        "cat /etc/os-release | grep -oP '(?<=^ID=).+'").stdout
    return os_name


def spinning_cursor(stop_event):
    while not stop_event.is_set():
        for cursor in '|/-\\':
            sys.stdout.write(cursor)
            sys.stdout.flush()
            sleep(0.1)
            sys.stdout.write('\b')


def custom_install_packages():
    clear()

    # run_command("./anime/install.sh")
    # miku = run_command("anime -r miku").stdout
    # print(miku)

    print(f"""
|---------------------------------------------------|
|        {COLOR_BOLD + COLOR_BLUE}Install Packages Customs                   |
|                                                   |
|    [1]. Install ccache    ⋆｡°✩                    |
|    [2]. Back To Menu            ⋆｡°✩              |
|    [3]. Exit             ⋆｡°✩        ⋆｡°✩         |
|                                                   |
|----------------------------------------------------""")

    choice = str(input(COLOR_BOLD + COLOR_WHITE + "choose ur option-nyan "))

    if choice == "1":
        install_ccache()
    elif choice == "2":
        menu()
    elif choice == "3":
        print("Bye!")
        exit()


def install_ccache():
    if detect_os("arch") or detect_os("archarm"):
        print(COLOR_BOLD + COLOR_YELLOW + "Installing... ", end="")
        stop_event = threading.Event()
        spinner_thread = threading.Thread(
            target=spinning_cursor, args=(stop_event,))
        spinner_thread.start()
        result = run_command("pacman -S ccache --noconfirm")

        stop_event.set()
        spinner_thread.join()

        if result.returncode == 0:
            print(COLOR_BLUE + "\nInstalled.")
            input()
            menu()


def install_packages():
    choice = str(
        input(COLOR_RESET + "Sir,\nU want the really install packages? " + COLOR_CYAN))
    yes = ["yes", "yeah", "yup", "yeah"]

    for y in yes:
        if y in choice:
            pkgs = ["bc", "neovim"]  # add more packages
            for pkg in pkgs:

                if detect_os("archarm") or detect_os("arch"):
                    print(COLOR_YELLOW + "Installing the packages, wait...")
                    result = run_command(f"pacman -S {pkg} --noconfirm")
                    if result.returncode == 0:
                        print(COLOR_GREEN + f"Installed Package {pkg} (:")
                    else:
                        print(
                            COLOR_RED + "ARCH! ERORR: I don't know, I just know that an error occurred... hehe")

                elif detect_os("ubuntu") or detect_os("Ubuntu"):
                    print(COLOR_YELLOW + "Installing the packages, wait...")
                    result = run_command(f"sudo apt install {pkg} -y")
                    if result.returncode == 0:
                        print(COLOR_GREEN + f"Installed Package {pkg} (:")
                    else:
                        print(
                            COLOR_RED + "UBUNTU! ERROR: I don't know, I just know that an error occurred... hehe")

                else:
                    print(COLOR_RED + "Occurred an Error.")

        elif "" in choice:
            menu()


if __name__ == "__main__":
    menu()
