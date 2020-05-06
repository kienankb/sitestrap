#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path
import pystache
import shutil
import sys

def regenerateSite(configFile, overwrite):
    siteConfig = json.load(open(configFile, 'r'))
    pages = siteConfig['pages']
    copyDirs = siteConfig['copyDirs']
    outputDir = Path(siteConfig['outputDir'])
    renderer = pystache.Renderer()

    try:
        os.mkdir(outputDir)
        print('created output directory')
    except FileExistsError:
        if not overwrite:
            print('the output directory already exists and neither -f nor --force were specified, exiting')
            sys.exit(1)
        else:
            print('removing existing output directory')
            shutil.rmtree(outputDir)
            os.mkdir(outputDir)
            print('created output directory')

    for dir in copyDirs:
        print('copying directory:', dir)
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
        print('rendered page:', filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a static site.')
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        dest='overwrite',
        required=False,
        default=False,
        help='wipe and rewrite the output directory if it exists')
    parser.add_argument(
        'config',
        help='The config JSON file to be used.')
    args = parser.parse_args()
    regenerateSite(args.config, args.overwrite)
