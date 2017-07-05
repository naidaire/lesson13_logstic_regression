import os
import json
from argparse import ArgumentParser
from pprint import pprint


def parser(input_ipynb, output_ipynb):

    with open(input_ipynb, 'r') as f:
        d = json.loads(f.read())

    cells = d['cells']

    guide = {
       "cell_type": "markdown",
       "metadata": {},
       "source": []
      }

    source = ["### Lesson Guide\n"]
    for i, cell in enumerate(cells):
        s = cell['source']
        if cell['cell_type'] == 'markdown':
            newlines = []
            for line in s:
                if (line.startswith('## ') or line.startswith('### ')) and not line.startswith('### $$'):
                    toparse = line.split('## ')[1].strip()
                    print toparse
                    parse = ''.join([c for c in toparse.lower()
                                     if c in 'abcdefghijklmnopqrstuvwxyz- '])
                    parse = parse.replace(' ','-')
                    indexer = '- ['+toparse+'](#'+parse+')\n'
                    if line.startswith('### '):
                        indexer = '\t'+indexer
                    source.append(indexer)
                    link = '<a id="'+parse+'"></a>\n'
                    newlines.append(link)
                newlines.append(line)
            d['cells'][i]['source'] = newlines
    guide['source'] = source
    d['cells'].insert(1, guide)

    with open(output_ipynb,'w') as f:
        f.write(json.dumps(d))


if __name__ == "__main__":
    argparser = ArgumentParser(description='Write a lesson guide for an ipython notebook.')
    argparser.add_argument('-i','--input',
                        default=None, type=str, nargs=1,
                        help='Input .ipynb file.')
    argparser.add_argument('-o','--output', default=None,
                        type=str, nargs=1,
                        help='Output .ipynb file.')

    args = argparser.parse_args()

    if args.input is None:
        print 'Must specify an input file.'
    else:
        input_ipynb = args.input[0]
        if args.output is None:
            output_ipynb = input_ipynb
        else:
            output_ipynb = args.output[0]
        parser(input_ipynb, output_ipynb)
