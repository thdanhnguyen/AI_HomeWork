import collections
import collections.abc

# Patch cho Python 3.10+
if not hasattr(collections, "Iterator"):
    collections.Iterator = collections.abc.Iterator
if not hasattr(collections, "Hashable"):
    collections.Hashable = collections.abc.Hashable

from kanren import run, var, facts
from kanren.core import lall
from kanren.assoccomm import eq_assoccomm as eq_assoc
from kanren.assoccomm import commutative, associative

add = "add"
mul = "mul"

a, b, c = var("a"), var("b"), var("c")

facts(commutative, (add,), (mul,))
facts(associative, (add,), (mul,))


# trong file
print("\n=== Test Case của Đề ===")
# (3 * -2) + ((1 + (2 * 3)) * -1) = -13
expr_orig = (add, (mul, 3, -2), (mul, (add, 1, (mul, 2, 3)), -1))

expr1 = (add, (mul, (add, 1, (mul, 2, a)), b), (mul, 3, c))
expr2 = (add, (mul, c, 3), (mul, b, (add, (mul, 2, a), 1)))
expr3 = (add, (add, (mul, (mul, 2, a), b), b), (mul, 3, c))

print("Expression 1 matches:", run(0, (a, b, c), eq_assoc(expr1, expr_orig)))
print("Expression 2 matches:", run(0, (a, b, c), eq_assoc(expr2, expr_orig)))
print("Expression 3 matches:", run(0, (a, b, c), eq_assoc(expr3, expr_orig)))

# bài toán thêm
print("\n=== Test Case 2 ===")

x, y, z = var('x'), var('y'), var('z')

# (2 * 3) + ((1 + (2 * 2)) * -1) = 6 + (5 * -1) = 1
test_orig2 = (add, (mul, 2, 3), (mul, (add, 1, (mul, 2, 2)), -1))

test1 = (add, (mul, (add, 1, (mul, 2, x)), y), (mul, 3, z)) 
test2 = (add, (mul, z, 3), (mul, y, (add, (mul, 2, x), 1))) 
test3 = (add, (add, (mul, (mul, 2, x), y), y), (mul, 3, z))

print("Test 1 matches:", run(0, (x, y, z), eq_assoc(test1, test_orig2)))
print("Test 2 matches:", run(0, (x, y, z), eq_assoc(test2, test_orig2)))
print("Test 3 matches:", run(0, (x, y, z), eq_assoc(test3, test_orig2)))
