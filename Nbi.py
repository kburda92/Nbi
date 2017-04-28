import sys
from Net import Net

def node_input(non_unique_list):
    unique_list = set(non_unique_list)
    size = len(unique_list)
    net_list = [Net() for i in range(size)]
    for number, net in zip(unique_list, net_list):
        net.node = number

    return sorted(net_list, key=lambda net: net.node)

def unique(non_unique_list):
    return len(set(non_unique_list))

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

left_node_number = unique(link_left)
left = node_input(link_left)
print(left_node_number)
right_node_number = unique(link_right)
right = node_input(link_right)
print(right_node_number)
