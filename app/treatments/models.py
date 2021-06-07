from app import db 

import enum


class baseline_type(enum.Enum):
	RACE='Race'
	GENDER='Gender'
	ETHNICITY='ETHNICITY'
	AGE='AGE'
	OTHER='OTHER'

class baseline_subtype(enum.Enum):
	WHITE='White'
	BLACK='Black'
	ASIAN='Asian'
	INDIAN='Indian'
	PACIFIC='Pacific'
	MALE='Male'
	FEMALE='Female'
	NA='NA'


class resonsible_party_type(enum.Enum):
	SPONSER= 'Sponser'
	PRINCIPLE_INVESTIGATOR= 'Principal Investigator'
	SPONSER_INVESTIGATOR= 'Sponsor-Investigator'


class measure_param(enum.Enum):
	MEAN='Mean'
	NUMBER='Number'
	COUNT_OF_PARTICIPANTS='Count of Participants'
	LEAST_SQUARES_MEAN='Least Squares Mean'
	GEOMETRIC_MEAN='Geometric Mean'
	COUNT_OF_UNITS='Count of Units'
	GEOMETRIC_LEAST_SQUARES_MEAN='Geometric Least Squares Mean'
	LOG_MEAN='Log Mean'
	NA='NA'


class study_type(enum.Enum):
	INTERVENTIONAL= 'Interventional'
	OBSERVATIONAL= 'Observational'
	PATIENT_REGISTRY='Patient Registry'
	EXPANDED_ACCESS='Expanded Access'


class purpose(enum.Enum):
	TREATMENT='Treatment'
	PREVENTION='Prevention'
	BASIC_SCIENCE='Basic Science'
	OTHER='Other'
	SUPPORTIVE_CARE='Supportive Care'
	DIAGNOSTIC='Diagnostic'
	HEALTH_SERVICES_RESEARCH='Health Services Research'
	SCREENING='Screening'
	DEVICE_FEASIBILITY='Device Feasibility'
	NA='NA'

class gender(enum.Enum):
	ALL='ALL'
	FEMALE='Female'
	MALE='Male'
	NA='NA'


class intervention_type(enum.Enum):
	PARALLEL_ASSIGNMENT='Parallel Assignment'
	SINGLE_GROUP_ASSIGNMENT='Single Group Assignment'
	CROSSOVER_ASSIGNMENT='Crossover Assignment'
	FACTORIAL_ASSIGNMENT='Factorial Assignment'
	SEQUENTIAL_ASSIGNMENT='Sequential Assignment'
	NA='NA'


class measure_type(enum.Enum):
	PRIMARY='Primary'
	SECONDARY='Secondary'
	OTHER='Other'


class group_type(enum.Enum):
	EXPERIMENTAL='Experimental'
	ACTIVE_COMPARATOR='Active Comparator'
	PLACEBO_COMPARATOR='Placebo Comparator'
	SHAM_COMPARATOR='Sham Comparator'
	NO_INTERVENTION='No Intervention'
	OTHER='Other'


class non_inferiority_type(enum.Enum):
	SUPERIORITY_OR_OTHER='Superiority or Other'
	SUPERIORITY='Superiority'
	OTHER='Other'
	SUPERIORITY_OR_OTHER_LEGACY='Superiority or Other (legacy)'
	NON_INFERIORITY_OR_EQUIVALENCE='Non-Inferiority or Equivalence'
	NON_INFERIORITY='Non-Inferiority'
	NON_INFERIORITY_OR_EQUIVALENCE_LEGACY='Non-Inferiority or Equivalence (legacy)'


class dispersion_param(enum.Enum):
	STANDARD_DEVIATION='Standard Deviation'
	CONFIDENCE_INTERVAL_95='95% Confidence Interval'
	STANDARD_ERROR='Standard Error'
	FULL_RANGE='Full Range'
	GEOMETRIC_COEFFICIENT_OF_VARIATION= 'Geometric Coefficient of Variation'
	INTER_QUARTILE_RANGE='Inter-Quartile Range'
	CONFIDENCE_INTERVAL_90='90% Confidence Interval'
	CONFIDENCE_INTERVAL_80='80% Confidence Interval'
	CONFIDENCE_INTERVAL_97='97% Confidence Interval'
	CONFIDENCE_INTERVAL_99='99% Confidence Interval'
	CONFIDENCE_INTERVAL_60='60% Confidence Interval'
	CONFIDENCE_INTERVAL_96='96% Confidence Interval'
	CONFIDENCE_INTERVAL_98='98% Confidence Interval'
	CONFIDENCE_INTERVAL_70='70% Confidence Interval'
	CONFIDENCE_INTERVAL_85='85% Confidence Interval'
	CONFIDENCE_INTERVAL_75='75% Confidence Interval'
	CONFIDENCE_INTERVAL_94='94% Confidence Interval'
	CONFIDENCE_INTERVAL_100='100% Confidence Interval'
	NA='NA'


class Study(db.Model):

	__tablename__ = 'studies'

	id = db.Column(db.String(11), primary_key=True)
	upload_date = db.Column(db.Date)
	short_title = db.Column(db.String(300))
	official_title = db.Column(db.String(600))
	description = db.Column(db.String(5000))
	responsible_party = db.Column(db.Enum(resonsible_party_type))
	sponser = db.Column(db.String(160))
	type = db.Column(db.Enum(study_type))
	purpose = db.Column(db.Enum(purpose))
	intervention_type = db.Column(db.Enum(intervention_type))
	min_age= db.Column(db.Integer)
	max_age = db.Column(db.Integer)
	gender = db.Column(db.Enum(gender))

	criteria = db.relationship('Criteria', lazy='dynamic')
	conditions = db.relationship('StudyCondition', lazy='dynamic')
	measures = db.relationship('Measure', lazy='dynamic')
	analytics = db.relationship('Analytics', lazy='dynamic')



class Criteria(db.Model):

	__tablename__ = 'criteria'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	criteria = db.Column(db.String(500))
	is_inclusion = db.Column(db.Boolean)


class Condition(db.Model):

	__tablename__ = 'conditions'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), index=True, unique=True)
	studies = db.relationship('StudyCondition', lazy='dynamic')


class StudyCondition(db.Model):

	__tablename__ = 'study_conditions'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	condition = db.Column(db.Integer, db.ForeignKey('conditions.id'))


class Measure(db.Model):

	__tablename__ = 'measures'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	title = db.Column(db.String(254))
	description = db.Column(db.String(999))
	dispersion = db.Column(db.Enum(dispersion_param))
	type = db.Column(db.Enum(measure_type))
	param = db.Column(db.Enum(measure_param))
	units = db.Column(db.String(40))


class Company(db.Model):

	__tablename__ = 'companies'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))

	treatments = db.relationship('Treatment', lazy='dynamic')


class Treatment(db.Model):

	__tablename__ = 'treatments'

	id = db.Column(db.Integer, primary_key=True)
	company = db.Column(db.Integer, db.ForeignKey('companies.id'))
	name = db.Column(db.String(100))

	administrations = db.relationship('Administration', lazy='dynamic')


class Group(db.Model):

	__tablename__ = 'groups'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	description = db.Column(db.String(999))
	type = db.Column(db.Enum(group_type))
	participants = db.Column(db.Integer)

	administrations = db.relationship('Administration', lazy='dynamic')
	analytics = db.relationship('Comparison', lazy='dynamic')


class Administration(db.Model):

	__tablename__ = 'administrations'

	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.Integer, db.ForeignKey('groups.id'))
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))
	description = db.Column(db.String(1000))


class Analytics(db.Model):

	__tablename__ = 'analytics'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	measure = db.Column(db.Integer, db.ForeignKey('measures.id'))
	from_study = db.Column(db.Boolean)
	method = db.Column(db.String(100))
	p_value = db.Column(db.Float)
	param_type = db.Column(db.String(100))
	is_non_inferiority = db.Column(db.Boolean)
	non_inferiority_type = db.Column(db.Enum(non_inferiority_type))
	non_inferiority_comment = db.Column(db.String(500))
	param_value = db.Column(db.Float)
	ci_pct = db.Column(db.Integer)
	ci_lower = db.Column(db.Float)
	ci_upper = db.Column(db.Float)

	groups = db.relationship('Comparison', lazy='dynamic')


class Comparison(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	analytic = db.Column(db.Integer, db.ForeignKey('analytics.id'))
	group = db.Column(db.Integer, db.ForeignKey('groups.id'))


class Baseline(db.Model):

	__tablename__ = 'baselines'

	id = db.Column(db.Integer, primary_key=True)
	base = db.Column(db.String(100))
	clss = db.Column(db.String(100))
	category = db.Column(db.String(50))
	param_type = db.Column(db.Enum(measure_param))
	dispersion = db.Column(db.Enum(dispersion_param))
	unit = db.Column(db.String(40))
	value = db.Column(db.Float)
	spread = db.Column(db.Float)
	upper = db.Column(db.Float)
	type = db.Column(db.Enum(baseline_type))
	sub_type = db.Column(db.Enum(baseline_subtype))
