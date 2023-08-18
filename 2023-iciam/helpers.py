# Adapted from https://github.com/quarto-ext/shinylive/issues/13

from pathlib import Path


def include_shiny_folder(path, viewer_height=600):
    folder_path = Path(__file__).parent / path

    # Start with the header
    header = f"```{{shinylive-python}}\n#| standalone: true\n#| viewerHeight: {viewer_height}\n"
    print(header)

    # Print contents of app.py
    app_path = folder_path / "app.py"

    with open(app_path, "r") as app_file:
        app_contents = app_file.read()
        print(app_contents)

    file_paths = folder_path.glob("**/*")

    # Additional files need to start with ## file:
    for file_path in file_paths:
        if file_path.suffix == ".py" and file_path.name != "app.py":
            print(f"\n## file: {file_path.name}")
            with open(file_path, "r") as file:
                file_contents = file.read()
                print(file_contents)

    # Finish with the closing tag
    print("```")

