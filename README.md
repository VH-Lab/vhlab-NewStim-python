# vhlab-NewStim-python

This python repository is designed to interpret data structures and read data files created in the matlab repository [vhlab-NewStim-matlab](https://github.com/VH-Lab/vhlab-NewStim-matlab).

**Note:** This library is intended solely for reading data files and data structures. It does not and will not have the capability to interact with hardware in the way that `vhlab-NewStim-matlab` does.

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
