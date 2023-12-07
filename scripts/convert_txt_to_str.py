import os


def read_txt_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


file_path = os.path.join("../data", "note1.txt")
text_content = read_txt_file(file_path)
result = text_content.replace("\"", "'")

if text_content is not None:
    print(f"{repr(result)}")
