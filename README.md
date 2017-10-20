# NumGen
## Application Purpose

Membran employees require several different types of codes in order to catalogue and ship new products. In order to manage these codes, a utility is needed to generate available codes for new products and track previously used codes. 

## Setup and Usage Details

### Initialising Database and Config

To setup this utility:
*Install python dependencies with "pip Init\requirements.txt"
*Enter database credentials into Config.json
*Read through DBconstructor.sql to see table structure
*Enter appropriate values for 'last_generated' variables in both tables
*Run DBconstructor.sql to create tables
*Set FLASK_APP env. variable to "app.py" and call "flask run"

### Usage

Users will interact with the number generators by navigatiing to the hosted addres in a web browser. From there, a user may select the type/amount of code they want and press the red generate button to recieve their code. Once the activation button is clicked, an API call will be made to app.py which will pass the parameters to the relevant generator class. The generator will then create codes and return them to the page from which the user may copy the code to their clipboard for usage.

## Generator Implementation

### Barcode Generator

The barcode generator accepts a parameter which defines the product class (244, 600, Digital etc...). It then uses this to access the database and acquire the last generated number of that class. It references the database's upper limit for that class and if it has been reached, last\_generated is not incremented and the class returns an error message rather than a barcode. Otherwise last\_generated is incremented, returned and saved as the new product number. With the product number and Membran's assigned initial digits, a barcode of the appropriate type (UPCA, EAN13) is created and returned to the caller as a dictionary.

### ISRC Generator 

The ISRC generator accepts a parameter which defines the desired amount of codes. It will then access the database to retrieve the last used code then check for year roll-over and if there is room for the requested amount of codes. If the current year is greater than the year of the last used code, it will set last_generated to "amount". If there is not enough room, last\_generated is returned to the database untouched. If there is enough room, last\_generated is incremented by the requested amount, returned to the database, and returned for later use. With the range of available codes it will then concatenate the country, org, and year codes, returning them as a list to the caller.
