# NumGen
## The Purpose

Membran employees require several different types of codes in order to catalogue and ship new products. In order to manage these codes, a utility is needed to generate available codes for new products and track previously used codes. 

## Application Details

### User Interaction

Users will interact with the number generators through a web browser interface. The interface will consist of a simple, single page layout containing two main sections for each generator (barcode & ISRC). Each generator will it's own control options and activation buttons. Once a user enters their parameters for code generation and clicks the activation button, an API call will be made to the relevant python generator. The generator will then create codes and return them to the page from which the user may copy the text for their usage.

### Barcode Generator

The barcode generator accepts a parameter defining the product class (244, 600, PROMO etc...) which it then uses to access the database and acquire the next available product number of that class, marking it as used. With the product number and Membran's assigned initial digits, it creates a barcode of the appropriate type (UPCA, EAN13) and returns the code to the caller.

### ISRC Generator 

The ISRC generator accepts a parameter defining the desired amount of codes. It will then access the database and find the last used code, and mark the range of codes to be generated as now in use (last_gen - last_gen+desAmount). If the current year is greater than the year of the last used code, it will reset the counter to "00001". With the range of available codes it will then concatenate the country, org, and year codes, returning them to the caller.
