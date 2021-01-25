# minimax_simple.py: Runs minimax on random boolean game tree of given depth,
# compares observed win probability with theoretical probabilities

import random, math, sys, getopt


# Min algorithm--recursively calls max algorithm on the branches,
# and takes the minimum of whatever those calls return. If we hit the leaves,
# we randomly choose the leaf's value to be either zero or one.
def m_min(depth):
    if depth == 1:
        return min(random.randint(0, 1), random.randint(0, 1))
    else:
        return min(m_max(depth - 1), m_max(depth - 1))


# Max algorithm--recursively calls min algorithm on the branches,
# and takes the minimum of whatever those calls return. If we hit the leaves,
# we randomly choose the leaf's value to be either zero or one.
def m_max(depth):
    if depth == 1:
        return max(random.randint(0, 1), random.randint(0, 1))
    else:
        return max(m_min(depth - 1), m_min(depth - 1))


# Given a depth, recurse uses the recursive relationship derived in my blogpost
# to calculate the probability that Player 1 has a winning strategy in a random
# Formula-Game instance.
def recurse(depth):
    if depth == 1:
        return 1 / 2
    if depth % 2 == 0:
        if depth == 2:
            return 9 / 16
        else:
            val = recurse(depth - 2)
            return math.pow(2 * val - math.pow(val, 2), 2)
    else:
        if depth == 3:
            return 49 / 256
        else:
            val = recurse(depth - 2)
            return math.pow(2 * val - math.pow(val, 2), 2)


def helper_message(exit_code):
    print("minimax_simple.py -d <depth> -i <iterations>")
    sys.exit(exit_code)


# Main method
def main(argv):
    its = 0
    depth = 0

    # We start by taking in arguments from the command line
    try:
        opts, args = getopt.getopt(argv, "hd:i:", ["depth=", "its="])
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
        elif opt in ("-i", "--iterations"):
            its = int(arg)
            if its <= 0:
                print("Iteration count must be a positive integer")
                sys.exit(2)
    tot = 0.0

    # We play the game of given depth its times, calculcating the experimental win probability
    for i in range(its):
        tot += m_max(depth)
    print("Theoretical probability of Player 1 having a winning strategy: " + str(1 - recurse(depth)))
    print("Experimental probability of Player 1 having a winning strategy: " + str(tot / its))


if __name__ == "__main__":
    main(sys.argv[1:])
