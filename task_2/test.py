import contextlib
import importlib
import io

import pytest

import author
import precode

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


class MsgError:

    def __init__(self, method_name, *args, **kwargs):
        self.result = getattr(self, method_name)(*args, **kwargs)

    def add_class(self, class_name, child=False, parent_name=""):
        text = f"Добавьте класс `{class_name}`"
        if child:
            text += f", этот класс наследуется от класса `{parent_name}`"
        return

    def add_method(self, method_name, class_name):
        return f"Добавьте метод `{method_name}()` для класса `{class_name}`"

    def dont_create_def(self, def_name):
        return f"`Функции `{def_name}()` не должно быть"


@pytest.fixture
def msg_err():
    def _msg_err(msg_name, *args, **kwargs):
        msg = MsgError(msg_name, *args, **kwargs)
        return msg.result
    return _msg_err


class TestContact:

    def test_method_show_contact(self, msg_err):
        assert hasattr(precode.Contact, "show_contact"), msg_err(
            "add_method", "show_contact", "Contact")
        assert not hasattr(precode, "print_contact"), msg_err(
            "dont_create_def", "print_contact")

    def test_attr_name(self):
        user = precode.Contact("Михаил Булгаков", "2-03-27", "15.05.1891", "Россия, Москва, Большая Пироговская, дом 35б, кв. 6")
        author_data = author.vlad.__dict__
        for key in author_data.keys():
            assert hasattr(user, key), (
                f"Error: Проверьте наличие атрибута {key} в классе Contact"
            )

    def test_extra_attributes(self):
        author_attr = [
            value for value in author.__dict__ if not value.startswith('__')]
        user_attr = [
            value for value in precode.__dict__ if not value.startswith('__')]

        assert len(author_attr) >= len(user_attr), (
            "Error: Убедитесь, что нет лишних переменных")
        assert len(author_attr) <= len(user_attr), (
            "Error: Убедитесь, что есть все переменные")
        assert author_attr == user_attr, (
            "Error: Убедитесь, что переменные названы верно")

    def test_response_output(self):
        assert output.getvalue() == author_output.getvalue(), (
            "Error: Вы ошиблись в выводе на экран !")
