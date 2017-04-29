import sys
from Net import Net

def BinarySearch(ar, key):
    Lower = 0
    Upper = len(ar) - 1

    while True:
        Mid = int((Upper + Lower) / 2)
        if ar[Mid].node == key :
            return Mid
        if ar[Mid].node > key:
            Upper = Mid - 1
        else:
            Lower = Mid + 1
        if Upper < Lower:
            return -1

def network_making(link_left, link_right, left, right):
    assert len(link_left) == len(link_right)
    link_number = len(link_left)

    for i in range(0, link_number):
        net_index = BinarySearch(left, link_left[i]);
        left[net_index].neighbor.append(link_right[i]);

        net_index = BinarySearch(right, link_right[i]);
        right[net_index].neighbor.append(link_left[i]);


def node_input(non_unique_list):
    unique_list = set(non_unique_list)
    size = len(unique_list)
    net_list = [Net() for i in range(size)]
    for number, net in zip(unique_list, net_list):
        net.node = number
    return sorted(net_list, key=lambda net: int(net.node))


number_recommend=sys.argv[1] if len(sys.argv) > 1 else 0

file = open('training.txt', 'r')
link_left = []
link_right = []
purchase_date = []
for line in file:
    line = line.split()
    link_left.append(line[0])
    link_right.append(line[1])
    purchase_date.append(line[2])

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