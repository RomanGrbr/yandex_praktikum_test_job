import time


def time_check(func):
    def wrapper(*args):
        start_time = time.time()
        result = func(*args)
        execution_time = round(time.time() - start_time, 1)
        # execution_time = time.time() - start_time
        print(f'Время выполнения функции: {execution_time} с.')
        return result

    return wrapper


def cache_args(func):

# Здесь код декоратора
    _result = {}

    def run(num):
        if num in _result:
            return _result[num]
        else:
            _result[num] = func(num)
            return _result[num]

    return run

    # Здесь код декоратора
    # def run(num):
    #     _result = func(num)
    #     return _result

    # return run

@time_check
@cache_args
def long_heavy(num):
    time.sleep(1)
    return num * 2


print(long_heavy(1))
# Время выполнения функции: 1.0 с.
# 2
print(long_heavy(1))
# Время выполнения функции: 0.0 с.
# 2
print(long_heavy(2))
# Время выполнения функции: 1.0 с.
# 4
print(long_heavy(2))
# Время выполнения функции: 0.0 с.
# 4
print(long_heavy(2))
# Время выполнения функции: 0.0 с.
# 4
