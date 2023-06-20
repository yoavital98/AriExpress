# AriExpress
In order to run the server, we need to have two configuration files: Load file (non-mandatory) and Config file (mandatory).

## Configuration Files

1. **config.json**: This file should contain a dictionary with configuration settings for the server: PaymentService, SupplyService, Database and Admins. Example for the config.json:

    ```json
    {
      "PaymentService": "https://external-systems.000webhostapp.com/",
      "SupplyService": "https://external-systems.000webhostapp.com/",
      "Database": "",
      "Admins": {
        "admin": "12341234",
        "admin2": "12341234"
      }
    }

    ```

   Values can be adjusted. Admins must include atleast one admin.

2. **load.json**: This file contains Service commands and their arguments that will run on server startup. If a function is not found or the argument number is invalid - an exception will occur. Example for the load.json:

    ```
    [
      {
        "register": {"args": ["aaa", "asdf1233", "a@a.com"]}
      },
      {
        "register": {"args": ["bbb", "asdf1233", "a@a.com"]}
      },
      {
        "logIn": {"args": ["bbb", "asdf1233"]}
      },
      {
        "createStore": {"args": ["bbb", "TESTSTORE"]}
      },
      {
        "logOut": {"args": ["bbb"]}
      },
      {
        "logIn": {"args": ["aaa", "asdf1233"]}
      },
      {
        "createStore": {"args": ["aaa", "store123"]}
      },
      {
        "createStore": {"args": ["aaa", "456store"]}
      },
      {
        "addNewProductToStore": {"args": ["aaa", "store123", "apple", "20", "3", "fruit"]}
      },
      {
        "addNewProductToStore": {"args": ["aaa", "store123", "banana", "30", "8", "fruit"]}
      },
      {
        "addNewProductToStore": {"args": ["aaa", "store123", "headphones", "10", "700", "electronics"]}
      },
      {
        "logOut": {"args": ["aaa"]}
      }
    ]
    ```

The JSON is a list that contains dictionaries with the key being the function name and the value is a dict of arguments (as shown above).
Note: the load JSON is not mandatory, meaning we can create a Service without a load file and the system will startup in a "clean" state.


## Running the Server

To run the server, follow these steps (works on Linux and MacOS):

1. Install the required dependencies.

2. Run ./run from the main directory.

## Additional Notes

- The configs are inserted in apps.py in the MainApp folder. Make sure to load the right JSON file.

