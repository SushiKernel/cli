import subprocess

def run_command(command, wait=True):
    """Executa um comando no shell e retorna a saída."""
    if wait:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Erro ao executar comando: {command}")
            print(result.stderr)
        return result
    else:
        subprocess.run(command, shell=True)

def get_commit_message(commit_hash):
    """Obtém a mensagem do commit com base no hash."""
    command = f"git log -1 --pretty=%B {commit_hash}"
    result = run_command(command)
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return ""

def cherry_pick_commits(start_commit, end_commit):
    """Realiza o cherry-pick dos commits entre start_commit e end_commit."""
    # Obtém a lista de commits no intervalo especificado
    command = f"git log --reverse --format=%H {start_commit}..{end_commit}"
    result = run_command(command)
    
    if result.returncode != 0:
        print("Falha ao obter a lista de commits.")
        return

    commits = result.stdout.strip().split("\n")

    for commit in commits:
        # Verifica a mensagem do commit
        commit_message = get_commit_message(commit)
        # print(f"Processando commit {commit}: {commit_message}")

        # Se a mensagem do commit contém "LTS: Update to", abra o Neovim
        if "LTS: Update to" in commit_message:
            print(f"Abrindo Neovim para o commit {commit}...")
            run_command("nvim Makefile", wait=False)
            input("Pressione Enter para continuar após fechar o Neovim...")

        print(f"Aplicando cherry-pick no commit {commit}...")
        result = run_command(f"git cherry-pick {commit}")
        
        if result.returncode != 0:
            print(f"Conflito no commit {commit}. Pulando...")
            run_command("git cherry-pick --skip")
        else:
            print(f"Commit {commit} aplicado com sucesso.")

if __name__ == "__main__":
    start_commit = input("Digite o hash do commit inicial: ")
    end_commit = input("Digite o hash do commit final: ")
    cherry_pick_commits(start_commit, end_commit)

