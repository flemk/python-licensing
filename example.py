from python_licensing.python_licensing import licensed

@licensed('https://127.0.0.1:5000')
def main():
    print("The body of the licensed function has been executed.")
    input("Press any key to exit.")

if __name__ == '__main__':
    main()
