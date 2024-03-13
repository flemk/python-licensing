# python-licensing
```python-licensing``` is a tool to protect your python scripts with a license that is provided by a licensing server. You can license functions via decorators or your entire script. ```python-licensing``` may be combined with [pyarmor](https://github.com/dashingsoft/pyarmor) to obfuscate your script and embeds and hide this licensing logic, which is located in [./python-licensing](./python-licensing). The licensing server implementation is located in [./server](./server).

**Audience**

The initial audience were university students who work on their theses without getting paid. While pursuing their thesis work they sometimes develop software which is being used long after their departure. Since they are not getting paid, they individuals hold the rights to the software.

This software may be used to sell licenses to the professorships where the software is desired - redeeming some of the money they should have earned. Feel free to use it in any circumstances where you see fit.

## Usage
### Individual functions
```python
import python_licensing as pl

@pl.licensed('https://my-licensing-server.example.com')
def my_licensed_function():
    pass
```
Have a look at ```example.py```.

## Installation
### python-licensing tool
```cmd
pip3 install python-licensing
```

### License server
#### Using docker-compose (recommended)
```cmd
docker-compose up -d
```

#### Using docker
```cmd
docker run python-licensing:latest
```
Keep in mind, that you'd need to specify the environment variables and build variables by hand.

## Obfuscating your script
**1. Install PyArmor using pip:**
```cmd
pip install pyarmor
```

Obfuscate your script using the ```gen``` command. Replace ```your_script.py``` with the path to your Python script:
```python
pyarmor gen your_script.py
```

This will create a ```dist``` directory containing the obfuscated version of your script and any necessary PyArmor runtime files. For more information visit [dashingsoft/pyarmor](https://github.com/dashingsoft/pyarmor)

**2. Delivering to the customer**

Package the ```dist``` directory into a ZIP file or another type of archive:

```cmd
zip -r your_script.zip dist
```

Send the ZIP file to your customer. They can run the obfuscated script using their Python interpreter:

```cmd
python dist/your_script.py
```

Please note that the customer will need to have the same major version of Python that you used to obfuscate the script. For example, if you obfuscated the script using Python 3.8, the customer will also need to have Python 3.8.

**3. Licensing**

To add licensing to your script, you can use the python-licensing library as described in the previous sections of this README. You should add the licensing code to your script before obfuscating it with PyArmor.