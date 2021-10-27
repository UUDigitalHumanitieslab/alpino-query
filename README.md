```bash
cd alpino_query
python marker.py "$(<../tests/voorbeeldzin.xml)" "Dit is een voorbeeldzin ." "pos pos pos pos pos"
python subtree.py "$(<../tests/voorbeeldzin-marked.xml)" cat
python xpath_generator.py "$(<../tests/voorbeeldzin-subtree.xml)" 0
```
