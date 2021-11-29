# Alpino Query

```bash
pip install alpino-query
```

When running locally without installing, instead of `alpino-query` use `python -m alpino_query`.

## Mark

Mark which part of the treebank should selected for filtering. It has three inputs:

1. [Lassy/Alpino XML](https://www.let.rug.nl/~vannoord/Lassy/)
2. the tokens of the sentence
3. for each token specify the properties which should be marked

For example:

```bash
alpino-query mark "$(<tests/data/001.xml)" "Dit is een voorbeeldzin ." "pos pos pos pos pos"
```

It is also possible to mark multiple properties for a token, this is done by separating them with a comma. Each of these can also be specified to be negated. These will then be marked as 'exclude' in the tree.

```bash
alpino-query mark "$(<tests/data/001.xml)" "Dit is een voorbeeldzin ." "pos pos,-word,rel pos pos pos"
```

## Subtree and XPath

```bash
alpino-query subtree "$(<tests/data/001.marked.xml)" cat
alpino-query xpath "$(<tests/data/001.subtree.xml)" 0
```

## Using as Module

```python
from alpino_query import AlpinoQuery

alpino_xml = "<Alpino xml as string>"
tokens = ["Dit", "is", "een", "voorbeeldzin", "."]
attributes = ["pos", "pos,-word,rel", "pos", "pos", "pos"]

query = AlpinoQuery()
query.mark(alpino_xml, tokens, attributes)
print(query.marked_xml) # query.marked contains the lxml Element

query.generate_subtree(["rel", "cat"])
print(query.subtree_xml) # query.subtree contains the lxml Element

query.generate_xpath(False) # True to make order sensitive
print(query.xpath)
```

## Considerations

### Exclusive
When querying a node this could be exclusive in multiple ways.
For example:

* a node should not be a noun `node[@pos!="noun"]`
* it should not have a node which is a noun `not(node[@pos="noun"])`

The first statement does *require* the existence of a node, whereas the second also holds true if there is no node at all. When a token is only exclusive (e.g. not a noun) a query of the second form will be generated, if a token has both inclusive and exclusive properties a query of the first form will be generated.

### Relations

`@cat` and `@rel` are always preserved for nodes which have children. The only way for this to be dropped is for when all the children are removed by specifying the `na` property for the child tokens.

## Upload to PyPi

```bash
pip install twine
python setup.py sdist
twine upload dist/*
```
