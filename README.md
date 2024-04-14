# jellycledata

`jellycledata` is a python script and CLI tool for creating movie.nfo formatted for jellyfin based on .txt files in the ~encora copy format~.

## python script
If you have a .txt file copied from encora, simply run it through jellycle data to produce a perfectly usable movie.nfo file.
1. Change the `txt_filename` variable to the name of your .txt file, the templated version is `info.txt`.
2. Run `$ script.py` (or however your terminal runs python scripts)
3. Receive an outputted `movie.nfo` file in the same directory. You may change the generated `nfo_filename` from `movie.nfo`, but it is not generally recommended.
4. Rinse and repeat as needed.

## CLI tool


## yes the name of this repository is a play on jellicle cats, data, and jellyfin...