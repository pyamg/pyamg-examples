import subprocess
import yaml
import os
from glob import glob

branch = 'reorg'

def exectute_demo(exampledir, name='demo.py'):
    """Exectue a demo in a particular directory."""
    output = subprocess.run(['python', f'{name}', '--savefig'],
                            cwd=f'{exampledir}',
                            capture_output=True, text=True)

    figs = glob(os.path.join(f'{exampledir}', 'output') +'/*.png')
    if output.stderr:
        raise ValueError(f'Trouble executing {exampledir} + {name} \n {output.stderr}')
    return output.stdout, figs

mainreadme = 'readme.md'
toc = yaml.safe_load("""
Blackbox Solver:
  - dir: blackbox
Smoothed Aggregation AMG:
  - dir: aggregation
    title: Aggregation
  - dir: one_dimension
    title: One Dimensional Problem
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

tocmd = '### Table of Contents\n'

main = '\n'

for section in toc:

    # add to the TOC
    hrefid = section.replace(' ', '').lower()
    tocmd += f'- **<a href="#{hrefid}">{section}</a>**\n'

    main += f'<a name="{hrefid}"></a>\n'
    main += f'### {section}\n\n'

    if toc[section] is not None:
        for demo in toc[section]:
            title = demo.get('title', None)
            if title:
                main += f'\n#### {title}\n\n'

            demoname = demo.get('demo', 'demo.py')
            main += f'[{demoname}](https://github.com/pyamg/pyamg-examples/blob/master/{demo["dir"]}/{demoname})\n\n'
            # get the readme
            with open(os.path.join(f"{demo['dir']}",'readme.md'), 'r') as f:
                readmeoutput = f.read()
            main += readmeoutput

            # get the demo output
            output, figs = exectute_demo(demo['dir'], name=demoname)
            if len(output) > 0:
                main += '\n```\n' + output + '```\n'

            for fig in figs:
                main += f'\n<img src="./{fig}" width="300"/>\n\n'
    main += '\n***\n\n'

with open(mainreadme, 'w') as f:
    f.write(header + tocmd + main)
