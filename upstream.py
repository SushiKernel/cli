import os
import subprocess
from dotenv import load_dotenv

TOKEN_GITHUB = os.getenv('TOKEN_GITHUB', '')
USER = "MoeKernel"
REPO = "scripts"

def run_command(command):
    """Executa um comando no shell e retorna a saída."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stdout:
        return result.stdout.strip()
    if result.stderr:
        return result.stderr.strip()
    return None

def fetch_and_reset_upstream(upstream_repo, branch):
    """Busca as atualizações do repositório upstream e aplica no branch atual."""
    run_command(f"git remote add upstream {upstream_repo} || true")
    run_command(f"git fetch upstream {branch}")
    run_command(f"git reset --hard upstream/{branch}")

def merge_with_strategy(branch, file_specific_strategy=None):
    """Faz o merge do branch upstream com a estratégia especificada."""
    result = run_command(f"git merge -X ours upstream/{branch}")

    if result and "CONFLICT" in result:
        print("Conflitos detectados. Resolvendo automaticamente...")

        # Verifica se há conflitos no arquivo específico (ex.: Makefile)
        if file_specific_strategy:
            for file, strategy in file_specific_strategy.items():
                if file in run_command("git diff --name-only --diff-filter=U"):
                    print(f"Conflito detectado em {file}. Usando a estratégia '{strategy}'.")
                    run_command(f"git checkout --{strategy} {file}")
                    run_command(f"git add {file}")

        unmerged_files = run_command("git diff --name-only --diff-filter=U")
        if unmerged_files:
            unmerged_files_list = set(unmerged_files.splitlines())
            for file in unmerged_files_list:
                run_command(f"git add {file}")

        run_command("git commit -m 'Resolve merge conflicts: preserving local changes'")
        print("Conflitos resolvidos.")

    print(f"Merge das mudanças do upstream {branch} concluído com sucesso.")

def clean_and_commit_makefile():
    """Remove a parte '-openela' da variável EXTRAVERSION no Makefile e comita as mudanças."""
    try:
        with open('Makefile', 'r') as file:
            lines = file.readlines()

        modified = False
        with open('Makefile', 'w') as file:
            for line in lines:
                if line.startswith("EXTRAVERSION"):
                    if '-openela' in line:
                        line = "EXTRAVERSION =\n"
                        modified = True
                file.write(line)

        if modified:
            print("Makefile atualizado. Comitando as mudanças...")
            run_command("git add Makefile")
            run_command('git commit -m "Remove -openela from EXTRAVERSION in Makefile"')
            print("Mudanças no Makefile comitadas com sucesso.")
        else:
            print("Nenhuma alteração necessária no Makefile.")
    except FileNotFoundError:
        print("Makefile não encontrado. Verifique se o arquivo está presente.")

def push_changes(branch):
    """Envia as mudanças para o repositório original."""
    url_remoto = f'https://{USER}:{TOKEN_GITHUB}@github.com/{USER}/{REPO}.git'
    subprocess.run(["git", "remote", "set-url", "origin", url_remoto])
    subprocess.run(["git", "config", "--global", "user.email", "akariondev@gmail.com"])
    subprocess.run(["git", "config", "--global", "user.name", "Akari Shoiya"])

    result = run_command(f"git push origin {branch}")
    if result:
        print(f"Push das mudanças para o branch {branch} realizado com sucesso.")
    else:
        print(f"Falha ao enviar as mudanças para o branch {branch}.")

def process_branches(upstream_repo, upstream_branch, branches):
    """Processa uma lista de branches para atualizar e enviar mudanças."""
    fetch_and_reset_upstream(upstream_repo, upstream_branch)

    for branch in branches:
        print(f"Processando o branch {branch}...")
        run_command(f"git checkout {branch}")
        merge_with_strategy(upstream_branch, file_specific_strategy={"Makefile": "theirs"})
        clean_and_commit_makefile()
        push_changes(branch)

if __name__ == "__main__":
    upstream_repo = "https://github.com/openela/kernel-lts.git"
    upstream_branch = "linux-4.14.y"
    branches = [
#        "test_kkk",
#        "test_2",
#        "test_3"
        "fourteen",
        "fourteen_dynamic_noksu",
        "fourteen_dynamic",
        "without-ksu"
    ]

    # Processar todas as branches definidas
    process_branches(upstream_repo, upstream_branch, branches)
