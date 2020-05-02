#!/usr/bin/env python3

import json
import os
from pathlib import Path
import pystache
import shutil
import sys

def regenerateSite(configFile):
    siteConfig = json.load(open(configFile, 'r'))
    pages = siteConfig['pages']
    copyDirs = siteConfig['copyDirs']
    outputDir = Path(siteConfig['outputDir'])
    renderer = pystache.Renderer()

    os.mkdir(outputDir)

    for dir in copyDirs:
        print('copying directory', dir)
        dirPath = Path(dir)
        shutil.copytree(dirPath, outputDir / dir)

    for pageConfig in pages:
        pageContext = json.load(open(Path(pageConfig['context'])))
        filename = outputDir / Path(pageConfig['outputPath'])
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        outputFile = open(filename, 'w')
        renderedContent = renderer.render_path(Path(pageConfig['template']), pageContext)
        outputFile.write(renderer.render(renderedContent))
        outputFile.close()
        print('created page', filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please provide the name of a configuration file.')
        print('Usage: sitestrap.py site.json')
        sys.exit(1)
    regenerateSite(sys.argv[1])
