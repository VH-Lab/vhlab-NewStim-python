# vhlab-NewStim-python

This python repository is designed to interpret data structures and read data files created in the matlab repository [vhlab-NewStim-matlab](https://github.com/VH-Lab/vhlab-NewStim-matlab).

**Note:** This library is intended solely for reading data files and data structures. It does not and will not have the capability to interact with hardware in the way that `vhlab-NewStim-matlab` does.

## Scope

This library reads NewStim data structures; it does not present stimuli.
NewStim's presentation half is built on Psychtoolbox, which exists only for
MATLAB, so a large part of `vhlab-NewStim-matlab` is deliberately not ported
rather than merely unported.

Which MATLAB function has a Python home here, which one is out of scope, and
why, is recorded per function in the
`vhlab_newstim_matlab_python_bridge.yaml` files under `src/vhlab_newstim/`.
Read [`PORTING_INSTRUCTIONS`](PORTING_INSTRUCTIONS) before porting anything;
it explains the convention and the status vocabulary, and `tests/test_bridge.py`
enforces the mechanical half of it.

## Installation

It is recommended to use a virtual environment for installation.

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activate the virtual environment:**

    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

3.  **Install the package:**

    You can install the package in editable mode using pip:

    ```bash
    pip install -e .
    ```

    Or install the dependencies directly if you are just developing:

    ```bash
    pip install -r requirements.txt # if provided
    # or just
    pip install .[test]
    ```

## Running Unit Tests

This project uses `pytest` for unit testing.

1.  **Ensure you have installed the package (or test dependencies):**

    If you installed with `pip install -e .`, make sure `pytest` is available. If not, install it:

    ```bash
    pip install pytest
    ```

2.  **Run the tests:**

    From the root directory of the repository, run:

    ```bash
    pytest
    ```

    To run with verbose output:

    ```bash
    pytest -v
    ```

CI runs the same suite on Python 3.10, 3.11 and 3.12, plus `ruff check src/
tests/`, on every push and pull request.

