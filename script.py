from datetime import datetime

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
            name = entry.strip()
            role = "Ensemble"
        xml_data += f"    <actor>\n"
        xml_data += f"        <name>{name.strip()}</name>\n"
        xml_data += f"        <role>{role.strip()}</role>\n"
        xml_data += f"    </actor>\n"
    return xml_data

def generate_nfo_from_txt(txt_content):
    # Split the content of the txt file into lines
    lines = txt_content.split('\n')
    # Extract title, tour, date, format, master, cast, and notes
    title_parts = lines[0].split(' - ')
    title = title_parts[0].strip()
    tour = title_parts[1]  # Extract tour from the title
    date_parts = lines[1].split(' - ')
    if date_parts[0].endswith(")"):
        # Split the input_string by "("
        parts = date_parts[0].rsplit("(", 1)
        # Take the first part, which is before the "("
        date = parts[0].strip()
    else:
        # If there's no "(#)" pattern at the end, return the original string
        date = date_parts[0]  
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
    years = date.split('-')
    year = years[0]
    # Generate content for the .nfo file
    nfo_content = f"""\
<?xml version="1.0" encoding="utf-8"?>
<movie>
    <title>{title}</title>
    <sorttitle>{title}</sorttitle>
    <set></set>
    <studio>{tour}</studio>
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

    <releasedate>{date}</releasedate>
    <style>{format_info}</style>
    <tag>{format_info}</tag>

    <director>{master}</director>
    <credits></credits>
{cast}
    
    <playcount>0</playcount>

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

# Example usage for generate nfo file
txt_filename = "info.txt"
nfo_filename = "movie.nfo"
generate_nfo_file(txt_filename, nfo_filename)

#---------------------------------