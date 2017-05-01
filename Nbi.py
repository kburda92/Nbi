import sys
from Net import Net

def input_for_check(size_check, direction):
    file = open('check.txt', 'r')
    link_left, link_right, purchase_date = [], [], []
    for line in file:
        line = line.split()
        link_left.append(int(line[0]))
        link_right.append(int(line[1]))
        purchase_date.append(int(line[2]))

    left = node_input(link_left)
    right = node_input(link_right)

    network_making(link_left, link_right, left, right)

    size_check = len(left)
    return right if direction else left

def recommendation(user, item_rank):
    user_n = len(user)
    rank_n = len(item_rank)
    expect_collect = 0
    size_check = 0
    idx, rank_seq, rank_temp = [], [], []

    check = input_for_check(size_check, 0);

    result = open('result.txt', 'w')

    for i in range(0, rank_n):
        idx.append(i)
        rank_temp.append(item_rank[i])

    QuickSort_dual(idx, rank_temp, rank_n)

    z1 = open('test_id_recommendation.txt', 'w')
    for c in idx:
        z1.write(str(c) + '\n')

    z2 = open('test_rank_temp_recommendation.txt', 'w')
    for c in rank_temp:
        z2.write(str(c) + '\n')

    for temp in rank_temp:
        rank_seq.append(temp)

    for u in user:
        recommend_table = []
        length = number_recommend
        for rank in item_rank:
            recommend_table.append(rank)

        for i in range(0, u.degree):
            k = BinarySearch_raw(rank_seq, u.neighbor[i])
            recommend_table[idx[k]] = 0
            length += 1

        k = BinarySearch(check, u.node)
        if k != -1:
            for i in range(0, check[k].degree):
                l = BinarySearch_raw(rank_seq, check[k].neighbor[i]);
                if l != -1 and idx[l] < length and recommend_table[idx[l]]:
                    expect_collect += 1

        result.write(str(u.node) + '\t')
        for j in range(0, length):
            if recommend_table[j]:
                result.write(str(recommend_table[j]) + '\t')
        result.write('\n')

    print("%s\t%s\n" % (number_recommend, expect_collect))

def QuickSort_dual(ar1, ar2, num, begin = 0):
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

    QuickSort_dual(ar1, ar2, left - begin, begin);
    QuickSort_dual(ar1, ar2, num - left + begin - 1, left + 1,);


def ranking(list):
    id, value = [], []

    for l in list:
        id.append(l.node)
        value.append(l.value)

    QuickSort_dual(id, value, len(id))
    return id;

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

def BinarySearch_raw(ar, key):
    Lower = 0
    Upper = len(ar) - 1

    while True:
        Mid = int((Upper + Lower) / 2)
        if ar[Mid] == key:
            return Mid
        if ar[Mid] > key:
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
link_left, link_right, purchase_date = [], [], []
for line in file:
    line = line.split()
    link_left.append(int(line[0]))
    link_right.append(int(line[1]))
    purchase_date.append(int(line[2]))

left = node_input(link_left)
right = node_input(link_right)

#tests
a = open('test_link_left.txt', 'w')
for line in link_left:
    a.write(str(line) + '\n')

b = open('test_left.txt', 'w')
for line in left:
    b.write(str(line.node) + '\n')

c = open('test_link_right.txt', 'w')
for line in link_right:
    c.write(str(line))
    c.write('\n')

d = open('test_right.txt', 'w')
for line in right:
    d.write(str(line.node) + '\n')

network_making(link_left, link_right, left, right)

e = open('test_left_network_making.txt', 'w')
for line in left:
    e.write(str(line.degree) + '\n')

f = open('test_right_network_making.txt', 'w')
for line in right:
    f.write(str(line.degree) + '\n')

heat_diffusion(right, left)

g = open('test_right_heat_diffusion.txt', 'w')
for line in right:
    g.write('%.10f\n' % (line.value))

item_rank = ranking(right)

h = open('test_right_ranking.txt', 'w')
for item in item_rank:
    h.write(str(item) + '\n')

recommendation(left, item_rank);