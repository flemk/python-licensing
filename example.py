from python_licensing.python_licensing import licensed

@licensed('https://localhost:5000')
def main():
    print("This is a licensed function.")
    input("Press any key to exit.")

if __name__ == '__main__':
    main()    
