import sys
from Net import Net

def node_input(non_unique_list):
    nodes_list = []
    for number in non_unique_list:
        if any(x.node == number for x in nodes_list):
            net = Net()
            net.node = number
            nodes_list.append(net)
    return nodes_list

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
print(left_node_number)
left = node_input(link_left)
right_node_number = unique(link_right)
print(right_node_number)
right = node_input(link_right)
