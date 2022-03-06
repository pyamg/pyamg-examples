import subprocess
import yaml
import os

def exectute_demo(exampledir, name='demo.py', figure=False):
    """Exectue a demo in a particular directory."""
    demopath = os.path.join(f'{exampledir}', f'{name}')
    output = subprocess.run(['python', demopath],
                            capture_output=True, text=True)

    return output.stdout

mainreadme = 'readme.md'
toc = yaml.safe_load("""
Blackbox Solver:
  - dir: blackbox
Smoothed Aggregation AMG:
Classical AMG:
Rootnode AMG:
Finite Elements:
Preconditioning:
Other Applications:
""")

# generate table and header
header = \
"""This is a collection of short examples for [PyAMG](https://github.com/pyamg/pyamg).
The source code for these **(and more)** examples is available at
https://github.com/pyamg/pyamg-examples.

"""

tocmd = '### Table of Contents'

main = '\n'

for section in toc:

    # add to the TOC
    hrefid = section.replace(' ', '').lower()
    tocmd += f'- **<a href="#{hrefid}">{section}</a>**\n'

    main += f'<a name="{hrefid}"></a>\n'
    main += f'### {section}\n\n'

    if toc[section] is not None:
        for demo in toc[section]:
            demoname = demo.get('demo', 'demo.py')
            main += f'[{demoname}](https://github.com/pyamg/pyamg-examples/blob/master/{demo["dir"]}/{demoname}\n\n'
            # get the readme
            with open(os.path.join(f"{demo['dir']}",'readme.md'), 'r') as f:
                readmeoutput = f.read()
            main += readmeoutput

            # get the demo output
            output = exectute_demo(demo['dir'], name=demoname)
            main += output
    main += '\n***\n\n'

with open(mainreadme, 'w') as f:
    f.write(header + tocmd + main)
