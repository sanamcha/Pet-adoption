from flask import Flask, url_for, request, render_template, session, jsonify, flash, redirect
from models import db,  connect_db,  Pet
from forms import AddPetForm, EditPetForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "hello1234567"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()

@app.route('/')
def home_pets():
    """Home page for all pets"""

    pets = Pet.query.all()

    return render_template("home.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Add a pet."""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        
        new_pet = Pet(name = form.name.data, 
                    species = form.species.data, 
                    age = form.age.data,
                    photo_url = form.photo_url.data, 
                    notes = form.notes.data)

        db.session.add(new_pet)
        db.session.commit()

        flash(f"{new_pet.name} added.")
        return redirect("/add")

    else:
        return render_template("add_form.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit pet."""

    
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
       

        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect("/")

    else:
        return render_template("edit_form.html", form=form, pet=pet)




@app.route("/api/pets")
def api_all_pet():
    """Return all pets info in JSON."""
  
    all_pets = [pet.serialize() for pet in Pet.query.all()]
    return jsonify(pet=all_pets)

@app.route('/api/pets/<int:pet_id>', methods=['GET'])
def api_get_pet(pet_id):
    """Returns JSON for one todo in particular"""
    pet = Pet.query.get_or_404(pet_id)
    return jsonify(pet=pet.serialize())





    






