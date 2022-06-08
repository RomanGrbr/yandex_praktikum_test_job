import contextlib
import importlib
import io

import author
import precode

import sys
from os.path import abspath, dirname

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

pytest_plugins = [
    'task_2.precode',
]

# stdout работы файла с кодом студента (все его print()) в виде одной строки
output = io.StringIO()
with contextlib.redirect_stdout(output):
    importlib.reload(precode)


# переменная, в которой в виде строки хранится весь код студента.
with open("precode.py", encoding="utf-8") as task:
    user_code = task.read()

# stdout работы файла с кодом автора (все его print()) в виде одной строки
author_output = io.StringIO()
with contextlib.redirect_stdout(author_output):
    importlib.reload(author)


def test_response_output():
    assert output.getvalue() == author_output.getvalue(), (
        "Erroe: Вы ошиблись в выводе на экран")

    
def test_method_show_contact():
    assert hasattr(precode.Contact, "show_contact"), (
        "Error: Проверьте наличие метода show_contact в классе Contact")

def test_attribut():
    author_attr = [value for value in author.__dict__ if not value.startswith('__')]
    user_attr = [value for value in precode.__dict__ if not value.startswith('__')]
    assert author_attr == user_attr, (
        "Error: Проверьте нет ли лишних атрибутов")
