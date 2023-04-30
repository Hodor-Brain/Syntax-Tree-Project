from django.db import models
from nltk.tree import *
import itertools


def next_position(pos):
    return pos[:len(pos) - 1] + (pos[len(pos) - 1] + 1,)


def rebuild_tree(tree):
    return ParentedTree.fromstring(str(tree))


def tree_to_string(tree):
    return ' '.join(str(tree).split())


class TreeParaphrase:
    def __init__(self, tree_string, limit=20, separators=(',', 'CC'), labels=('NP',)):
        self.ptree = ParentedTree.convert(Tree.fromstring(tree_string))
        self.limit = limit
        self.separators = separators
        self.labels = labels
        self.reached_positions = {}

    def paraphrase(self, ):
        positions = self.ptree.treepositions()
        result = [self.ptree]

        for pos in positions:
            if pos in self.reached_positions:
                continue

            self.reached_positions[pos] = True
            ptree_cur = self.ptree[pos]

            if type(ptree_cur) == ParentedTree and ptree_cur.label() in self.labels:
                found_phrases, found_positions = self.find_noun_phrases(ptree_cur.right_sibling(), next_position(pos))
                noun_phrases = [ptree_cur] + found_phrases
                noun_positions = [pos] + found_positions

                if len(noun_phrases) > 1:
                    permutations = list(itertools.permutations(noun_phrases))
                    result = self.make_paraphrases(result, permutations, noun_positions)

        self.reached_positions = {}
        return result

    def find_noun_phrases(self, current_node, current_pos):
        phrases, positions = [], []
        cur = current_node
        cur_pos = current_pos

        while type(cur) == ParentedTree and cur.label() in self.separators:
            self.reached_positions[cur_pos] = True
            cur = cur.right_sibling()
            cur_pos = next_position(cur_pos)

            if type(cur) == ParentedTree and cur.label() in self.labels:
                self.reached_positions[cur_pos] = True
                phrases.append(cur)
                positions.append(cur_pos)

                cur = cur.right_sibling()
                cur_pos = next_position(cur_pos)

        return phrases, positions

    def make_paraphrases(self, trees, permutations, noun_positions):
        result = []

        for tree in trees:
            for permutation in permutations:
                if len(result) == self.limit:
                    break

                tree_copy = tree.copy(deep=True)
                for i in range(len(permutation)):
                    tree_copy[noun_positions[i]] = rebuild_tree(permutation[i])
                result.append(tree_copy)

        return result
