from pathlib import Path

BASE_DIR = Path("output").resolve()


def create_file(path: str, content: str):
    path_obj = Path(path).resolve()

    if not str(path_obj).startswith(str(BASE_DIR)):
        raise ValueError("❌ Writing outside output/ is not allowed")

    path_obj.parent.mkdir(parents=True, exist_ok=True)

    with open(path_obj, "w") as f:
        f.write(content)

    print(f"✔ Created file: {path}")


def read_file(path: str) -> str:
    path_obj = Path(path).resolve()

    if not str(path_obj).startswith(str(BASE_DIR)):
        raise ValueError("❌ Reading outside output/ is not allowed")

    with open(path_obj, "r") as f:
        return f.read()


def update_file(path: str, content: str):
    create_file(path, content)


def list_files():
    files = []
    for path in BASE_DIR.rglob("*"):
        if path.is_file():
            files.append(str(path))
    return files

def create_directory(path: str):
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created directory: {path}")
