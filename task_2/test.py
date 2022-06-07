import sys
from os.path import abspath, dirname
import contextlib, io
import precode as pr
# import author as au


root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

# stdout работы файла с кодом студента (все его print()) в виде одной строки
output = io.StringIO()
with contextlib.redirect_stdout(output):
    import precode

# переменная, в которой в виде строки хранится весь код студента.
with open("precode.py", encoding="utf-8") as precode:
    user_code = precode.readlines()

# stdout работы файла с кодом автора (все его print()) в виде одной строки
author_output = io.StringIO()
with contextlib.redirect_stdout(author_output):
    import author


def test_response_output():
    assert output.getvalue() == author_output.getvalue(), (
        "Вы ошиблись в выводе на экран")

def test_method_show_contact():
    assert hasattr(pr.Contact, "show_contact"), (
        "Проверьте наличие метода show_contact в классе Contact")



