import sys
from Net import Net

def heat_diffusion(center, proj):
    for c in center:
        for d in range(0, c.degree):
            index = BinarySearch(proj, c.neighbor[d])
            c.value += (proj[index].degree - 1)

    for c in center:
        for d in range(0, c.degree):
            index = BinarySearch(proj, c.neighbor[d])
            proj[index].value += (c.value / c.degree)

    for c in center:
        c.value = 0

    for p in proj:
        for d in range(0, p.degree):
            index = BinarySearch(center, p.neighbor[d])
            center[index].value += (p.value / p.degree)

    for p in proj:
        p.value = 0


def BinarySearch(ar, key):
    Lower = 0
    Upper = len(ar) - 1

    while True:
        Mid = int((Upper + Lower) / 2)
        if ar[Mid].node == key:
            return Mid
        if ar[Mid].node > key:
            Upper = Mid - 1
        else:
            Lower = Mid + 1
        if Upper < Lower:
            return -1

def network_making(link_left, link_right, left, right):
    assert len(link_left) == len(link_right)

    for link_l, link_r in zip(link_left, link_right):
        net_index = BinarySearch(left, link_l);
        left[net_index].neighbor.append(link_r);
        left[net_index].degree += 1

        net_index = BinarySearch(right, link_r);
        right[net_index].neighbor.append(link_l);
        right[net_index].degree += 1

def node_input(non_unique_list):
    unique_list = set(non_unique_list)
    size = len(unique_list)
    net_list = [Net() for i in range(size)]
    for number, net in zip(unique_list, net_list):
        net.node = number
    return sorted(net_list, key=lambda net: net.node)


number_recommend=sys.argv[1] if len(sys.argv) > 1 else 0

file = open('training.txt', 'r')
link_left = []
link_right = []
purchase_date = []
for line in file:
    line = line.split()
    link_left.append(int(line[0]))
    link_right.append(int(line[1]))
    purchase_date.append(int(line[2]))

left = node_input(link_left)
right = node_input(link_right)

#left_node_number = len(left)
#right_node_number = len(right)

#tests
# a = open('test_link_left.txt', 'w')
# for line in link_left:
#     a.write(line)
#     a.write('\n')
#
# b = open('test_left.txt', 'w')
# for line in left:
#     b.write(line.node)
#     b.write('\n')
#
# c = open('test_link_right.txt', 'w')
# for line in link_right:
#     c.write(line)
#     c.write('\n')
#
# d = open('test_right.txt', 'w')
# for line in right:
#     d.write(line.node)
#     d.write('\n')

network_making(link_left, link_right, left, right)

# e = open('test_left_after_network_making.txt', 'w')
# for line in left:
#     e.write(str(line.degree))
#     e.write('\n')
#
# f = open('test_right_after_network_making.txt', 'w')
# for line in right:
#     f.write(str(line.degree))
#     f.write('\n')

heat_diffusion(right, left)

g = open('test_left_after_heat_diffusion.txt', 'w')
for line in left:
    g.write(str(line.value))
    g.write('\n')

h = open('test_right_after_heat_diffusion.txt', 'w')
for line in right:
    h.write(str(line.value))
    h.write('\n')