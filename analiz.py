# Создаем список всех поставщиков и кол-во товара у них в наличии
warenum = int(input("Введите количество поставщиков: "))
warehouses = []
supply = {}
for i in range(warenum):
    warehouse = input("Введите название " + str(i + 1) + "-го поставщика: ")
    supplies = int(input("Введите количество товара у данного поставщика: "))
    warehouses.append(warehouse)
    supply[warehouse] = supplies
print()

# Создаем список всех потребителей и кол-во товара ими требуемого
demandnum = int(input("Введите количество потребителей: "))
demand = {}
projects = []
for i in range(demandnum):
    demands = input("Введите название " + str(i + 1) + "-го потребителя: ")
    units = int(input("Введите количество товара, требуемого данным потребителем: "))
    projects.append(demands)   
    demand[demands] = units
print()

# Создаем матрицу стоимостей
costs = []
for i in range(warenum):
    table = []
    for r in range(demandnum):
        l = int(input("Введите стоимость поставки из " + warehouses[i] + " в " + projects[r] + ": "))
        table.append(l)
    costs.append(table)

# Импортировать библиотеку pulp
from pulp import *

# Превратить матрицу стоимостей в словарь
costs = makeDict([warehouses, projects], costs, 0)


# Создаем переменную, чтобы хранить в ней цель задачи
prob = LpProblem("Проблема поставки", LpMinimize)
# Создаем список всех возможных маршрутов
Routes = [(w, b) for w in warehouses for b in projects]

# Создаем словарь, чтобы хранить в нем маршруты и затраты на него
vars = LpVariable.dicts("Маршрут", (warehouses, projects), 0, None, LpInteger)

# Добавляем минимальную целевую функцию в переменную prob
prob += (
    lpSum([vars[w][b] * costs[w][b] for (w, b) in Routes]),
    "Sum_of_Transporting_Costs",
)

# Ограничения на максимальный объем поставок добавляются в prob для каждого поставщика
for w in warehouses:
    prob += (
        lpSum([vars[w][b] for b in projects]) <= supply[w],
        "Sum_of_Products_out_of_warehouses_%s" % w,
    )

# Минимальные ограничения спроса добавляются в prob для каждого узла потребителя
for b in projects:
    prob += (
        lpSum([vars[w][b] for w in warehouses]) >= demand[b],
        "Sum_of_Products_into_projects%s" % b,
    )

    # Решаем задачу с помощью метода библиотеки
prob.solve()

# Выводим маршруты и единицы товара
for v in prob.variables():
    print(v.name, "=", v.varValue)
    
# Выводим общую стоимость
print("Всего: ", value(prob.objective))
