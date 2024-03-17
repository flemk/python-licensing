"""
This module demonstrates the use of the python_licensing library.
"""
from python_licensing import licensed

@licensed('https://127.0.0.1:5001')
def main():
    """
    This function prints a message and waits for the user to press any key.
    """
    print("The body of the licensed function has been executed.")
    input("Press any key to exit.")

if __name__ == '__main__':
    main()
