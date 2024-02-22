
import yaml

# Load the metadata from the YAML file
with open('metadata.yml', 'r') as file:
    metadata = yaml.safe_load(file)

def generate_html(staff):
    html_lines = [
        "<!-- Grid person -->",
        "::: {.grid .person}",
        "::: {.g-col-13 .g-col-sm-6 .g-col-md-4}"
    ]
    
    # Photo
    if 'photo' in staff:
        html_lines.append(f"<img src=\"{staff['photo']}\" style=\"width: 249px; height: 250px;\" />")

    html_lines.append(":::")
    html_lines.append("::: {.g-col-13 .g-col-sm-6 .g-col-md-4}")
    html_lines.append("<!-- ### info -->")
    
    # Name and URL
    if 'name' in staff and 'url' in staff:
        html_lines.append(f"#### <i class=\"fa fa-user\"></i> &nbsp; [{staff['name']}]({staff['url']})")
    
    # Office
    if 'office' in staff:
        html_lines.append(f"- <i class=\"fa fa-university\"></i> &nbsp; {staff['office']}")
    
    # Email
    if 'email' in staff:
        html_lines.append(f"- <i class=\"fa fa-envelope\"></i> &nbsp; <a href=\"mailto:{staff['email']}\">{staff['email']}</a>")
    
    # Phone
    if 'phone' in staff:
        html_lines.append(f"- <i class=\"fa fa-phone\"></i> &nbsp; {staff['phone']}")
    
    # Appointment URL
    if 'appointment_url' in staff:
        html_lines.append(f"- <i class=\"fa fa-calendar-check\"></i> &nbsp; [Schedule an appointment]({staff['appointment_url']})")
    
    html_lines.append(":::")
    html_lines.append("::: {.g-col-13 .g-col-md-4 .contact-policy}")
    html_lines.append("<!-- ### contact-policy -->")
    
    # Contact Policy
    if 'contact_policy' in staff:
        html_lines.append(f"#### Contacting me\n{staff['contact_policy']}")
    
    html_lines.append(":::")
    html_lines.append(":::")
    html_lines.append("<!-- Grid person -->")
    
    return '\n'.join(html_lines)

# Generate and print HTML for each staff member

for staff_member in metadata['coordinator']:
    print(generate_html(staff_member))
    # display(HTML(generate_html(staff_member)))
    # print("\n")  # Add a newline for separation between entries



