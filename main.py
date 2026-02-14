from config import VERY_QUICK, QUICK, ORDER_MAPPING, JSON_DIR, RESULTS_DIR
from utils import save_result, save_summary
from test_runners import GinvRunner, SympyRunner
import os

# Конфигурация
METHODS = ['ginv', 'sympy']  # Методы
CATEGORIES = VERY_QUICK  # Тесты (quick benchmarks)
ORDERS = ['deglex']  # Порядки (универсальные названия)
VERBOSE = True
SAVE_CSV = True

# Соответствие методов к классам runners
RUNNER_CLASSES = {
    'ginv': GinvRunner,
    'sympy': SympyRunner
}

def run_all_tests():
    results = []
    done_files = set(os.listdir(RESULTS_DIR)) if os.path.isdir(RESULTS_DIR) else set()

    for test_name in CATEGORIES:
        for method in METHODS:
            for order in ORDERS:
                result_filename = f"{test_name}_{method}_{order}.json"
                if result_filename in done_files:
                    print(f"Пропуск (уже есть): {result_filename}")
                    continue

                print(f"\nЗапуск: {test_name} ({method}, {order})")

                runner_class = RUNNER_CLASSES.get(method)
                if not runner_class:
                    print(f"Runner для {method} не найден")
                    continue

                runner = runner_class(order)
                result = runner.run_test(test_name, verbose=VERBOSE)

                if result:
                    results.append(result)
                    save_result(result, test_name, method, order)

    if SAVE_CSV:
        save_summary(results)

    print("\nВсе тесты завершены")
    return results


if __name__ == '__main__':
    run_all_tests()