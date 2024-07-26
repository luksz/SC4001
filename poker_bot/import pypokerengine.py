import pypokerengine

def check_pypokerengine():
    try:
        print("PyPokerEngine is installed.")
        print(f"pypokerengine version: {pypokerengine.__version__}")
    except ImportError as e:
        print(f"Error: {e}")
        print("PyPokerEngine is not installed or there is an issue with the installation.")

if __name__ == "__main__":
    check_pypokerengine()
