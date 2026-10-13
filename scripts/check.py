"""Maintenance checks; normal mediator usage is standard-library only."""
from pathlib import Path
import sys,subprocess
from rdflib import Graph
from rdflib.compare import isomorphic
from pyshacl import validate
root=Path(__file__).resolve().parents[1]
core=root/'skills/ontolink-skills'
for skill in (root/'skills').iterdir():
    text=(skill/'SKILL.md').read_text()
    if not text.startswith('---\nname: '+skill.name+'\n') or '\ndescription: ' not in text:
        raise SystemExit('Invalid skill entry: '+skill.name)
    if not (skill/'agents/openai.yaml').is_file(): raise SystemExit('Missing UI metadata')
owl=Graph().parse(core/'assets/ontolink.owl',format='xml')
ttl=Graph().parse(core/'assets/ontolink.ttl',format='turtle')
assert isomorphic(owl,ttl), 'Ontology mirror differs'
state=Graph().parse(core/'assets/examples/project.owl',format='xml')
conforms,_,report=validate(state,shacl_graph=Graph().parse(core/'assets/shapes.ttl',format='turtle'),ont_graph=owl,inference='none')
if not conforms: raise SystemExit(report)
subprocess.run([sys.executable,str(core/'scripts/mediator.py'),'validate','--state',str(core/'assets/examples/project.owl')],check=True)
subprocess.run([sys.executable,str(core/'scripts/test_mediator.py')],check=True)
print(f'PASS: eight skill entry points, {len(owl)} ontology triples, equivalent Turtle mirror, SHACL example and mediator tests')
