```bash
cd alpino_query
```

# Mark

Mark which part of the treebank should selected for filtering. It has three inputs:
1 - [Lassy/Alpino XML](https://www.let.rug.nl/~vannoord/Lassy/)
2 - the tokens of the sentence
3 - for each token specify the properties which should be marked

For example:

```bash
python marker.py "$(<../tests/voorbeeldzin.xml)" "Dit is een voorbeeldzin ." "pos pos pos pos pos"
```

It is also possible to mark multiple properties for a token, this is done by separating them with a comma. Each of these can also be specified to be negated. These will then be marked as 'exclude' in the tree.

```bash
python marker.py "$(<../tests/voorbeeldzin.xml)" "Dit is een voorbeeldzin ." "pos pos,-word,rel pos pos pos"
```

# Subtree

```bash
python subtree.py "$(<../tests/voorbeeldzin-marked.xml)" cat
python xpath_generator.py "$(<../tests/voorbeeldzin-subtree.xml)" 0
```

# Considerations

## Exclusive
When querying a node this could be exclusive in multiple ways.
For example:

* a node should not be a noun `node[@pos!="noun"]`
* it should not have a node which is a noun `not(node[@pos="noun"])`

The first statement does *require* the existence of a node, whereas the second also holds true if there is no node at all. When a token is only exclusive (e.g. not a noun) a query of the second form will be generated, if a token has both inclusive and exclusive properties a query of the first form will be generated.

## Relations

`@cat` and `@rel` are always preserved for nodes which have children. The only way for this to be dropped is for when all the children are removed by specifying the `na` property for the child tokens.
