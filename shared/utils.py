def create_symlink(source, target, dry_run):
    if dry_run:
        print(f"Would link {source} -> {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or target.exists():
        if target.is_symlink() and target.resolve() == source.resolve():
            print(f"Symlink already correct {target} -> {source}")
            return
        if target.is_symlink():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
    target.symlink_to(source)
    print(f"Linked {source} -> {target}")
