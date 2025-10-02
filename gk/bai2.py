
from kanren import Relation, facts, run, var, conde, lall, eq


parent = Relation()
bloodbrother = Relation()

facts(parent, ("John", "Jack"), ("John", "Cathy"))
facts(bloodbrother, ("Cathy", "Jonas"))

x, y, z = var(), var(), var()
print("✅ Quan hệ cha mẹ sau suy luận:")

for father, child in set(run(0, (x, y), conde([parent(x, y)], [lall(parent(x, z), bloodbrother(z, y))]))):
    print(f"{father} là cha/mẹ của {child}")

print("\n✅ Quan hệ anh em ruột sau suy luận:")

brother_pairs = set(run(0, (y, z), conde([
    bloodbrother(y, z)],
    [lall(parent(x, y), parent(x, z))],
    [bloodbrother(z, y)]
)))
for bro1, bro2 in brother_pairs:
    if bro1 != bro2:
        print(f"{bro1} là anh/em ruột của {bro2}")

# Ai là bố của Jonas?
f = var()
fathers_of_jonas = run(0, f, conde([parent(f, "Jonas")], [lall(parent(f, z), bloodbrother(z, "Jonas"))]))
if fathers_of_jonas:
    print("\n Bố của Jonas là:", fathers_of_jonas[0])
else:
    print("\nKhông tìm thấy thông tin về bố của Jonas!")
