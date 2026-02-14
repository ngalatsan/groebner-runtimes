from config import TEST_VERY_QUICK, RESULTS_DIR
from utils import save_result, save_summary, load_json_data
from test_runners import GinvRunner, SympyRunner
import os

# Конфигурация
METHODS = ['ginv', 'sympy']  # Методы
CATEGORIES = TEST_VERY_QUICK  # Тесты
ORDERS = ['deglex']  # Порядки
VERBOSE = True
SAVE_CSV = True

"""
TO DO

MEASURE_MEMORY = True  # Замерять ли память или чистое время
"""


# Соответствие методов к классам runners
RUNNER_CLASSES = {
    'ginv': GinvRunner,
    'sympy': SympyRunner
}

if not os.path.isdir(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

test_data = {}
for test_name in set(CATEGORIES):
    test_data[test_name] = load_json_data(test_name)

def run_all_tests():
    """Запускает все тесты по конфигурации и сохраняет результаты"""
    results = []
    done_files = set(os.listdir(RESULTS_DIR)) if os.path.isdir(RESULTS_DIR) else set()

    for test_name in CATEGORIES:
        for method in METHODS:
            for order in ORDERS:
                result_filename = f"{test_name}_{method}_{order}.json"
                if result_filename in done_files:
                    print(f"Пропуск (уже есть): {result_filename}")
                    continue

                print(f"\nЗапуск: {test_name} ({method})")

                runner_class = RUNNER_CLASSES.get(method)
                if not runner_class:
                    print(f"Runner для {method} не найден")
                    continue

                runner = runner_class(order)
                try:
                    result = runner.run_test(test_name, test_data[test_name], verbose=VERBOSE)
                except Exception as e:
                    print(f"Ошибка в {test_name} ({method}): {e}")
                    continue

                if result:
                    results.append(result)
                    save_result(result, test_name, method, order)

    if SAVE_CSV:
        save_summary(results)

    print("\nВсе тесты завершены")
    return results


if __name__ == '__main__':
    run_all_tests()