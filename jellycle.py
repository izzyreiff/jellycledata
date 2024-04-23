from datetime import datetime
import argparse
import os
import sys

# Redirect print statements
sys.stdout = open("errors.txt", "w")
sys.stderr = open("errors.txt", "a")


def parse_date(date_str):
    try:
        # Attempt to parse date in "Month Day, Year" format
        date = datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        try:
            # Attempt to parse date in "Year" format
            date = datetime.strptime(date_str, "%Y")
        except ValueError:
            try:
                # Attempt to parse date in "Month, Year" format
                date = datetime.strptime(date_str, "%B, %Y")
            except ValueError as e:
                # Print error message if date parsing fails
                print(f"Error parsing date: {e}")
                date = None
    return date.strftime("%Y-%m-%d") if date else None  # Convert date to ISO format if parsed successfully

def cast_to_xml(cast_info):
    xml_data = ""
    for entry in cast_info.split(','):
        try:
            name, role = entry.split('(')
            role = role[:-1]  # Remove the trailing ')'
        except ValueError:
            # If there's only one value, set role to "Ensemble"
            name = entry
            role = "Ensemble"
        xml_data += f"    <actor>\n"
        xml_data += f"        <name>{name.strip()}</name>\n"
        xml_data += f"        <role>{role.strip()}</role>\n"
        xml_data += f"    </actor>\n"
    return xml_data

def generate_nfo_from_txt(txt_content):
    # Split the content of the txt file into lines
    # Error handling for {&, "", ''} for XML (.NFO) file
    # Replace double quotes with &quot;
    #txt_content = txt_content.replace('"', '&quot;')
    # Replace single quotes with &apos;
    #txt_content = txt_content.replace("'", '&apos;')
    # Replace ampersands with &amp;
    txt_content = txt_content.replace('&', '&amp;')
    # REAL START OF METHOD
    lines = txt_content.split('\n')
    # Extract title, tour, date, format, master, cast, and notes
    title_parts = lines[0].split(' - ')
    title = title_parts[0].strip()
    tour = title_parts[1]  # Extract tour from the title
    # clean tour word bank for genre / studio
    keywords = ["Pre-Broadway", "Pre-West End", "Off-Broadway", "Off-West End", "Broadway", "West End", "US National Tour", "UK Tour", "UK & Ireland Tour", "Tour"]
    # Check if any keyword is present in the tour variable
    for keyword in keywords:
        if keyword in tour:
            cleantour = keyword
        else:
            cleantour = tour
            # Write print statement for tour and cleantour to troubleshoot special cases

    date_parts = lines[1].split(' - ')
    if date_parts[0].endswith(")"):
        # Split the input_string by "("
        parts = date_parts[0].rsplit("(", 1)
        # Take the first part, which is before the "("
        date = parts[0].strip()
    else:
        # If there's no "(#)" pattern at the end, return the original string
        date = date_parts[0].strip()
    master = date_parts[1].strip() if len(date_parts) > 1 else ""  # Extract master if available
    date = parse_date(date)  # Parse date using custom function
    format_info = lines[2].strip()
    if master == "Pro-Shot":
        genre = "Pro-Shot"
    else:
        genre = "Bootleg"
    cast_line_index = None
    for i, line in enumerate(lines):
        if "Cast:" in line or "CAST:" in line:
            cast_line_index = i+1
            break
    if cast_line_index is not None:
        cast = lines[cast_line_index].strip()
    else:
        cast = ""
    cast = cast_to_xml(cast)
    notes_line_index = None
    for i, line in enumerate(lines):
        if "Notes:" in line or "NOTES:" in line:
            notes_line_index = i+1
            break
    # Extract notes if "Notes:" line is found
    if notes_line_index is not None:
        notes = lines[notes_line_index].strip()
    else:
        notes = "The plot was lost along the way... Please email izzyreiff at gmail dot com"
    years = date.split('-')
    year = years[0]
    play = "Play"
    musical = "Musical"
    ballet = "Ballet"
    opera = "Opera"
    concert = "Concert"
    special = "Special"
     # Error handling for {&, "", ''} for XML (.NFO) file
    # Replace double quotes with &quot;
    #notes = notes.replace('"', '&quot;')
    # Replace single quotes with &apos;
    #notes = notes.replace("'", '&apos;')
    # Replace ampersands with &amp;
    #notes = notes.replace('&', '&amp;')
    
    # Generate content for the .nfo file
    nfo_content = f"""\
<?xml version="1.0" encoding="utf-8"?>
<movie>
    <title>{title}</title>
    <sorttitle>{title}</sorttitle>
    <set></set>
    <studio>{cleantour}</studio>
    <year>{year}</year>
    <runtime></runtime>
    <mpaa></mpaa>
    
    <outline></outline>
    <plot>{notes}</plot>
    <tagline></tagline>
    
    <rating></rating>
    <votes>0</votes>
    <top250></top250>
    <id></id>

    <thumb></thumb>
    <filenameandpath></filenameandpath>
    <trailer></trailer>
    
    <genre>Musical Theater</genre>
    <genre>{genre}</genre>
    <genre>{cleantour}</genre>
    
    <releasedate>{date}</releasedate>
    <style>{format_info}</style>
    <tag>{format_info}</tag>
    <tag>{tour}</tag>

    <director>{master}</director>
    <credits></credits>
{cast}
    
    <playcount>0</playcount>

</movie>
"""

    return nfo_content

def generate_nfo_file(txt_filename, nfo_filename):
    # Read content of the .txt file
    with open(txt_filename, 'r', encoding='utf-8') as txt_file:
        txt_content = txt_file.read()

    # Generate content for .nfo file
    nfo_content = generate_nfo_from_txt(txt_content)

    # Write content to .nfo file
    with open(nfo_filename, 'w', encoding='utf-8') as nfo_file:
        nfo_file.write(nfo_content)

#---------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Convert text files named 'info.txt' with show information to 'movie.nfo' format.")
    parser.add_argument("-o", "--output_file", help="Path to the output 'movie.nfo' file (default: 'movie.nfo')", default="movie.nfo")
    return parser.parse_args()

def convert_files(input_file, output_file):
    # Check if input file is 'info.txt'
    if os.path.basename(input_file).lower() == 'info.txt':
        # Generate corresponding output file path
        output_dir = os.path.dirname(input_file)
        output_nfo = os.path.join(output_dir, output_file)
        try:
            # Generate .nfo file
            generate_nfo_file(input_file, output_nfo)
        except Exception as e:
            print(f"Error processing file '{input_file}': {e}")

    # Recursively search directories for 'info.txt' files
    if os.path.isdir(input_file):
        for root, dirs, files in os.walk(input_file):
            for file in files:
                if file.lower() == 'info.txt':
                    # Generate corresponding output file path
                    txt_path = os.path.join(root, file)
                    output_dir = os.path.dirname(txt_path)
                    output_nfo = os.path.join(output_dir, output_file)
                    # Generate .nfo file
                    try:
                        # Generate .nfo file
                        generate_nfo_file(txt_path, output_nfo)
                    except Exception as e:
                        print(f"Error processing file '{txt_path}': {e}")
                        #print(f"Current directory: {root}")

def main():
    args = parse_args()
    convert_files(".", args.output_file)  # Start the recursive search from the current directory
    
if __name__ == "__main__":
    main()