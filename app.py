from flask import Flask, render_template, request, redirect, url_for, flash
from docxtpl import DocxTemplate
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random secret key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "case_number": request.form["case_number"],
            "first_name": request.form["first_name"],
            "middle_name": request.form["middle_name"],
            "last_name": request.form["last_name"],
            "full_name": f"{request.form['first_name']} {request.form['middle_name']} {request.form['last_name']}".strip(),
            "work_location": request.form["work_location"],
            "position_title": request.form["position_title"],
            "position_level": request.form["position_level"],
            "address": request.form["address"],
            "unit": request.form["unit"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            # Add witness data:
            "witness_first_name": request.form["witness_first_name"],
            "witness_middle_name": request.form["witness_middle_name"],
            "witness_last_name": request.form["witness_last_name"],
            "witness_full_name": f"{request.form['witness_first_name']} {request.form['witness_middle_name']} {request.form['witness_last_name']}".strip(),
            "witness_work_location": request.form["witness_work_location"],
            "witness_position_title": request.form["witness_position_title"],
            "witness_position_level": request.form["witness_position_level"],
            "witness_address": request.form["witness_address"],
            "witness_unit": request.form["witness_unit"],
            "witness_email": request.form["witness_email"],
            "witness_phone": request.form["witness_phone"],
            "named_comparator": request.form["named_comparator"],
            "allegations": [
                request.form[key]
                for key in request.form
                if key.startswith("allegation_input_")
            ],
            "purview_type": {
                "race": "race" in request.form,
                "color": "color" in request.form,
                "religion": "religion" in request.form,
                "sex": "sex" in request.form,
                "sexual_orientation": "sexual_orientation" in request.form,
                "national_origin": "national_origin" in request.form,
                "age": "age" in request.form,
            },
            "complaint_type": {
                complaint: [
                    request.form[key]
                    for key in request.form
                    if key.startswith(f"{complaint}_input_")
                ]
                if complaint in request.form
                else []
                for complaint in [
                    "retaliation", "disability", "gina", "discrete", 
                    "non_discrete", "non_selection", "accommodation", "harassment"
                ]
            },
            "discrete_claims": [
                request.form[key]
                for key in request.form
                if key.startswith("discrete_input_")
            ],
            "hide_investigator_info": "hide_investigator_info" in request.form,
        }
        generate_document(data)
        flash("Document generated successfully!")
        return redirect(url_for("index"))
    return render_template("index.html")

def generate_purview_title(purview_type):
    selected_purviews = [purview.replace('_', ' ').upper() for purview, selected in purview_type.items() if selected]
    if not selected_purviews:
        return ""
    title = ", ".join(selected_purviews) + " ALLEGATIONS"
    return title

# Add input validation
def validate_input(data):
    required_fields = ['case_number', 'first_name', 'last_name']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Missing required field: {field}")
    
    if not any(data['purview_type'].values()):
        raise ValueError("At least one purview must be selected")
        
    if not any(data['complaint_type'].values()):
        raise ValueError("At least one complaint type must be selected")

def generate_document(data):
    try:
        validate_input(data)
        complainant_doc = DocxTemplate("template.docx")
        complainant_context = {
            **data,
            # Dynamically change title 
            "purview_title": generate_purview_title(data["purview_type"]),
            # === ADD THE PURVIEW QUESTIONS HERE ===
            "discrete_questions": [
                f"Why do you believe your {purview.replace('_', ' ')} was a factor?  What evidence can you present to substantiate this belief?"
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "discrete_questions_2": [
                f"Their {purview.replace('_', ' ')}"
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "non_discrete_questions": [
                f"Why do you believe your {purview.replace('_', ' ')} was a factor regarding this incident?  What evidence can you present to substantiate this belief?"
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "non_selection_questions": [
                f"Why do you believe your {purview.replace('_', ' ')} was a factor in the selection process"
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "accommodation_questions": [
                f"Why do you believe your {purview.replace('_', ' ')} was a factor when you were denied Reasonable Accommodation? "
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "show_race_section": data["purview_type"]["race"],
            "show_color_section": data["purview_type"]["color"],
            "show_religion_section": data["purview_type"]["religion"],
            "show_sex_section": data["purview_type"]["sex"],
            "show_sexual_orientation_section": data["purview_type"]["sexual_orientation"],
            "show_national_origin_section": data["purview_type"]["national_origin"],
            "show_age_section": data["purview_type"]["age"],
            "show_retaliation_section": data["complaint_type"]["retaliation"],
            "show_disability_section": data["complaint_type"]["disability"],
            "show_gina_section": data["complaint_type"]["gina"],
            "show_discrete_section": data["complaint_type"]["discrete"],
            "show_non_discrete_section": data["complaint_type"]["non_discrete"],
            "show_non_selection_section": data["complaint_type"]["non_selection"],
            "show_accommodation_section": data["complaint_type"]["accommodation"],
            "show_harassment_section": data["complaint_type"]["harassment"],
        }
        complainant_doc.render(complainant_context)

        # Generate Witness Affidavit
        witness_doc = DocxTemplate("witnesstemplate.docx")
        witness_context = {
            **data,
                        # === ADD THE PURVIEW QUESTIONS HERE ===
            "witness_discrete_questions": [
                f"Was the Complainant’s {purview.replace('_', ' ')} a factor in any action you took or decision you made related to this claim? If yes, explain how. "
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "witness_discrete_questions_2": [
                f"Their {purview.replace('_', ' ')}"
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "witness_non_discrete_questions": [
                f"Was the Complainant’s {purview.replace('_', ' ')} a factor in any action you took or decision you made related to this claim? If yes, explain how. "
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "witness_non_discrete_questions_2": [
                f"Their {purview.replace('_', ' ')}"
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "witness_non_selection_questions": [
                f"Was the Complainant’s {purview.replace('_', ' ')} a factor in any action you took or decision you made related to this claim? "
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "witness_accommodation_questions": [
                f"Was the Complainant’s {purview.replace('_', ' ')} a factor in any action you took or decision you made related to this claim? "
                for purview, selected in data["purview_type"].items()
                if selected
            ],
            "case_number": data["case_number"],
            "witness_full_name": data["witness_full_name"],
            "witness_work_location": data["witness_work_location"],
            "witness_position_title": data["witness_position_title"],
            "witness_position_level": data["witness_position_level"],
            "witness_address": data["witness_address"],
            "witness_unit": data["witness_unit"],
            "witness_email": data["witness_email"],
            "witness_phone": data["witness_phone"],
            "show_race_section": data["purview_type"]["race"],
            "show_color_section": data["purview_type"]["color"],
            "show_religion_section": data["purview_type"]["religion"],
            "show_sex_section": data["purview_type"]["sex"],
            "show_sexual_orientation_section": data["purview_type"]["sexual_orientation"],
            "show_national_origin_section": data["purview_type"]["national_origin"],
            "show_age_section": data["purview_type"]["age"],
            "show_retaliation_section": data["complaint_type"]["retaliation"],
            "show_disability_section": data["complaint_type"]["disability"],
            "show_gina_section": data["complaint_type"]["gina"],
            "show_discrete_section": data["complaint_type"]["discrete"],
            "show_non_discrete_section": data["complaint_type"]["non_discrete"],
            "show_non_selection_section": data["complaint_type"]["non_selection"],
            "show_accommodation_section": data["complaint_type"]["accommodation"],
            "show_harassment_section": data["complaint_type"]["harassment"],
        }
        witness_doc.render(witness_context)

        last_name = data["last_name"]
        first_initial = data["first_name"][0]
        witness_last_name = data["witness_last_name"]
        witness_first_initial = data["witness_first_name"][0]
        case_number = data["case_number"]
        
        complainant_doc.save(f"saved complainant affidavits/{case_number} {last_name} {first_initial}.docx")
        witness_doc.save(f"saved witness affidavits/{case_number} {witness_last_name} {witness_first_initial}.docx")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    except ValueError as e:
        flash(str(e))
        return False
    except Exception as e:
        flash(f"Error generating document: {str(e)}")
        return False
    return True


if __name__ == "__main__":
    app.run(debug=True)
