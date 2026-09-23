import pathlib


def main(dry_run: bool):
    home = pathlib.Path.home()
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    source_line = f"source {repo_root}/shell/init.sh"
    bashrc = home / ".bashrc"
    if dry_run:
        if not bashrc.exists():
            print(f"Would create {bashrc} with source line for shell/init.sh")
            return
        content = bashrc.read_text() if bashrc.exists() else ""
        if source_line in content:
            print("Would keep existing shell init sourcing in ~/.bashrc")
        else:
            print(f"Would add shell init sourcing to {bashrc}")
        return
    if not bashrc.exists():
        bashrc.write_text(source_line + "\n")
        print(f"Created {bashrc} with shell init sourcing")
        return
    content = bashrc.read_text()
    if source_line in content:
        print("Shell init sourcing already present in ~/.bashrc")
    else:
        with bashrc.open("a") as handle:
            handle.write("\n" + source_line + "\n")
        print(f"Added shell init sourcing to {bashrc}")
