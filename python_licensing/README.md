# python-licensing

`python-licensing` is a Python package that provides functionality for licensing a Python script and providing licenses via a licensing server. It allows you to license individual functions via decorators or your entire script.

## Installation

You can install `python-licensing` using pip:

```sh
pip install python-licensing
```

## Usage
Here's an example of how to use ```python-licensing``` to license a function:

```python
from python_licensing import licensed

@licensed('https://my-licensing-server.example.com')
def my_licensed_function():
    pass
```

In this example, my_licensed_function is a licensed function. The @licensed decorator takes the URL of your licensing server as an argument.

## Licensing Server
The licensing server implementation is located in ./server. You can run it using Docker or Docker Compose. For more information, see the server README.

## Obfuscating Your Script
You can combine ```python-licensing``` with pyarmor to obfuscate your script and hide the licensing logic. For more information, see the pyarmor documentation.

## Contact
If you have any questions or issues, please contact:

info@kostelezky.com
