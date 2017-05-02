import sys
from bisect import bisect_left

class Net:
    def __init__(self, _node = 0):
        self.node = _node
        self.degree = 0
        self.neighbor = []
        self.value = 0.0

    def __lt__(self, other):
        return self.node < other.node

def input_for_check(direction):
    link_left, link_right, purchase_date = [], [], []
    with open('check.txt', 'r') as file:
        for line in file:
            line = line.split()
            link_left.append(int(line[0]))
            link_right.append(int(line[1]))
            # purchase_date.append(int(line[2])) #in original C file parameter is passed to network_making but is not used

    left = node_input(link_left)
    right = node_input(link_right)

    network_making(link_left, link_right, left, right)
    size_check = len(left)
    ret_list = right if direction else left
    return ret_list, size_check


def recommendation(user, item_rank):
    expect_collect = 0
    idx = list(range(0, len(item_rank)))

    check, size_check = input_for_check(0)
    result = open('result.txt', 'w')

    rank_temp = item_rank[:]

    quick_sort_dual(idx, rank_temp, len(item_rank))
    rank_seq = rank_temp[:]

    for u in user:
        length = number_recommend
        recommend_table = item_rank[:]

        for i in range(0, u.degree):
            k = binary_search_raw(rank_seq, u.neighbor[i])
            recommend_table[idx[k]] = 0
            length += 1

        k = binary_search_raw([n.node for n in check], u.node)
        if k != -1:
            for i in range(0, check[k].degree):
                l = binary_search_raw(rank_seq, check[k].neighbor[i])
                if l != -1 and idx[l] < length and recommend_table[idx[l]]:
                    expect_collect += 1

        result.write(str(u.node) + '\t')
        for j in range(0, length):
            if recommend_table[j]:
                result.write(str(recommend_table[j]) + '\t')
        result.write('\n')

    print("%s\t%s\n" % (number_recommend, expect_collect))


def quick_sort_dual(ar1, ar2, num, begin = 0):
    if num <= 1:
        return

    key = ar2[begin + num-1]
    left = begin
    right = begin + num - 2
    while True:
        while ar2[left] < key:
            left += 1
        while ar2[right] > key:
            right -= 1
        if left >= right:
            break
        ar1[left], ar1[right] = ar1[right], int(ar1[left])
        ar2[left], ar2[right] = ar2[right], int(ar2[left])
        left += 1
        right -= 1

    ar1[left], ar1[begin + num - 1] = ar1[begin + num - 1], int(ar1[left])
    ar2[left], ar2[begin + num - 1] = ar2[begin + num - 1], int(ar2[left])

    quick_sort_dual(ar1, ar2, left - begin, begin)
    quick_sort_dual(ar1, ar2, num - left + begin - 1, left + 1,)


def ranking(list):
    id, value = [], []

    for l in list:
        id.append(l.node)
        value.append(l.value)

    quick_sort_dual(id, value, len(id))
    return id


def heat_diffusion(center, proj):
    center_nodes = [n.node for n in center]
    proj_nodes = [n.node for n in proj]
    indexes = []
    for c in center:
        for d in range(0, c.degree):
            indexes.append(binary_search_raw(proj_nodes, c.neighbor[d]))
            c.value += (proj[indexes[-1]].degree - 1)

    i = 0
    for c in center:
        for d in range(0, c.degree):
            proj[indexes[i]].value += (c.value / c.degree)
            i += 1

    for c in center:
        c.value = 0

    for p in proj:
        for d in range(0, p.degree):
            index = binary_search_raw(center_nodes, p.neighbor[d])
            center[index].value += (p.value / p.degree)

    for p in proj:
        p.value = 0


def binary_search_raw(ar, key):
    index = bisect_left(ar, key)
    if index != len(ar) and ar[index] == key:
        return index
    return -1


def network_making(link_left, link_right, left, right):
    assert len(link_left) == len(link_right)

    left_nodes = [n.node for n in left]
    right_nodes = [n.node for n in right]

    for link_l, link_r in zip(link_left, link_right):
        net_index = binary_search_raw(left_nodes, link_l)
        left[net_index].neighbor.append(link_r)
        left[net_index].degree += 1

        net_index = binary_search_raw(right_nodes, link_r)
        right[net_index].neighbor.append(link_l)
        right[net_index].degree += 1


def node_input(non_unique_list):
    unique_list = set(non_unique_list)
    net_list = []
    for number in unique_list:
        net_list.append(Net(number))
    return sorted(net_list)

number_recommend = int(sys.argv[1]) if len(sys.argv) > 1 else 0

link_left, link_right, purchase_date = [], [], []
with open('training.txt', 'r') as file:
    for line in file:
        line = line.split()
        link_left.append(int(line[0]))
        link_right.append(int(line[1]))
        #purchase_date.append(int(line[2])) #in original C file parameter is passed to network_making but is not used

left = node_input(link_left)
right = node_input(link_right)

network_making(link_left, link_right, left, right)
heat_diffusion(right, left)
item_rank = ranking(right)
recommendation(left, item_rank)