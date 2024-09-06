import subprocess
import yaml
import os
import sys
from glob import glob

def execute_demo(exampledir, name='demo.py'):
    """Exectue a demo in a particular directory."""
    nameall = name.split()
    output = subprocess.run(['python3'] + nameall + ['--savefig'],
                            cwd=f'{exampledir}',
                            capture_output=True, text=True)

    if output.stderr:
        raise ValueError(f'Trouble executing {exampledir} + {name} \n {output.stderr}')
    return output.stdout

mainreadme = 'readme.md'
toc = yaml.safe_load("""
Introduction:
  - dir: 0_start_here
    title: Overview
Blackbox Solver:
  - dir: blackbox
Smoothed Aggregation AMG:
  - dir: aggregation
    title: Aggregation
  - dir: one_dimension
    title: One Dimensional Problem
  - dir: visualizing_aggregation
    title: Visualizing Aggregation
    demo: demo1.py, demo2.py
  - dir: solver_diagnostics
    title: Solver Diagnostics
    demo: demo.py --matrix 2
  - dir: complex
    title: Complex Arithmetic
    demo: demo.py --solver 1
  - dir: nonsymmetric
    title: Nonsymmetric example
    demo: demo.py --solver 1
Classical AMG:
  - dir: coarse_fine_splitting
    title: Coarse Fine Splitting
  - dir: compatible_relaxation
    title: Compatible Relaxation
  - dir: strength_options
    title: Stength of Connection
  - dir: air
    title: Approximate ideal restriction (AIR)
Rootnode AMG:
  - dir: rootnode
    title: Rootnode AMG
Finite Elements:
  - dir: diffusion
    title: Anisotropic Diffusion
  - dir: linear_elasticity
    title: Linear Elasticity
    demo: demo.py --solver 2
Preconditioning:
  - dir: preconditioning
    title: Krylov Methods
    demo: demo.py --solver 1
  - dir: eigensolver
    title: Eigenvalue Solvers
Other Applications:
  - dir: mesh_partition
    title: Graph Partitioning
  - dir: helmholtz
    title: Indefinite Helmholtz
    demo: demo1d.py, demo2d.py
  - dir: diffusion_dg
    title: High-Order DG on Poisson
  - dir: edge_amg
    title: Edge-based AMG
Other:
  - dir: profile_pyamg
    title: Profiling Performance
  - dir: performance
    title: Scaling performance of AMG and FE assembly
""")

# generate table and header
header = \
"""This is a collection of short examples for [PyAMG](https://github.com/pyamg/pyamg).
The source code for these **(and more)** examples is available at
https://github.com/pyamg/pyamg-examples.

"""

tocmd = '### Table of Contents\n'

main = '\n'

dirs = None
if len(sys.argv) > 1:
    dirs = sys.argv[1:]
    for d in dirs:
        found = False
        for section in toc:
            for demo in toc[section]:
                if d == demo['dir']:
                    found = True
        if not found or not os.path.isdir(d):
            print('usage: runner.py')
            print('usage: runner.py dir1 [dir2] ...')
            exit()

for section in toc:

    # add to the TOC
    hrefid = section.replace(' ', '').lower()
    tocmd += f'- **<a href="#{hrefid}">{section}</a>**\n'

    main += f'<a name="{hrefid}"></a>\n'
    main += f'### {section}\n\n'

    if toc[section] is not None:
        for demo in toc[section]:
            print(f'Processing {demo["dir"]}.', end=' ')
            title = demo.get('title', None)
            if title:
                hrefid = title.replace(' ', '').lower()
                tocmd += f'  - <a href="#{hrefid}">{title}</a>\n'
                main += f'<a name="{hrefid}"></a>\n'
                main += f'\n#### {title}\n\n'

            demonames = [d.strip() for d in demo.get('demo', 'demo.py').split(',')]
            for demoname in demonames:
                main += f'[{demoname}](./{demo["dir"]}/{demoname.split()[0]})\n\n'
            # get the readme
            with open(os.path.join(f"{demo['dir']}",'readme.md'), 'r') as f:
                readmeoutput = f.read()
            main += readmeoutput

            # get the demo output
            runit = True
            if dirs is not None:
                if demo['dir'] not in dirs:
                    runit = False
                    print('')
            if runit:
                print('[--->rerunning]')
            for demoname in demonames:
                if runit:
                    output = execute_demo(demo['dir'], name=demoname)
                    if len(output) > 0:
                        main += '\n```\n' + output + '```\n'

            # get the output figs
            figs = glob(os.path.join(f'{demo["dir"]}', 'output') +'/*.png')
            for fig in figs:
                main += f'\n<img src="./{fig}" width="300"/>\n\n'
    main += '\n***\n\n'

with open(mainreadme, 'w') as f:
    f.write(header + tocmd + main)
