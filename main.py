from config import VERY_QUICK, QUICK, MEDIUM, RESULTS_DIR
from utils import *
from test_runners import GinvRunner, SympyRunner
from timeout_utils import run_with_timeout
import os

# Конфигурация
METHODS = ['ginv', 'sympy']
CATEGORIES = VERY_QUICK + QUICK + MEDIUM
ORDERS = ['deglex']
VERBOSE = True
SAVE_CSV = True
MEASURE_MEMORY = False
TIMEOUT = 600  # секунд (None без таймаута)

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

                print(f"\nЗапуск: {test_name} ({method}, {order})")

                runner_class = RUNNER_CLASSES.get(method)
                if not runner_class:
                    print(f"Runner для {method} не найден")
                    continue

                runner = runner_class(order)
                try:
                    if TIMEOUT:
                        result = run_with_timeout(
                            runner.run_test,
                            TIMEOUT,
                            test_name,
                            test_data[test_name],
                            verbose=VERBOSE,
                            measure_memory=MEASURE_MEMORY
                        )
                    else:
                        result = runner.run_test(
                            test_name,
                            test_data[test_name],
                            verbose=VERBOSE,
                            measure_memory=MEASURE_MEMORY
                        )
                except Exception as e:
                    print(f"Ошибка в {test_name} ({method}): {e}")
                    continue

                # обработка таймаута
                if result and result.get("status") == "timeout":
                    print(f" - таймаут: {test_name} ({method}, {order}) > {TIMEOUT} c")
                    result.update({
                        'test': test_name,
                        'method': method,
                        'order': order,
                        'dimension': test_data[test_name].get("dimension"),
                        'num_vars': len(test_data[test_name]["variables"]),
                        'num_equations': len(test_data[test_name]["equations"]),
                        'basis_size': None,
                        'avr_memory': None,
                        'max_memory': None,
                        'mem_per_sec': None,
                        'mode': 'memory' if MEASURE_MEMORY else 'clean'
                    })
                if result and "status" not in result:
                    result["status"] = "ok"

                if result:
                    results.append(result)
                    save_result(result, test_name, method, order)

    all_results = load_all_results() + results  # сохранение в csv всех результатов (в том числе ранее вычисленных)
    if SAVE_CSV:
        save_summary(all_results) # заменить на results для только новых результатов

    print("\nВсе тесты завершены")
    return results


if __name__ == '__main__':
    results = run_all_tests()