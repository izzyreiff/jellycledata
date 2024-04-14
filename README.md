# jellycledata
### Converting show information to NFO format

`jellycledata` is a python script and command-line tool for converting show information from text files to the NFO (XBMC metadata) format. This tool is useful for organizing and cataloging information about various shows, including musicals, plays, concerts, and more. It was originally created to mass format movie.nfo files for jellyfin based on .txt files in the ~encora copy format~.

There are two ways to use it: through the python script, and through the CLI tool.

## Installation
To use jellycledata, ensure you have Python 3 installed on your system. You can download and install Python from the official website.

Clone or download the jellycledata repository to your local machine:
```
git clone https://github.com/izzyreiff/jellycledata.git
```

Navigate to the jellycle directory:
```
cd jellycle
```
Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

## Python script - Great for one file
If you have a `.txt` file copied from encora, simply run it through jellycledata's `script.py` to produce a perfectly usable `movie.nfo` file.
#### In the script.py file:
1. Change the `txt_filename` variable to the name of your .txt file, the templated version is `info.txt`.
2. Change the `nfo_filename` variable to the desired name of your .nfo file, the templated version is `movie.nfo`.
3. Run `$ script.py` (however your machine runs python scripts)
4. Receive an outputted `.nfo` file in the same directory.


## CLI Tool - Great for many files
To create many `movie.nfo` files from `info.txt` files, run the following command:
```
python jellycle.py -o movie.nfo
```

This command will search for `info.txt` files in the current directory and all of its subdirectories and generate corresponding `movie.nfo` files.

You can specify a different output file name using the `-o` or `--output_file` option:
```
python info2nfo.py -o output.nfo
```

You may also choose not to specify an output file name, and it will default to `movie.nfo`.

## Input Format
The input file (info.txt) should follow a specific format to ensure proper conversion. Each info.txt file should contain the following information:

- Title: The title of the show.
- Tour: The tour or production name (if applicable).
- Date: The date of the show in one of the following formats: "Month Day, Year", "Month, Year", or "Year".
- Director: The show's director.
- Format: The format of the show (e.g., Video, Audio, Highlights).
- Cast: The cast members and their respective roles.
- Notes: Additional notes or information about the show (optional).

Here's an example of the info.txt format:
```
Title - Tour
Date - Director
Format

Cast:
Actor 1 (Role 1), Actor 2 (Role 2), Actor 3 (Role 3)

Notes:
Additional notes about the show.
```

## Output
The tool generates NFO files (`movie.nfo`) based on the input `info.txt` files. The output NFO file contains metadata about the show, including title, date, format, cast, and notes.

### yes the name of this repository is a play on jellicle cats, data, and jellyfin...
