from datetime import datetime
import argparse
import os

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
    xml_data = "<actors>\n"
    for entry in cast_info.split(','):
        name, role = entry.split('(')
        role = role[:-1]  # Remove the trailing ')'
        xml_data += f"    <actor>\n"
        xml_data += f"        <name>{name.strip()}</name>\n"
        xml_data += f"        <role>{role.strip()}</role>\n"
        xml_data += f"    </actor>\n"
    xml_data += "</actors>"
    return xml_data

def generate_nfo_from_txt(txt_content):
    # Split the content of the txt file into lines
    lines = txt_content.split('\n')
    # Extract title, tour, date, format, master, cast, and notes
    title_parts = lines[0].split(' - ')
    title = title_parts[0].strip()
    tour = title_parts[1]  # Extract tour from the title
    date_parts = lines[1].split(' - ')
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
        if "Cast:" in line:
            cast_line_index = i+1
            break
    if cast_line_index is not None:
        cast = lines[cast_line_index].strip()
    else:
        cast = ""
    cast = cast_to_xml(cast)
    notes_line_index = None
    for i, line in enumerate(lines):
        if "Notes:" in line:
            notes_line_index = i+1
            break
    # Extract notes if "Notes:" line is found
    if notes_line_index is not None:
        notes = lines[notes_line_index].strip()
    else:
        notes = "The plot was lost along the way... Please email izzyreiff+jf@gmail.com'"

    # Generate content for the .nfo file
    nfo_content = f"""\
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<movie>
<tile>{title}</title>
<plot>{notes}</plot>
<genre>Musical Theater</genre>
<genre>{genre}</genre>
<studio>{tour}</studio>
<premiered>{date}</premiered>
<style>{format_info}</style>
<director>{master}</director>
{cast}
</movie>
"""
    return nfo_content

def generate_nfo_file(txt_filename, nfo_filename):
    # Read content of the .txt file
    with open(txt_filename, 'r') as txt_file:
        txt_content = txt_file.read()

    # Generate content for .nfo file
    nfo_content = generate_nfo_from_txt(txt_content)

    # Write content to .nfo file
    with open(nfo_filename, 'w') as nfo_file:
        nfo_file.write(nfo_content)

#---------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Convert text files named 'info.txt' with show information to 'movie.nfo' format.")
    parser.add_argument("-o", "--output_file", help="Path to the output 'movie.nfo' file (default: 'movie.nfo')", default="movie.nfo")
    return parser.parse_args()

def convert_files(input_file, output_file):
    # Check if input file is 'info.txt'
    if os.path.basename(input_file) == 'info.txt':
        # Generate corresponding output file path
        output_dir = os.path.dirname(input_file)
        output_nfo = os.path.join(output_dir, output_file)
        # Generate .nfo file
        generate_nfo_file(input_file, output_nfo)

    # Recursively search directories for 'info.txt' files
    if os.path.isdir(input_file):
        for root, dirs, files in os.walk(input_file):
            for file in files:
                if file == 'info.txt':
                    # Generate corresponding output file path
                    txt_path = os.path.join(root, file)
                    output_dir = os.path.dirname(txt_path)
                    output_nfo = os.path.join(output_dir, output_file)
                    # Generate .nfo file
                    generate_nfo_file(txt_path, output_nfo)

def main():
    args = parse_args()
    convert_files(".", args.output_file)  # Start the recursive search from the current directory
    
if __name__ == "__main__":
    main()