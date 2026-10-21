---
title: Notes Regarding `uv` Python Package Pre-installation.
keywords: [computer reference, uv, python, linux, installation]
abstract: Notes regarding how to download Python packages for offline availability, without using them in a current project.
---

Create a new project folder and navigate to it. My projects are in `~/dev`.

* `uv init` creates a new project in the current working directory.
* `uv add requests python_package_name` installs the requested packages in `~/.cache/uv`.

The packages will remain in the cache until running `uv cache clean` which removes unused packages. Otherwise, requesting them in a new project will use the locally availble packages by default.

*I am not certain how versions will be dealt with, or how the packages interact with different versions of Python.*

The project created to download the packages can be immediately deleted.
