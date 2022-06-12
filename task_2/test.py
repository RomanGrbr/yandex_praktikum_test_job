import contextlib
import io

import pytest

# stdout работы файла с кодом студента (все его print()) в виде одной строки
output = io.StringIO()
with contextlib.redirect_stdout(output):
    try:
        import precode
    except SyntaxError as e:
        assert False, f"Синтаксическая ошибка: {e}"
    except ImportError as e:
        assert False, f"Ошибка импорта: {e}"
    except NameError as e:
        assert False, f"Имя не определено: {e}"
    except Exception as e:
        assert False, (
            f"Не удалось запустить код. Исправьте в нем ошибки: {e}")

# переменная, в которой в виде строки хранится весь код студента.
with open("precode.py", encoding="utf-8") as task:
    user_code = task.read()

# stdout работы файла с кодом автора (все его print()) в виде одной строки
author_output = io.StringIO()
with contextlib.redirect_stdout(author_output):
    import author


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
        return f"Функции `{def_name}()` не должно быть"


@pytest.fixture
def msg_err():
    def _msg_err(msg_name, *args, **kwargs):
        msg = MsgError(msg_name, *args, **kwargs)
        return msg.result
    return _msg_err


class TestContact:

    def test_print_contact(self, msg_err):
        """
        Тест отсутствия метода print_contact в классе Contact.
        """
        assert not hasattr(precode, "print_contact"), msg_err(
            "dont_create_def", "print_contact")

    def test_attr_name(self):
        """
        Тест наличия атрибутов класса Contact.
        """
        author_data = author.vlad.__dict__
        try:
            user = precode.Contact(
                "Михаил Булгаков", "2-03-27", "15.05.1891",
                "Россия, Москва, Большая Пироговская, дом 35б, кв. 6"
            )
        except (TypeError, NameError) as e:
            assert False, (
                f"{e} Не меняйте метод `__init__()` класса `Contact` "
            )

        for key in author_data.keys():
            assert hasattr(user, key), (
                f"Error: Проверьте наличие атрибута {key} в классе Contact"
            )

    def test_extra_attributes(self):
        """
        Тест количества и наименования переменных.
        """
        author_attr = [
            value for value in author.__dict__ if not value.startswith('__')]
        user_attr = [
            value for value in precode.__dict__ if not value.startswith('__')]

        assert len(author_attr) >= len(user_attr), (
            "Убедитесь, что нет лишних переменных/функций")
        assert len(author_attr) <= len(user_attr), (
            "Убедитесь, что есть все переменные/функции")
        assert author_attr == user_attr, (
            "Убедитесь, что переменные/функции названы верно")

    def test_response_output(self):
        """Тест корректности вывода."""
        assert output.getvalue() == author_output.getvalue(), (
            "Error: Вы ошиблись в выводе на экран !")
