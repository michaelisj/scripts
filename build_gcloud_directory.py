import argparse
import json
import logging
import os
import shutil
from urllib.parse import urlparse


class BuildFileSystem:
    def __init__(self, jsonPath, baseDir, targetDirectory):
        assert os.path.isfile(jsonPath), '{} is not a file'.format(jsonPath)
        assert os.path.isdir(baseDir), '{} is not a directory'.format(baseDir)

        if not os.path.isdir(targetDirectory):
            os.makedirs(targetDirectory)

        self.baseDir = baseDir
        self.targetDirectory = targetDirectory
        self.jsonContent = try_parse_json(jsonPath)

    def build(self):
        for fileName, paramsDict in self.jsonContent.items():
            self.parse_content(fileName, paramsDict)

    @staticmethod
    def extract_params(fileName, paramsDict):
        params = urlparse(paramsDict['sourceUrl'])
        path = os.path.split(params.path)[-1]
        return list(os.path.split(fileName)) + [path]

    def parse_content(self, fileName, paramsDict):
        targetDirectory, targetFileName, sourceFileName = self.extract_params(
            fileName, paramsDict)

        targetDirectory = os.path.join(self.targetDirectory, targetDirectory)
        if not os.path.isdir(targetDirectory):
            os.makedirs(targetDirectory)

        targetFileName = os.path.join(targetDirectory, targetFileName)
        sourceFileName = os.path.join(self.baseDir, sourceFileName)
        if os.path.isfile(sourceFileName):
            shutil.copy(sourceFileName, targetFileName)
        else:
            logging.warning("%s is not a file; target file name: %s",
                            sourceFileName, targetFileName)


def try_parse_json(filePath):
    with open(filePath) as jsonFile:
        content = jsonFile.read()

    return json.loads(content)


def main():
    builder = BuildFileSystem(
        args.config_file, args.base_directory, args.target_directory)
    builder.build()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='json configuration file')
    parser.add_argument('base_directory', help='json configuration file')
    parser.add_argument('--target-directory', '-t',
                        default='.', help='Target directory')

    args = parser.parse_args()
    try:
        main()
    except Exception as e:
        logging.exception(e)
