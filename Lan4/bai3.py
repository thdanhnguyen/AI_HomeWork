import json
import collections
import collections.abc

# Patch cho Python 3.10+
if not hasattr(collections, "Iterator"):
    collections.Iterator = collections.abc.Iterator
if not hasattr(collections, "Hashable"):
    collections.Hashable = collections.abc.Hashable

from kanren import Relation, facts, run, var, conde, lall

# Định nghĩa các quan hệ
father = Relation()
mother = Relation()

# Hàm tạo quan hệ parent từ father và mother
def parent(x, y):
    return conde([father(x, y)], [mother(x, y)])

# Quan hệ ông bà
def grandparent(x, z):
    y = var()
    return lall(parent(x, y), parent(y, z))

# Quan hệ anh chị em
def sibling(x, y):
    p = var()
    return conde([parent(p, x), parent(p, y)])

# Quan hệ chú bác (anh em của cha)
def uncle(x, z):
    f = var()
    return lall(father(f, z), sibling(x, f))

if __name__ == '__main__':
    # Đọc dữ liệu từ file JSON
    with open('family.json') as f:
        d = json.load(f)

    # Nạp dữ liệu vào facts
    for item in d['father']:
        for k, v in item.items():
            facts(father, (k, v))
    for item in d['mother']:
        for k, v in item.items():
            facts(mother, (k, v))

    # Khai báo biến logic
    x, husband, wife, child = var(), var(), var(), var()

    # 1. Tìm tất cả con của John
    name = 'John'
    output = run(0, x, father(name, x))
    print(f"\nCác con của {name}:")
    for item in output:
        print(item)

    # 2. Tìm mẹ của William
    name = 'William'
    output = run(0, x, mother(x, name))
    print(f"\nMẹ của {name} là:")
    for item in output:
        print(item)

    # 3. Tìm cha mẹ của Adam
    name = 'Adam'
    output = run(0, x, parent(x, name))
    print(f"\nCha mẹ của {name}:")
    for item in output:
        print(item)

    # 4. Tìm ông bà của Wayne
    name = 'Wayne'
    output = run(0, x, grandparent(x, name))
    print(f"\nÔng bà của {name}:")
    for item in output:
        print(item)

    # 5. Tìm anh chị em của David
    name = 'David'
    output = run(0, x, sibling(x, name))
    siblings = [person for person in output if person != name]
    print(f"\nAnh chị em của {name}:")
    for item in siblings:
        print(item)

    # 6. Tìm chú bác của Tiffany
    name = 'Tiffany'
    name_father = run(1, x, father(x, name))
    output = run(0, x, uncle(x, name))
    uncles = [person for person in output if person not in name_father]
    print(f"\nCác chú bác của {name}:")
    for item in uncles:
        print(item)

    # 7. Liệt kê tất cả các cặp vợ chồng
    output = run(0, (husband, wife), (father, husband, child), (mother, wife, child))
    print("\nDanh sách các cặp vợ chồng:")
    for h, w in set(output):
        print(f'Chồng: {h} <==> Vợ: {w}')
