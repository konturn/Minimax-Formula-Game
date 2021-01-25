# Minimax-Formula-Game
Two short Python programs I wrote up which experimentally verified some of my analysis in https://nkontur.com/blog/index.php/2021/01/25/formula-game-using-game-theory-to-analyze-the-probabilistic-features-of-true-quantified-boolean-formulas/. The first program, minimax_simple.py, iteratively runs randomly generated instances of Formula-Game, comparing the experimental probability of Player 1 having an optimal strategy to the theoretical probability via the recursive relation established in my blog post. The second program, minimax_full.py, extends this analysis by providing experimental probabilities that a TQBF instance would be true. This experimental analysis is performed at a given depth for each combination of quantifications. 

A note on intractability. Since there are 2^depth leaves, there are thus 2^(2^depth) combinations of leaf values that must be iterated through. Furthermore, there are 2^depth combinations of quantifications that can be applied to the inner formula. The solver therefore runs minimax on a game tree 2^(2^depth) times, a problem which quickly becomes intractable past depth 4 or so. To ameliorate this issue, I've also provided the option to randomize the leaf values and run minimax a given amount of times. While the probabilities yielded from this method are only approximately correct, this approach extends the feasibility of my program to about depth 12.
