from flask import Blueprint

from grant import JSONResponse
from .models import Milestone, milestones_schema

blueprint = Blueprint('milestone', __name__, url_prefix='/api/v1/milestones')


@blueprint.route("/", methods=["GET"])
def get_users():
    milestones = Milestone.query.all()
    result = milestones_schema.dump(milestones)
    return JSONResponse(result)