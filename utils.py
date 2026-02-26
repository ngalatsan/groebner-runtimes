import os
import json
import pandas as pd
from config import JSON_DIR, RESULTS_DIR

def load_json_data(test_name, json_dir=JSON_DIR):
    """Загружает данные теста из JSON"""
    path = os.path.join(json_dir, f"{test_name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON для {test_name} не найден: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_result(result, test_name, method, order, results_dir=RESULTS_DIR):
    """Сохраняет результат вычислений в JSON"""
    filename = f"{test_name}_{method}_{order}.json"
    path = os.path.join(results_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)

def load_all_results(results_dir=RESULTS_DIR):
    """Загружает все результаты из папки"""
    all_results = []
    if not os.path.isdir(results_dir):
        return all_results

    for filename in os.listdir(results_dir):
        if filename.endswith('.json'):
            path = os.path.join(results_dir, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_results.append(data)
            except Exception as e:
                print(f"Ошибка чтения {filename}: {e}")
    return all_results


def save_summary(results, summary_path='summary_table.csv'):
    """Сохраняет результаты в CSV"""
    if not results:
        print("Нет результатов для сохранения")
        return

    df = pd.DataFrame(results)

    # Приводим метрики памяти к None в режиме clean
    clean_mask = df['mode'] == 'clean'
    for col in ['avr_memory', 'max_memory', 'mem_per_sec']:
        if col in df.columns:
            df.loc[clean_mask, col] = None

    # Желаемый порядок столбцов
    desired_order = [
        'test', 'method', 'order', 'time', 'dimension',
        'num_vars', 'num_equations', 'basis_size',
        'avr_memory', 'max_memory', 'mem_per_sec',
        'crit1', 'crit2', 'error', 'mode', 'status'
    ]

    existing_cols = [col for col in desired_order if col in df.columns]
    df = df[existing_cols]
    df.to_csv(summary_path, sep=';', index=False, decimal=',', float_format='%.4f')
    print(f"\nСводная таблица сохранена: {summary_path}")