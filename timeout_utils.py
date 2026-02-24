import multiprocessing as mp
import time


def _timeout_target(queue, func, args, kwargs):
    """Функция-исполнитель (должна быть на уровне модуля для Windows)"""
    try:
        result = func(*args, **kwargs)
        queue.put(("ok", result))
    except Exception as e:
        queue.put(("error", str(e)))


def run_with_timeout(func, timeout, *args, **kwargs):
    """
    Запускает func в отдельном процессе.
    Если время превышено — процесс убивается.
    Возвращает результат func или dict с timeout.
    """

    queue = mp.Queue()
    p = mp.Process(
        target=_timeout_target,
        args=(queue, func, args, kwargs)
    )

    start = time.perf_counter()
    p.start()
    p.join(timeout)

    # Таймаут
    if p.is_alive():
        p.terminate()
        p.join()
        elapsed = time.perf_counter() - start
        return {
            "status": "timeout",
            "time": round(elapsed, 3)
        }

    # Получаем результат
    if queue.empty():
        return {
            "status": "error",
            "error": "Empty result"
        }

    status, data = queue.get()

    if status == "error":
        return {
            "status": "error",
            "error": data
        }

    return data