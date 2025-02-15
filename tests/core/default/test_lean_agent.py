import pytest
import tempfile
from gpt_engineer.core.ai import AI
from gpt_engineer.core.default.lean_agent import LeanAgent
from gpt_engineer.core.code import Code
import os
from tests.caching_ai import CachingAI

from gpt_engineer.core.chat_to_files import parse_chat, Edit, parse_edits, apply_edits
from gpt_engineer.core.chat_to_files import logger as parse_logger
import logging


def test_init():
    temp_dir = tempfile.mkdtemp()

    lean_agent = LeanAgent.with_default_config(temp_dir, CachingAI())
    outfile = "output.txt"
    file_path = os.path.join(temp_dir, outfile)
    code = lean_agent.init(
        f"Make a program that prints 'Hello World!' to a file called '{outfile}'"
    )
    assert os.path.isfile(file_path)
    with open(file_path, "r") as file:
        assert file.read().strip() == "Hello World!"


def test_improve():
    temp_dir = tempfile.mkdtemp()
    code = Code(
        {
            "main.py": "def write_hello_world_to_file(filename):\n    \"\"\"\n    Writes 'Hello World!' to the specified file.\n    \n    :param filename: The name of the file to write to.\n    \"\"\"\n    with open(filename, 'w') as file:\n        file.write('Hello World!')\n\nif __name__ == \"__main__\":\n    output_filename = 'output.txt'\n    write_hello_world_to_file(output_filename)",
            "requirements.txt": "# No dependencies required",
            "run.sh": "python3 main.py\n",
        }
    )
    lean_agent = LeanAgent.with_default_config(temp_dir, CachingAI())
    lean_agent.improve(
        code,
        "Change the program so that it prints '!dlroW olleH' instead of 'Hello World!'",
    )
    outfile = "output.txt"
    file_path = os.path.join(temp_dir, outfile)
    assert os.path.isfile(file_path)
    with open(file_path, "r") as file:
        file_content = file.read().strip()
        assert file_content == "!dlroW olleH"


if __name__ == "__main__":
    pytest.main()
