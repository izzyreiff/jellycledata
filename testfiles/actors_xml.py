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

# Example cast information
cast_info = "Beth Leavel (Miranda Priestly), Taylor Iman Jones (Andy Sachs), Javier Muñoz (Nigel Owens), Christiana Cole (Lauren Hunter), Megan Masako Haley (Emily Charlton), Tiffany Mann (Kayla Ward), Michael Tacconi (Nate Angstrom), Terrance Spencer (u/s Christian Thompson), Kyle Brown (Ensemble), Jojo Carmichael (s/w Ensemble), Olivia Cipolla (Ensemble), Tyrone Davis Jr. (Ensemble), Audrey Douglass (Ensemble), Hannah Douglass (Ensemble), Cailen Fu (Ensemble), Michael Samarie George (Ensemble), Henry Gottfried (Ensemble), Marya Grandy (Ensemble), Liana Hunt (Ensemble), Amber Jackson (Ensemble), Nikka Graff Lanzarone (Ensemble), Anthony Murphy (Ensemble), Jim Ortlieb (Ensemble), Johnny Rice (Ensemble), Sawyer Smith (Ensemble), CJ Tyson (Ensemble)"

# Convert cast information to XML-like format
xml_cast_info = cast_to_xml(cast_info)

print(xml_cast_info)
