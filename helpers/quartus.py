"""
********************************************************************************
* SPDX-License-Identifier: MIT
* SPDX-FileType: OTHER
* SPDX-FileCopyrightText: (c) 2024, OpenGateware authors and contributors
********************************************************************************
*
* Intel Quartus Compilation Flow
* Copyright (c) 2024, Marcus Andrade <marcus@opengateware.org>
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
********************************************************************************
"""

import os

from python_on_whales import DockerException, docker


def run_quartus_compile(config):
    """
    Compiles a Quartus project using Docker.

    This function takes a configuration dictionary, extracts the project name and target platform,
    and constructs a command to compile the project using the Quartus command-line tools inside a Docker container.
    The Docker container used for compilation is determined by the target platform.

    Parameters:
    - config (dict): A configuration dictionary that must contain at least a 'name' key, which is used
                     to construct the path to the Quartus project file (.qpf).

    Environment Variables:
    - TARGET: The target platform for the Quartus compilation. This determines the Docker image to use.
              The value of TARGET is appended to 'raetro/quartus:' to form the Docker image name.
    - GITHUB_WORKSPACE: The root directory of the GitHub workspace. This directory is mounted to the
                        Docker container to allow access to the project files.

    The function streams the output of the Docker command to stdout. In case of a Docker-related error,
    it catches the exception and prints the error message along with the Docker command and exit code.

    Exceptions:
    - DockerException: If a Docker-related error occurs, the function will catch this exception, print
                       an error message containing the Docker command and exit code, and then re-raise the exception.

    Returns:
    - None: This function does not return a value. It prints the output of the compilation process to stdout.
    """
    target = os.getenv('TARGET')
    workspace = os.getenv("GITHUB_WORKSPACE")
    qpf = f"projects/{config['name']}_{target}.qpf"

    image = f"raetro/quartus:{target}"
    cmd = f"quartus_sh --flow compile {qpf}"
    try:
        output = docker.run(
                image,
                ["sh", "-c", cmd],
                volumes=[(f"{workspace}", "/build")],
                remove=True,
                stream=True,
                name=f"{target}"
        )

        for stream_content in output:
            print(stream_content)

        print("Done")
    except DockerException as e:
        print(f"Exit code {e.return_code} while running {e.docker_command}")
