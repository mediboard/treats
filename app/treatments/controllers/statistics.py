import scipy.stats as stats
import math

from app.models import measure_dispersion_param 


# TODO need to refactor this to use strings
continous_dispersions = [
	'measure_dispersion_param.STANDARD_ERROR',
	'measure_dispersion_param.STANDARD_DEVIATION']

confidence_intervals = [
	'measure_dispersion_param.CONFIDENCE_INTERVAL_95',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_90',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_80',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_97',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_99',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_60',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_96',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_98',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_70',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_85',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_75',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_94',
	'measure_dispersion_param.CONFIDENCE_INTERVAL_100']

iqr = ['measure_dispersion_param.INTER_QUARTILE_RANGE']

non_calculable = [
	'measure_dispersion_param.FULL_RANGE',
	'measure_dispersion_param.GEOMETRIC_COEFFICIENT_OF_VARIATION',
	'measure_dispersion_param.NA']

def pick_top_point(outcomes_a, outcomes_b, dispersion_type):
	# line them up based on title
	title2Outcomes = {}
	for outcome in outcomes_a:
		if outcome.title not in title2Outcomes:
			title2Outcomes[outcome.title] = []

		title2Outcomes[outcome.title].append(outcome)

	for outcome in outcomes_b:
		if outcome.title not in title2Outcomes:
			title2Outcomes[outcome.title] = []

		title2Outcomes[outcome.title].append(outcome)

	return max([x for x in title2Outcomes.values() if len(x) > 1], key=lambda x: cohen_d(x[0], x[1], dispersion_type))


def cohen_d(outcome_a, outcome_b, dispersion_type):
	if dispersion_type in non_calculable:
		return None

	sd_a = get_sd(outcome_a, dispersion_type)
	sd_b = get_sd(outcome_b, dispersion_type)

	# 99% of the time this is a mean
	mean_a = outcome_a.value
	mean_b = outcome_b.value

	pooled_sd = math.sqrt(((sd_a * sd_a) + (sd_b * sd_b)) / 2)

	mean_diff = max(mean_a, mean_b) - min(mean_a, mean_b)

	return mean_diff / pooled_sd


def get_sd(outcome, dispersion_type):

	if (dispersion_type == 'measure_dispersion_param.STANDARD_ERROR'):
		return math.sqrt(outcome.no_participants) * float(outcome.dispersion)

	if (dispersion_type in confidence_intervals):
		return math.sqrt(outcome.no_participants) * (float(outcome.upper) - float(outcome.lower)) / 3.92

	if (dispersion_type in iqr):
		return (float(outcome.upper) - float(outcome.lower)) / 1.35

	return outcome.dispersion


def get_pval(outcome_a, outcome_b, dispersion_type):
	continous_dispersions = [
		'measure_dispersion_param.STANDARD_ERROR',
		'measure_dispersion_param.STANDARD_DEVIATION']

	confidence_intervals = [
		'measure_dispersion_param.CONFIDENCE_INTERVAL_95',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_90',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_80',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_97',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_99',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_60',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_96',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_98',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_70',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_85',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_75',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_94',
		'measure_dispersion_param.CONFIDENCE_INTERVAL_100']

	iqr = ['measure_dispersion_param.INTER_QUARTILE_RANGE']

	non_calculable = [
		'measure_dispersion_param.FULL_RANGE',
		'measure_dispersion_param.GEOMETRIC_COEFFICIENT_OF_VARIATION',
		'measure_dispersion_param.NA']

	sd_a = outcome_a.dispersion
	sd_b = outcome_b.dispersion

	if (dispersion_type == measure_dispersion_param.STANDARD_ERROR):
		sd_a = math.sqrt(outcome_a.no_participants) * float(outcome_a.dispersion)
		sd_b = math.sqrt(outcome_b.no_participants) * float(outcome_b.dispersion)

	if (dispersion_type in confidence_intervals):
		sd_a = math.sqrt(outcome_a.no_participants) * (float(outcome_a.upper) - float(outcome_a.lower)) / 3.92
		sd_b = math.sqrt(outcome_b.no_participants) * (float(outcome_b.upper) - float(outcome_b.lower)) / 3.92

	if (dispersion_type in iqr):
		sd_a = (float(outcome_a.upper) - float(outcome_a.lower)) / 1.35
		sd_b = (float(outcome_b.upper) - float(outcome_b.lower)) / 1.35

	return stats.ttest_ind_from_stats(
							mean1=outcome_a.value, 
							std1=sd_a, 
							nobs1=outcome_a.no_participants,
							mean2=outcome_b.value,
							std2=sd_b,
							nobs2=outcome_b.no_participants).pvalue       

