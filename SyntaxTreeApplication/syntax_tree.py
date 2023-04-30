from nltk.tree import *
import itertools


def tree_to_string(tree):
    return ' '.join(str(tree).split())


def next_position(pos):
    return pos[:len(pos) - 1] + (pos[len(pos) - 1] + 1,)


def without_parent(tree):
    return ParentedTree.fromstring(str(tree))


def find_noun_phrases(current, current_pos, reached_positions, separators, labels):
    phrases, positions = [], []
    cur = current
    cur_pos = current_pos

    while type(cur) == ParentedTree and cur.label() in separators:
        reached_positions[cur_pos] = True
        cur = cur.right_sibling()
        cur_pos = next_position(cur_pos)

        if type(cur) == ParentedTree and cur.label() in labels:
            reached_positions[cur_pos] = True
            phrases.append(cur)
            positions.append(cur_pos)

            cur = cur.right_sibling()
            cur_pos = next_position(cur_pos)

    return phrases, positions


def make_paraphrases(trees, permutations, noun_positions, limit):
    result = []

    for tree in trees:
        for permutation in permutations:
            if len(result) == limit:
                break

            tree_copy = tree.copy(deep=True)
            for i in range(len(permutation)):
                tree_copy[noun_positions[i]] = without_parent(permutation[i])
            result.append(tree_copy)

    return result


def paraphrase(tree_str, limit=20, separators=(',', 'CC'), labels=('NP',)):
    ptree = ParentedTree.convert(Tree.fromstring(tree_str))
    positions = ptree.treepositions()
    reached_positions = {}

    result = [ptree]

    for pos in positions:
        if pos in reached_positions:
            continue

        reached_positions[pos] = True
        ptree_cur = ptree[pos]

        if type(ptree_cur) == ParentedTree and ptree_cur.label() in labels:
            found_phrases, found_positions = find_noun_phrases(ptree_cur.right_sibling(), next_position(pos),
                                                               reached_positions, separators, labels)
            noun_phrases = [ptree_cur] + found_phrases
            noun_positions = [pos] + found_positions

            if len(noun_phrases) > 1:
                permutations = list(itertools.permutations(noun_phrases))
                result = make_paraphrases(result, permutations, noun_positions, limit)

    return result
