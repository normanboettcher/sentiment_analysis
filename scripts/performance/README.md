### Automization of performance testing

#### The script

To fire a number of `n` different reviews from a given csv-file to the REST-API where the model lives, a script is
created.
This script will be able to:

- take a flag `-n` which defines the number of reviews to fire up.
- take a flag `-f` which defines the filepath where the reviews are defined
- a flag `-s` which will be the separator in this file.

##### Prerequisites

- all reviews from a given file are written within `"`-characters.
    - e.g. `"wow, what a really nice movie"`

##### Technologies

The basic script with the business logic of extracting the reviews and make the remote call to the REST-API will be
written using `python`. Python has an excellent support for csv file handling.
The Python script will be wrapped into a classic bash script, where the flags are handled and the Python script will be
called.