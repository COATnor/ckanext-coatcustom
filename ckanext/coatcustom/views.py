from flask import Blueprint, jsonify
import ckan.plugins.toolkit as toolkit
from . import helpers

scheming = Blueprint("scheming", __name__)

@scheming.route('/scheming/api/util/<field>/autocomplete')
def autocomplete(field):
    tags = []
    value = toolkit.request.params.get('incomplete')
    if field == "dataset":
        dataset_type = toolkit.request.params.get('dataset_type')
        context = {
            "user": toolkit.g.user,
            "userobj": toolkit.g.userobj,
        }
        query = {
            "q": f"name:*{value}*",
            "include_private": True,
        }
        if dataset_type:
            query["q"] += f" AND dataset_type:{dataset_type}"
        found = toolkit.get_action('package_search')(context,  query)
        for dataset in found['results']:
            tags.append(dataset['name'])
    elif field == "associated_parties":
        tags = helpers.scheming_publisher_tags(field)
    elif field == "location":
        tags = helpers.scheming_locations_tags(field)
    elif field == "scientific_name":
        tags = helpers.scheming_scientific_name_tags(field)
    else:
        tags = []
    results = []
    for tag in tags:
        if value.lower() in tag.lower():
            results.append({'Name': tag})
    return jsonify({"ResultSet": {"Result": results}})
