import getopt
import random
import sys

table_values = []


def m_min(depth):
    if depth == 1:
        return min(random.randint(0, 1), random.randint(0, 1))
    else:
        return min(m_max(depth - 1), m_max(depth - 1))


def m_max(depth):
    if depth == 1:
        return max(random.randint(0, 1), random.randint(0, 1))
    else:
        return max(m_min(depth - 1), m_min(depth - 1))


# The quantifier values are stored as an integer where the least
# significant bits up to the depth encode a universal quantification
# if equal to 1 or existential otherwise. The table_values array stores
# the values at the leaves. Once the base of the recursion is hit,
# the path value tells us at which leaf we are headed. The leftmost leaf
# in the tree has path value zero, and the rightmost has path value (1<<depth)-1
def m_min_max(depth, quantifier_values, path):
    if depth == 0:
        p_val = table_values[path]
        return p_val
    else:
        q_val = (1 << (depth - 1)) & quantifier_values
        if q_val:
            return max(m_min_max(depth - 1, quantifier_values, path),
                       m_min_max(depth - 1, quantifier_values, path + (1 << (depth - 1))))
        else:
            return min(m_min_max(depth - 1, quantifier_values, path),
                       m_min_max(depth - 1, quantifier_values, path + (1 << (depth - 1))))


# When we are explicitly calculating probabilities, we need to iterate through
# all possible leaf values. We implement simple addition on the array so that we
# can increment through leaf values by adding
def inc_table(t_val):
    if t_val[len(t_val) - 1] == 0:
        t_val[len(t_val) - 1] = 1
    else:
        t_val[len(t_val) - 1] = 0
        for i in range(len(t_val) - 2, -1, -1):
            if t_val[i] == 0:
                t_val[i] = 1
                break
            else:
                t_val[i] = 0


# In randomization mode, we randomize the table values at each
# iteration
def rand_table(t_val):
    for i in range(len(t_val)):
        t_val[i] = random.randint(0, 1)


# When we print out results, we convert the quantifier_values
# variable to a human-readable string
def quant_val_to_string(quantifier_values, depth):
    quant_string = ""
    for i in range(depth - 1, -1, -1):
        if quantifier_values & 1 << i:
            quant_string += "\u2203"
        else:
            quant_string += "\u2200"
    return quant_string


def helper_message(exit_code):
    print("minimax_full.py -d <depth> -r -i <iterations>")
    sys.exit(exit_code)


# Main function. Note that running with randomization mode is much quicker,
# though it does not guarantee perfectly accurate results
def main(argv):
    randomization_enabled = False
    its = 0
    depth = 0
    try:
        opts, args = getopt.getopt(argv, "hd:ri:", ["depth=", "randomization", "its"])
    except getopt.GetoptError:
        helper_message(2)
    if not len(opts):
        helper_message(2)
    for opt, arg in opts:
        if opt == '-h':
            helper_message(0)
        elif opt in ("-d", "--depth"):
            depth = int(arg)
            if depth <= 0:
                print("Depth must be a positive integer")
                sys.exit(2)
        elif opt in ("-r", "--random"):
            randomization_enabled = True
        elif opt in ("-i", "--iterations"):
            print(arg)
            its = int(arg)
            if its <= 0:
                print("Iteration count must be a positive integer")
                sys.exit(2)
    grand_tot = 0
    print(opts)
    if not randomization_enabled:
        # There are 1<<depth leaves, and so 2^(1<<depth) possible leaf values
        its = ((1 << depth) << (1 << depth))
    global table_values
    table_values = [0] * (1 << depth)
    for quantifier_values in range(1 << depth):
        table_values = [0] * (1 << depth)
        t_val = 0
        tot = 0
        while t_val < its:
            if randomization_enabled:
                rand_table(table_values)
            tot += m_min_max(depth, quantifier_values, 0)
            if not randomization_enabled:
                inc_table(table_values)
            t_val += 1
        quantifier_string = quant_val_to_string(quantifier_values, depth)
        print(
            "Probability of winning strategy given quantifier string " + quantifier_string + ": " + str(
                tot / its))
        grand_tot += tot
    print("Total probability of winning strategy: " + str(grand_tot / (its * (1 << depth))))


if __name__ == '__main__':
    main(sys.argv[1:])
