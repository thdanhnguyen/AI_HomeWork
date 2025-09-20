from kanren import run, var, membero, eq
from kanren.core import lall

# Khai báo biến
people = var()

# Định nghĩa luật (rules)
rules = lall(
    # Có 4 người
    (eq, (var(), var(), var(), var()), people),

    # Steve có xe màu blue
    (membero, ('Steve', var(), 'blue', var()), people),

    # Người nuôi cat sống ở Canada
    (membero, (var(), 'cat', var(), 'Canada'), people),

    # Matthew sống ở USA
    (membero, ('Matthew', var(), var(), 'USA'), people),

    # Người có xe màu black sống ở Australia
    (membero, (var(), var(), 'black', 'Australia'), people),

    # Jack có cat
    (membero, ('Jack', 'cat', var(), var()), people),

    # Alfred sống ở Australia
    (membero, ('Alfred', var(), var(), 'Australia'), people),

    # Người có dog sống ở France
    (membero, (var(), 'dog', var(), 'France'), people),

    # Một người trong nhóm có rabbit
    (membero, (var(), 'rabbit', var(), var()), people)
)

# Chạy solver
solutions = run(0, people, rules)

if solutions:
    # Tìm người có rabbit
    rabbit_owner = [person for person in solutions[0] if person[1] == 'rabbit'][0][0]

    print(f"\n{rabbit_owner} is the owner of the rabbit\n")
    print("Here are all the details:")
    attribs = ['Name', 'Pet', 'Color', 'Country']
    print('\t\t'.join(attribs))
    print('-' * 50)
    for item in solutions[0]:
        print('\t\t'.join([str(x) for x in item]))
else:
    print("No solution found.")
