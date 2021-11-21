from app import db 

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import func, select
import enum


class baseline_type(enum.Enum):
	RACE='Race'
	GENDER='Gender'
	ETHNICITY='ETHNICITY'
	AGE='AGE'
	OTHER='OTHER'


class effect_type(enum.Enum):
	SERIOUS='Serious'
	OTHER='Other'


class effect_collection_method(enum.Enum):
	SYSTEMATIC_ASSESSMENT='Systematic Assessment',
	NON_SYSTEMATIC_ASSESSMENT='Non-Systematic Assessment',
	NA='NA'


class organ_system(enum.Enum):
	BLOOD_AND_LYMPHATIC_SYSTEM_DISORDERS='Blood and lymphatic system disorders',
	CARDIAC_DISORDERS='Cardiac disorders',
	CONGENITAL_FAMILIAL_AND_GENETIC_DISORDERS='Congenital, familial and genetic disorders',
	EAR_AND_LABYRINTH_DISORDERS='Ear and labyrinth disorders',
	ENDOCRINE_DISORDERS='Endocrine disorders',
	EYE_DISORDERS='Eye disorders',
	GASTROINTESTINAL_DISORDERS='Gastrointestinal disorders',
	GENERAL_DISORDERS='General disorders',
	HEPATOBILIARY_DISORDERS='Hepatobiliary disorders',
	IMMUNE_SYSTEM_DISORDERS='Immune system disorders',
	INFECTIONS_AND_INFESTATIONS='Infections and infestations',
	INJURY_POISONING_AND_PROCEDURAL_COMPLICATIONS='Injury, poisoning and procedural complications',
	INVESTIGATIONS='Investigations',
	METABOLISM_AND_NUTRITION_DISORDERS='Metabolism and nutrition disorders',
	MUSCULOSKELETAL_AND_CONNECTIVE_TISSUE_DISORDERS='Musculoskeletal and connective tissue disorders',
	NEOPLASMS_BENIGN_MALIGNANT_AND_UNSPECIFIED='Neoplasms benign, malignant and unspecified (incl cysts and polyps)',
	NERVOUS_SYSTEM_DISORDERS='Nervous system disorders',
	PREGNANCY_PUERPERIUM_AND_PERINATAL_CONDITIONS='Pregnancy, puerperium and perinatal conditions',
	PRODUCT_ISSUES='Product Issues',
	PSYCHIATRIC_DISORDERS='Psychiatric disorders',
	RENAL_AND_URINARY_DISORDERS='Renal and urinary disorders',
	REPRODUCTIVE_SYSTEM_AND_BREAST_DISORDERS='Reproductive system and breast disorders',
	RESPIRATORY_THORACIC_AND_MEDIASTINAL_DISORDERS='Respiratory, thoracic and mediastinal disorders',
	SKIN_AND_SUBCUTANEOUS_TISSUE_DISORDERS='Skin and subcutaneous tissue disorders',
	SOCIAL_CIRCUMSTANCES='Social circumstances',
	SURGICAL_AND_MEDICAL_PROCEDURES='Surgical and medical procedures',
	VASCULAR_DISORDERS='Vascular disorders',


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
	MEDIAN='Median'
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
	ALL='All'
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
	EQUIVAlENCE='Equivalence'
	NA='NA'


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


class age_units(enum.Enum):
	YEARS='years',
	MONTHS='Months',
	WEEKS='Weeks',
	DAYS='Days',
	HOURS='Hours',
	MINUTES='Minutes',
	NA='NA'


class Study(db.Model):

	__tablename__ = 'studies'

	id = db.Column(db.String(11), primary_key=True)
	upload_date = db.Column(db.Date)
	short_title = db.Column(db.String(300))
	official_title = db.Column(db.String(600))
	description = db.Column(db.String(5000))
	responsible_party = db.Column(db.String(160))
	sponsor = db.Column(db.String(160))
	type = db.Column(db.Enum(study_type))
	purpose = db.Column(db.Enum(purpose))
	intervention_type = db.Column(db.Enum(intervention_type))
	min_age = db.Column(db.Integer)
	min_age_units = db.Column(db.Enum(age_units))
	max_age = db.Column(db.Integer)
	max_age_units = db.Column(db.Enum(age_units))
	gender = db.Column(db.Enum(gender))

	criteria = db.relationship('Criteria', lazy='joined')
	conditions = db.relationship('StudyCondition', lazy='joined')
	treatments = db.relationship('StudyTreatment', lazy='joined')
	measures = db.relationship('Measure', lazy='joined')
	analytics = db.relationship('Analytics', lazy='joined')
	baselines = db.relationship('Baseline', lazy='joined')
	groups = db.relationship('Group', lazy='joined')


	def to_dict(self):
		return {
			'id': self.id,
			'upload_date': self.upload_date,
			'short_title': self.short_title,
			'official_title': self.official_title,
			'description': self.description,
			'responsible_party': self.responsible_party,
			'sponsor': self.sponsor,
			'type': str(self.type),
			'purpose': str(self.purpose),
			'intervention_type': str(self.intervention_type),
			'min_age': self.min_age,
			'min_age_units': str(self.min_age_units),
			'max_age': self.max_age,
			'min_age_units': str(self.max_age_units),
			'gender': str(self.gender),
			'criteria': [x.to_dict() for x in self.criteria],
			'measures': [x.to_dict() for x in self.measures],
			'analytics': [x.to_dict() for x in self.analytics],
			'baselines': [x.to_dict() for x in self.baselines],
			'groups': [x.to_dict() for x in self.groups],
			'conditions': [x.conditions.to_dict() for x in self.conditions],
			'treatments': [x.treatments.to_dict() for x in self.treatments]
		}


class Criteria(db.Model):

	__tablename__ = 'criteria'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	criteria = db.Column(db.String(500))
	is_inclusion = db.Column(db.Boolean)


class Condition(db.Model):

	__tablename__ = 'conditions'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), index=True, unique=True)

	studies = db.relationship('StudyCondition', lazy='joined', backref='conditions')
	treatment_scores = db.relationship('ConditionScore', lazy='dynamic')

	@hybrid_property
	def no_studies(self):
		if self.studies:
			return len(self.studies)
		return 0

	@no_studies.expression
	def no_studies(cls):
		return select([func.count(StudyCondition.id)]).\
			where(StudyCondition.condition==cls.id).\
			group_by(cls.id).\
			label('no_studies')

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name
		}


class StudyCondition(db.Model):

	__tablename__ = 'study_conditions'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	condition = db.Column(db.Integer, db.ForeignKey('conditions.id'))


class StudyTreatment(db.Model):

	__tablename__ = 'study_treatments'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))


class Measure(db.Model):

	__tablename__ = 'measures'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	title = db.Column(db.String(256))
	description = db.Column(db.String(1005))
	dispersion = db.Column(db.Enum(dispersion_param))
	type = db.Column(db.Enum(measure_type))
	param = db.Column(db.Enum(measure_param))
	units = db.Column(db.String(40))

	outcomes = db.relationship('Outcome', lazy='joined')

	def to_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'title': self.title,
			'description': self.description,
			'dispersion': str(self.dispersion),
			'type': str(self.type),
			'param': str(self.param),
			'units': self.units,
			'outcomes': [x.to_dict() for x in self.outcomes]
		}


class Company(db.Model):

	__tablename__ = 'companies'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))


class Treatment(db.Model):

	__tablename__ = 'treatments'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(400))
	from_study = db.Column(db.Boolean)
	no_studies = db.Column(db.Integer)

	studies = db.relationship('StudyTreatment', lazy='joined', backref='treatments')
	administrations = db.relationship('Administration', lazy='dynamic')
	condition_scores = db.relationship('ConditionScore', lazy='dynamic')

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'from_study': self.from_study,
			'no_studies': self.no_studies
		}


class ConditionScore(db.Model):

	__tablename__ = 'conditionscores'

	id = db.Column(db.Integer, primary_key=True)
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))
	condition = db.Column(db.Integer, db.ForeignKey('conditions.id'))
	mixed_score = db.Column(db.Float)
	singular_score = db.Column(db.Float)

	def to_dict(self):
		return {
			'id': self.id,
			'treatment': self.treatment,
			'condition': self.condition,
			'mixed_score': self.mixed_score,
			'singular_score': self.singular_score
		}


class Group(db.Model): # These are just the outcome groups for now

	__tablename__ = 'groups'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	study_id = db.Column(db.String(7))
	description = db.Column(db.String(1500))
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))

	administrations = db.relationship('Administration', lazy='dynamic')
	analytics = db.relationship('Comparison', lazy='dynamic')

	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'study_id': self.study_id,
			'description': self.description,
			'study': self.study
		}


class Outcome(db.Model):

	__tablename__ = 'outcomes'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	group = db.Column(db.Integer, db.ForeignKey('groups.id'))
	measure = db.Column(db.Integer, db.ForeignKey('measures.id'))
	title = db.Column(db.String(225))
	value = db.Column(db.Float)
	dispersion = db.Column(db.Float)
	upper = db.Column(db.Float)
	lower = db.Column(db.Float)
	no_participants = db.Column(db.Integer)

	def to_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'group': self.group,
			'measure': self.measure,
			'title': self.title,
			'value': self.value,
			'dispersion': self.dispersion,
			'upper': self.upper,
			'lower': self.lower,
			'no_participants': self.no_participants
		}


class Administration(db.Model):

	__tablename__ = 'administrations'

	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.Integer, db.ForeignKey('groups.id'))
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))
	description = db.Column(db.String(1500))


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

	groups = db.relationship('Comparison', lazy='joined')

	def to_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'measure': self.measure,
			'from_study': self.from_study,
			'method': self.method,
			'p_value': self.p_value,
			'param_type': self.param_type,
			'is_non_inferiority': self.is_non_inferiority,
			'non_inferiority_type': str(self.non_inferiority_type),
			'non_inferiority_comment': self.non_inferiority_comment,
			'param_value': self.param_value,
			'ci_pct': self.ci_pct,
			'ci_lower': self.ci_lower,
			'ci_upper': self.ci_upper,
			'groups': [x.to_dict() for x in self.groups]
		}

	def to_small_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'measure': self.measure,
			'from_study': self.from_study,
			'method': self.method,
			'p_value': self.p_value,
			'param_type': self.param_type,
			'is_non_inferiority': self.is_non_inferiority,
			'non_inferiority_type': str(self.non_inferiority_type),
			'param_value': self.param_value,
			'ci_pct': self.ci_pct,
			'ci_lower': self.ci_lower,
			'ci_upper': self.ci_upper,
			'groups': [x.to_dict() for x in self.groups]
		}
		

class Comparison(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	analytic = db.Column(db.Integer, db.ForeignKey('analytics.id'))
	group = db.Column(db.Integer, db.ForeignKey('groups.id'))

	def to_dict(self):
		return {
			'id': self.id,
			'analytic': self.analytic,
			'group': self.group
		}


class Baseline(db.Model):

	__tablename__ = 'baselines'

	id = db.Column(db.Integer, primary_key=True)
	base = db.Column(db.String(100))
	clss = db.Column(db.String(100))
	category = db.Column(db.String(100))
	param_type = db.Column(db.Enum(measure_param))
	dispersion = db.Column(db.Enum(dispersion_param))
	unit = db.Column(db.String(40))
	value = db.Column(db.Float)
	spread = db.Column(db.Float)
	upper = db.Column(db.Float)
	lower = db.Column(db.Float)
	type = db.Column(db.Enum(baseline_type))
	sub_type = db.Column(db.Enum(baseline_subtype))
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))

	def is_demographic(self):
		return (self.type != baseline_type.OTHER)

	def to_dict(self):
		return {
			'id': self.id,
			'base': self.base,
			'class': self.clss,
			'category': self.category,
			'param_type': str(self.param_type),
			'dispersion': str(self.dispersion),
			'unit': self.unit,
			'value': self.value,
			'spread': self.spread,
			'upper': self.upper,
			'lower': self.lower,
			'type': str(self.type),
			'sub_type': str(self.sub_type),
			'study': self.study
		}


class Effect(db.Model):

	__tablename__ = 'effects'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.String(11), db.ForeignKey('studies.id'))
	group = db.Column(db.Integer, db.ForeignKey('effectsgroups.id'))
	name = db.Column(db.String(100))
	organ_system = db.Column(db.Enum(organ_system))
	effect_type = db.Column(db.Enum(effect_type))
	assessment = db.Column(db.Enum(effect_collection_method))
	no_effected = db.Column(db.Float)
	no_at_risk = db.Column(db.Integer)
	collection_threshold = db.Column(db.Float)

	def to_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'group': self.group,
			'name': self.name,
			'organ_system': str(self.organ_system),
			'effect_type': str(self.effect_type),
			'assessment': str(self.assessment),
			'no_effected': self.no_effected,
			'no_at_risk': self.no_at_risk,
			'collection_threshold': self.collection_threshold
		}


class EffectGroup(db.Model):

	__tablename__ = 'effectsgroups'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(101))
	description = db.Column(db.String(1500))
	study_id = db.Column(db.String(7))

	effects = db.relationship('Effect', lazy='dynamic')


class EffectAdministration(db.Model):

	__tablename__ = 'effectsadministrations'

	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.Integer, db.ForeignKey('effectsgroups.id'))
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))



