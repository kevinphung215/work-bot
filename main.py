import os
import tkinter as tk
from tkinter import messagebox
from docxtpl import DocxTemplate


# Function to generate the document
def generate_document(data):
    try:
        # Load the template
        doc = DocxTemplate("template.docx")
        # Prepare context for rendering
        context = {
            **data,
            "show_race_section": data["complaint_type"]["race"],
            "show_color_section ": data["complaint_type"]["color"],
            "show_religion_section ": data["complaint_type"]["religion"],
            "show_sex_section": data["complaint_type"]["sex"],
            "show_sexual_orientation_section": data["complaint_type"]["sexual orientation"],
            "show_national_origin_section": data["complaint_type"]["national origin"],
            "show_age_section": data["complaint_type"]["age"],
            "show_retaliation_section": data["complaint_type"]["retaliation"],
            "show_disability_section": data["complaint_type"]["disability"],
            "show_gina_section": data["complaint_type"]["gina"],
            "show_discrete_section": data["complaint_type"]["discrete"],
            "show_non_discrete_section": data["complaint_type"]["non discrete"],
            "show_non_selection_section": data["complaint_type"]["non selection"],
            "show_accommodation_section": data["complaint_type"]["accommodation"],
            "show_harassment_section": data["complaint_type"]["harassment"],
        }
        # Render the template with user data
        doc.render(context)
        # Save the document
        if not os.path.exists("saved affidavits"):
            os.makedirs("saved affidavits")
        doc.save(f"saved affidavits/{data['full_name']}_affidavit.docx")
        messagebox.showinfo("Success", "Document generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to collect data from the form
def collect_data():
    data = {
        "full_name": full_name_entry.get(),
        "case_number": case_number_entry.get(),
        "address": address_entry.get(),
        "position_title": position_title_entry.get(),
        "work_location": work_location_entry.get(),
        "email": email_entry.get(),
        "phone": phone_entry.get(),
        "complaint_type": {
            "race": complaint_type_var_race.get(),
            "color": complaint_type_var_color.get(),
            "religion": complaint_type_var_religion.get(),
            "sex": complaint_type_var_sex.get(),
            "sexual orientation": complaint_type_var_sexual_orientation.get(),
            "national origin": complaint_type_var_national_origin.get(),
            "age": complaint_type_var_age.get(),
            "retaliation": complaint_type_var_retaliation.get(),
            "disability": complaint_type_var_disability.get(),
            "gina": complaint_type_var_gina.get(),
            "discrete": complaint_type_var_discrete.get(),
            "non discrete": complaint_type_var_non_discrete.get(),
            "non selection": complaint_type_var_non_selection.get(),
            "accommodation": complaint_type_var_accommodation.get(),
            "harassment": complaint_type_var_harassment.get(),
        },
    }
    # Generate the document
    generate_document(data)


# Create the main window
root = tk.Tk()
root.title("Complainant Affidavit Generator")

# Add input fields
tk.Label(root, text="Full Name:").grid(row=0, column=0)
full_name_entry = tk.Entry(root)
full_name_entry.grid(row=0, column=1)

tk.Label(root, text="Case Number:").grid(row=1, column=0)
case_number_entry = tk.Entry(root)
case_number_entry.grid(row=1, column=1)

tk.Label(root, text="Address:").grid(row=2, column=0)
address_entry = tk.Entry(root)
address_entry.grid(row=2, column=1)

tk.Label(root, text="Position Title:").grid(row=3, column=0)
position_title_entry = tk.Entry(root)
position_title_entry.grid(row=3, column=1)

tk.Label(root, text="Work Location:").grid(row=4, column=0)
work_location_entry = tk.Entry(root)
work_location_entry.grid(row=4, column=1)

tk.Label(root, text="Email:").grid(row=5, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=5, column=1)

tk.Label(root, text="Phone:").grid(row=6, column=0)
phone_entry = tk.Entry(root)
phone_entry.grid(row=6, column=1)

tk.Label(root, text="Purview Type:").grid(row=8, column=0)
complaint_type_var_race = tk.BooleanVar()
complaint_type_var_color = tk.BooleanVar()
complaint_type_var_religion = tk.BooleanVar()
complaint_type_var_sex = tk.BooleanVar()
complaint_type_var_sexual_orientation = tk.BooleanVar()
complaint_type_var_national_origin = tk.BooleanVar()
complaint_type_var_age = tk.BooleanVar()
complaint_type_var_retaliation = tk.BooleanVar()
complaint_type_var_disability = tk.BooleanVar()
complaint_type_var_gina = tk.BooleanVar()
complaint_type_var_discrete = tk.BooleanVar()
complaint_type_var_non_discrete = tk.BooleanVar()
complaint_type_var_non_selection = tk.BooleanVar()
complaint_type_var_accommodation = tk.BooleanVar()
complaint_type_var_harassment = tk.BooleanVar()

tk.Checkbutton(root, text="Race", variable=complaint_type_var_race).grid(
    row=9, column=0, sticky='w'
)
tk.Checkbutton(root, text="Color", variable=complaint_type_var_color).grid(
    row=10, column=0, sticky='w' 
)
tk.Checkbutton(root, text="Religion", variable=complaint_type_var_religion).grid(
    row=11, column=0, sticky='w'
)
tk.Checkbutton(root, text="Sex", variable=complaint_type_var_sex).grid(
    row=12, column=0, sticky='w'
)
tk.Checkbutton(root, text="Sexual Orientation", variable=complaint_type_var_sexual_orientation).grid(
    row=13, column=0, sticky='w'
)
tk.Checkbutton(root, text="National Origin", variable=complaint_type_var_national_origin).grid(
    row=14, column=0, sticky='w'
)
tk.Checkbutton(root, text="Age", variable=complaint_type_var_age).grid(
    row=15, column=0, sticky='w'
)
# Section break 
tk.Label(root, text="Complaint Type:").grid(row=16, column=0)
tk.Checkbutton(root, text="Retaliation", variable=complaint_type_var_retaliation).grid(
    row=17, column=0, sticky='w'
)
tk.Checkbutton(root, text="Disability", variable=complaint_type_var_disability).grid(
    row=18, column=0, sticky='w'
)
tk.Checkbutton(root, text="GINA", variable=complaint_type_var_gina).grid(
    row=19, column=0, sticky='w'
)
tk.Checkbutton(root, text="Discrete", variable=complaint_type_var_discrete).grid(
    row=20, column=0, sticky='w'
)
tk.Checkbutton(root, text="Non Discrete", variable=complaint_type_var_non_discrete).grid(
    row=21, column=0, sticky='w'
)
tk.Checkbutton(root, text="Non Selection", variable=complaint_type_var_non_selection).grid(
    row=22, column=0, sticky='w'
)
tk.Checkbutton(root, text="Accommodation", variable=complaint_type_var_accommodation).grid(
    row=23, column=0, sticky='w'
)
tk.Checkbutton(root, text="Harassment", variable=complaint_type_var_harassment).grid(
    row=24, column=0, sticky='w'
)

# Additional details for each complaint type
race_details_entry = tk.Entry(root)
race_details_entry.grid(row=9, column=1)

color_details_entry = tk.Entry(root)
color_details_entry.grid(row=10, column=1)

religion_details_entry = tk.Entry(root)
religion_details_entry.grid(row=11, column=1)

sex_details_entry = tk.Entry(root)
sex_details_entry.grid(row=12, column=1)

sexual_orientation_details_entry = tk.Entry(root)
sexual_orientation_details_entry.grid(row=13, column=1)

national_origin_details_entry = tk.Entry(root)
national_origin_details_entry.grid(row=14, column=1)

age_details_entry = tk.Entry(root)
age_details_entry.grid(row=15, column=1)


# Submit button
tk.Button(root, text="Generate Affidavit", command=collect_data).grid(
    row=26, column=0, columnspan=2
)

# Run the application
root.mainloop()
