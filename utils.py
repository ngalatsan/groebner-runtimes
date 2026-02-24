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
    """Загружает существующие результаты в папке"""
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
    """Сохраняет все результаты в CSV, перезаписывая существующий файл"""
    if not results:
        print("Нет результатов для сохранения")
        return

    df = pd.DataFrame(results)
    df.to_csv(summary_path, sep=';', index=False, decimal=',', float_format='%.3f')
    print(f"\nСводная таблица сохранена успешно: {summary_path}")