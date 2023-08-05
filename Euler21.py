import numpy as np


def divisors(n):
    # Return list of proper divisors of integer n
    limit = int(np.ceil(np.sqrt(n)))  # search until limit
    factors = [1]  # 1 is always a divisor
    for i in np.arange(2, limit + 1):
        if np.mod(n, i) == 0:
            factors.extend([i, n // i])
    factor_arr = np.array(factors, dtype=int)
    # factor_arr_uniq = np.unique(factor_arr)

    return factor_arr


def sum_divisors(n):
    # return sum of the proper divisors of n
    div_array = divisors(n)
    div_sum = np.sum(div_array)
    return div_sum


limit = 10000  # how high to check for the numbers. In the problem, this is 10000

input_list = np.arange(0, limit+1, dtype=int)
np_sum_divisors = np.vectorize(sum_divisors)
divisors_list = np_sum_divisors(input_list)

#amic_arr1 has input value in first column and divisor sum in second
amic_arr1 = np.column_stack((input_list,divisors_list))
#amic_arr2 is flipped from 1
amic_arr2 = np.fliplr(amic_arr1)

sum_amic = 0
for index, numbers in enumerate(amic_arr1):
    input_num = index  # since we start at 0, the index is equal to the input num
    sum_div = amic_arr1[index][1]
    if sum_div <= limit and index != sum_div:
        if amic_arr2[sum_div][0] == index:
            sum_amic += index

print(sum_amic)








