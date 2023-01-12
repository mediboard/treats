from app.errors import create_notfound_error
from app.studies import bp
from flask_cors import cross_origin
from app.studies import controller
from flask import request
from app.utils import calculate_results_summary


@bp.route('/')
@cross_origin(supports_credentials=True)
def main():
	studies, next_page, total = controller.get_studies(request.args, int(request.args.get('page')))

	return {'studies': [study.to_summary_dict() for study in studies], 'next': next_page, 'total': total}


@bp.route('/search')
@cross_origin(supports_credentials=True)
def search():
	query = request.args.get('q')
	limit = request.args.get('limit')
	studies = controller.search(query, limit)
	
	return {'studies': [x.to_core_dict() for x in studies]}


@bp.route('/banner')
@cross_origin(supports_credentials=True)
def get_banner_studies():
	banner_studies = controller.get_banner_studies()

	return {'studies': [study.to_summary_effects_dict() for study in banner_studies]}


@bp.route('/administrations/<int:admin_id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_admin(admin_id):
	controller.remove_admin(admin_id)

	return {'status': 'success'}


@bp.route('/administrations', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_admin():
	data = request.get_json()
	new_admin = controller.add_admin(data)

	return {'admin': new_admin.to_dict()}


@bp.route('/insights/<int:insight_id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def remove_insight(insight_id):
	controller.remove_insight(insight_id)

	return {'status': 'success'}


@bp.route('/<string:study_id>/insights', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def get_add_insight(study_id):
	if (request.method == 'POST'):
		data = request.get_json()
		new_insight = controller.add_insight(data)

		return {'insight': new_insight.to_dict()}

	measure_id = request.args.get('measure_id')
	type = request.args.get('type')

	insights = controller.get_insights(study_id, measure_id, type)

	return {'insights': [x.to_dict() for x in insights]}


@bp.route('/<string:study_id>')
@cross_origin(supports_credentials=True)
def get_study(study_id):
	studies = controller.get_study(study_id)
	if (not studies):
		return create_notfound_error('Study with id {0} not found'.format(study_id))
		
	return {'studies': [study.to_summary_dict() for study in studies]}


@bp.route('/<string:study_id>/summary')
@cross_origin(supports_credentials=True)
def get_summary(study_id):
	studies = controller.get_study_summary(study_id)
	return {'studies': [study.to_summary_dict() for study in studies]}


@bp.route('/<string:study_id>/related')
@cross_origin(supports_credentials=True)
def get_related_studies(study_id):
	studies, next_page, total = controller.get_related_studies(study_id, int(request.args.get('page')))
	if not studies:
		return create_notfound_error('Study with id {0} not found'.format(study_id))
	return {'studies': [study.to_summary_dict() for study in studies], 'next': next_page, 'total': total}


@bp.route('/<string:study_id>/baselines')
@cross_origin(supports_credentials=True)
def get_baselines(study_id):
	baselines = controller.get_baselines(study_id)
	return {'baselines': [baseline.to_dict() for baseline in baselines]}


@bp.route('/<string:study_id>/effects')
@cross_origin(supports_credentials=True)
def get_effects(study_id):
	effect_groups = controller.get_effects(study_id)
	return {'effects': [effect.to_dict() for effect in effect_groups]}


@bp.route('/<string:study_id>/measures')
@cross_origin(supports_credentials=True)
def get_measures(study_id):
	limit = request.args.get('limit') or None
	primary = request.args.get('primary') or False

	measures = controller.get_measures(study_id, limit, primary)
	return {'measures': [measure.to_dict() for measure in measures]}


@bp.route('/<string:study_id>/groups')
@cross_origin(supports_credentials=True)
def get_groups(study_id):
	groups = controller.get_groups(study_id)
	return {'groups': [group.to_dict() for group in groups]}


@bp.route('/groups/<int:group_id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_group(group_id):
	data = request.get_json()
	group = controller.update_group(data, group_id)

	return {'group': group.to_dict()}


@bp.route('/<string:study_id>/criteria')
@cross_origin(supports_credentials=True)
def get_criteria(study_id):
	criteria = controller.get_criteria(study_id)
	return {'criteria': [c.to_dict() for c in criteria]}


@bp.route('/<string:study_id>/conditions')
@cross_origin(supports_credentials=True)
def get_conditions(study_id):
	conditions = controller.get_conditions(study_id)
	return {'conditions': [condition.to_dict() for condition in conditions]}


@bp.route('/<string:study_id>/treatments')
@cross_origin(supports_credentials=True)
def get_treatments(study_id):
	treatments = controller.get_treatments(study_id)
	return {'treatments': [treat.to_dict() for treat in treatments]}


# @bp.route('/<string:study_id>/analytics')
# @cross_origin(supports_credentials=True)
# def get_analytics(study_id):
# 	analytics = controller.get_analytics(study_id)
	


@bp.route('/get_studies_by_ids')
@cross_origin(supports_credentials=True)
def get_studies_by_ids():
	study_ids = request.args.get('ids', None, type=str)
	studies = controller.get_studies_by_ids(study_ids.split(','))

	return {'studies': [{**x[0].to_summary_dict(), 'mean':x[1], 'min': x[2], 'resultsSummary': calculate_results_summary(x[1], x[2]) } for x in studies]}
