from datetime import datetime
from flask import jsonify, make_response, abort

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {
    "Jones": {
        "fname": "Indiana",
        "lname": "Jones",
        "timestamp": get_timestamp(),
    },
    " Sparrow": {
        "fname": "Jack",
        "lname": " Sparrow",
        "timestamp": get_timestamp(),
    },
    "Snow": {
        "fname": "John",
        "lname": "Snow",
        "timestamp": get_timestamp(),
    },
}

def read_all():
    dict_alunos = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
    alunos = jsonify(dict_alunos)
    qtd = len(dict_alunos)
    content_range = "alunos 0-"+str(qtd)+"/"+str(qtd)
    # Configura headers
    alunos.headers['Access-Control-Allow-Origin'] = '*'
    alunos.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    alunos.headers['Content-Range'] = content_range
    return alunos

def read_one(lname):
    if lname in PEOPLE:
        person = PEOPLE.get(lname)
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )
    return person


def create(person):
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        return make_response(
            "{lname} successfully created".format(lname=lname), 201
        )
    else:
        abort(
            406,
            "Person with last name {lname} already exists".format(lname=lname),
        )


def update(lname, person):
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

def delete(lname):
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )
