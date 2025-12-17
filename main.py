from flask import Flask, redirect, render_template, request, session
import ast
import math
import itertools

app = Flask(__name__)


def total_path_distance(points):
    origin = (0, 0)
    dist = math.dist(origin, points[0])
    for i in range(len(points) - 1):
        dist += math.dist(points[i], points[i+1])
    dist += math.dist(points[-1], origin)
    return dist

def is_valid_locations(lst):
    #input validation
    if not isinstance(lst, list):
        return False
    for item in lst:
        if not (isinstance(item, tuple) and len(item) == 2):
            return False
        x, y = item
        # must be numbers
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            return False
    return True



@app.errorhandler(404)
def error(e):
    return redirect('/')


@app.route('/')
def homepage():
    # get the "locations" parameter
    locations_str = request.args.get('locations')

    # Case 1: No locations (just return the homepage)
    if not locations_str:
        return render_template("home_page.html")

    # Try to convert the string into a python object
    try:
        lst_Locations = ast.literal_eval(locations_str)
    except:
        return render_template('results.html', error="Invalid input format")

    # Case 2: Validate
    if not is_valid_locations(lst_Locations):
        return render_template('results.html', error="Invalid input format")

    # compute best route
    best_order = None
    best_distance = float('inf')

    for perm in itertools.permutations(lst_Locations):
        d = total_path_distance(list(perm))
        if d < best_distance:
            best_distance = d
            best_order = perm

    return render_template(
        "results.html",
        distance=round(best_distance, 3),
        order=best_order,
        error=None
    )


if __name__ == "__main__":
    app.run(debug=True)
