# python-licensing
```python-licensing``` is a tool to protect your python scripts with a license that is provided by a licensing server. You can license functions via decorators or your entire script. ```python-licensing``` may be combined with [pyarmor](https://github.com/dashingsoft/pyarmor) to obfuscate your script and embeds and hide this licensing logic, which is located in [./python-licensing](./python-licensing). The licensing server implementation is located in [./server](./server).

**Audience**

The initial audience were university students who work on their theses without getting paid. While pursuing their thesis work they sometimes develop software which is being used long after their departure. Since they are not getting paid, they individuals hold the rights to the software.

This software may be used to sell licenses to the professorships where the software is desired - redeeming some of the money they should have earned. Feel free to use it in any circumstances where you see fit.

---

## Usage
### Individual functions
```python
import python_licensing as pl

@pl.license('https://my-licensing-server.example.com')
def my_licensed_function():
    pass
```

## Installation
### python-licensing tool
```cmd
pip3 install python-licensing
```

### License server
#### Using docker-compose
```cmd
docker run python-licensing:latest
```