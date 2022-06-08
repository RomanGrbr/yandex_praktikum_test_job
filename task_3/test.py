import contextlib
import io


# stdout работы файла с кодом студента (все его print()) в виде одной строки
output = io.StringIO()
with contextlib.redirect_stdout(output):
    import precode

# переменная, в которой в виде строки хранится весь код студента.
with open("precode.py", encoding="utf-8") as task:
    user_code = task.readlines()

# stdout работы файла с кодом автора (все его print()) в виде одной строки
author_output = io.StringIO()
with contextlib.redirect_stdout(author_output):
    import author

def test_response_output():
    assert output.getvalue() == author_output.getvalue(), (
        "Error: Вы ошиблись в выводе на экран !")
