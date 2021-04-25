# howto

[![Travis build](https://travis-ci.com/flavienbwk/howto.svg?branch=main)](https://travis-ci.com/flavienbwk/howto)
[![PyPI version](https://badge.fury.io/py/howto-cli.svg)](https://badge.fury.io/py/howto-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Coding Style : Black](https://img.shields.io/badge/code%20style-black-000000.svg)

Howto is a useful tool to design and play tutorials, guides or even stories in your shell.

## Install

```bash
pip3 install howto-cli
```

## Usage

```bash
howto [-h] [-v] file

Multi-scenarios CLI tool for tutorials, guides or stories.

positional arguments:
  file           JSON scenario file path

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debug operations
```

## Creating a scenario

The easiest way of creating your scenario is to get inspired by [examples](./examples).

Most of prompts are based on the [PyInquirer library](https://github.com/CITGuru/PyInquirer). Howto adds the JSON-config feature and several [addons](./cli/howto/addons.py) such as _markdown_ support.

## TODOs

- [ ] Make it possible to save howtos to run them without specifying a scenario file path

  Let's say you have a `cook-a-cake.json` scenario file. Let's save it.

  ```bash
  howto --load ./cook-a-cake.json
  ```

  Now, anywhere on your computer, you can run :

  ```bash
  howto cook-a-cake
  # instead of `howto ./cook-a-cake.json`
  ```
