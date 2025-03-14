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
            "race_details": request.form["race_details"],
            "color_details": request.form["color_details"],
            "religion_details": request.form["religion_details"],
            "sex_details": request.form["sex_details"],
            "sexual_orientation_details": request.form["sexual_orientation_details"],
            "national_origin_details": request.form["national_origin_details"],
            "age_details": request.form["age_details"],
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
            "hide_investigator_info": "hide_investigator_info" in request.form,
        }
        generate_document(data)
        flash("Document generated successfully!")
        return redirect(url_for("index"))
    return render_template("index.html")


def generate_document(data):
    try:
        doc = DocxTemplate("template.docx")
        context = {
            **data,
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
                f"82. Why do you believe your {purview.replace('_', ' ')} was a factor in the selection process"
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
            "show_sexual_orientation_section": data["purview_type"][
                "sexual_orientation"
            ],
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
        doc.render(context)
        if not os.path.exists("saved affidavits"):
            os.makedirs("saved affidavits")
        last_name = data["last_name"]
        first_initial = data["first_name"][0]
        doc.save(
            f"saved affidavits/{data['case_number']} {last_name} {first_initial}.docx"
        )
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    app.run(debug=True)
