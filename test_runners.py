import time
from memory_profiler import memory_usage
from abc import ABC, abstractmethod
from config import ORDER_MAPPING

from ginv.monom import Monom
from ginv.poly import Poly
from ginv.gb import GB
from sympy import groebner, symbols, ZZ


class TestRunner(ABC):
    """Абстрактный класс для запуска тестов"""

    def __init__(self, method_name, order):
        self.method_name = method_name
        self.order = order
        self.internal_order = ORDER_MAPPING[method_name].get(order, None)
        if not self.internal_order:
            raise ValueError(f"Неподдерживаемый порядок '{order}' для {method_name}")

    @abstractmethod
    def run_test(self, test_name, data, verbose=True, measure_memory=True):
        """Запускает тест и возвращает dict с результатами"""
        pass


class GinvRunner(TestRunner):
    def __init__(self, order):
        super().__init__('ginv', order)

    def init_ginv(self, variables):
        Monom.init(variables)
        Monom.variables = variables.copy()
        Monom.zero = Monom(0 for _ in Monom.variables)
        Monom.cmp = getattr(Monom, self.internal_order)
        Poly.cmp = Monom.cmp
        local_dict = {}
        for i, var in enumerate(variables):
            p = Poly()
            p.append([Monom([0 if j != i else 1 for j in range(len(variables))]), 1])
            local_dict[var] = p
        return local_dict

    def run_test(self, test_name, data, verbose=True, measure_memory=True):
        dimension = data.get("dimension", None)
        variables = data["variables"]
        equations = data["equations"]

        local_dict = self.init_ginv(variables)
        eqs = [eval(eq.replace('^', '**'), {"__builtins__": {}}, local_dict) for eq in equations]

        G = GB()

        def compute():
            G.algorithm2(eqs)
            return G

        start_time = time.perf_counter()

        if measure_memory:
            mem_log, basis = memory_usage(compute, interval=0.1, retval=True)
        else:
            basis = compute()
            mem_log = []

        elapsed = time.perf_counter() - start_time

        basis_size = len(basis) if basis else None

        result = {
            'test': test_name,
            'method': self.method_name,
            'order': self.order,
            'time': round(elapsed, 3),
            'dimension': dimension,
            'crit1': int(G.crit1) if hasattr(G, 'crit1') else None,
            'crit2': int(G.crit2) if hasattr(G, 'crit2') else None,
            'num_vars': len(variables),
            'num_equations': len(eqs),
            'basis_size': basis_size,
            'avr_memory': round(sum(mem_log) / len(mem_log), 2) if mem_log else 0.0,
            'max_memory': round(max(mem_log), 2) if mem_log else 0.0,
            'mem_per_sec': round(max(mem_log) / elapsed, 2) if elapsed > 0 and mem_log else 0.0,
            'mode': 'memory' if measure_memory else 'clean'
        }

        if verbose:
            mem_str = f", {result['max_memory']:.1f} Мб" if measure_memory else ""
            print(
                f" + {test_name} ({self.method_name}, {self.order}): {elapsed:.3f} с{mem_str}, базис: {basis_size} полиномов")

        return result


class SympyRunner(TestRunner):
    def __init__(self, order):
        super().__init__('sympy', order)

    def run_test(self, test_name, data, verbose=True, measure_memory=True):
        dimension = data.get("dimension", None)
        variables = data["variables"]
        equations = data["equations"]

        sym_vars = symbols(' '.join(variables))
        local_dict = {v: sym_vars[i] for i, v in enumerate(variables)}
        eqs = [eval(eq.replace('^', '**'), {"__builtins__": {}}, local_dict) for eq in equations]

        def compute_groebner():
            return groebner(eqs, *sym_vars, order=self.internal_order, domain=ZZ)

        start_time = time.perf_counter()

        if measure_memory:
            mem_log, basis = memory_usage(compute_groebner, interval=0.1, retval=True)
        else:
            basis = compute_groebner()
            mem_log = []

        elapsed = time.perf_counter() - start_time

        basis_size = len(basis) if basis else None

        result = {
            'test': test_name,
            'method': self.method_name,
            'order': self.order,
            'time': round(elapsed, 3),
            'dimension': dimension,
            'num_vars': len(variables),
            'num_equations': len(eqs),
            'basis_size': basis_size,
            'avr_memory': round(sum(mem_log) / len(mem_log), 2) if mem_log else 0.0,
            'max_memory': round(max(mem_log), 2) if mem_log else 0.0,
            'mem_per_sec': round(max(mem_log) / elapsed, 2) if elapsed > 0 and mem_log else 0.0,
            'mode': 'memory' if measure_memory else 'clean'
        }

        if verbose:
            mem_str = f", {result['max_memory']:.1f} Мб" if measure_memory else ""
            print(
                f" + {test_name} ({self.method_name}, {self.order}): {elapsed:.3f} с{mem_str}, базис: {basis_size} полиномов")

        return result