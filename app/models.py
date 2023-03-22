from app import db 

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import CheckConstraint
from sqlalchemy import func, select
from app.utils import enum2String
import uuid
import enum


BOARD_ID_SEQ = db.Sequence('board_id_seq')

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


class baseline_param(enum.Enum):
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


class phase_type(enum.Enum):
	NA = 'NA'
	EARLY_PHASE_1 = 'Early Phase 1'
	PHASE_1 = 'Phase 1'
	PHASE_1_PHASE_2 = 'Phase 1 Phase 2'
	PHASE_2 = 'Phase 2'
	PHASE_2_PHASE_3 = 'Phase 2 Phase 3'
	PHASE_3 = 'Phase 3'
	PHASE_4 = 'Phase 4'


class study_type(enum.Enum):
	INTERVENTIONAL= 'Interventional'
	OBSERVATIONAL= 'Observational'
	PATIENT_REGISTRY='Patient Registry'
	EXPANDED_ACCESS='Expanded Access'
	NA='NA'


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
	EDUCATIONAL_COUNSELING_TRAINING = 'Educational/Counseling/Training'
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


class measure_group_type(enum.Enum):
	PRIMARY='Primary'
	SECONDARY='Secondary'
	OTHER='Other'
	IRRELEVANT='Irrelevant'


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
	EQUIVALENCE='Equivalence'
	NA='NA'


# class baseline_dispersion_param(enum.Enum):
# 	STANDARD_DEVIATION='Standard Deviation'
# 	CONFIDENCE_INTERVAL_95='95% Confidence Interval'
# 	STANDARD_ERROR='Standard Error'
# 	FULL_RANGE='Full Range'
# 	GEOMETRIC_COEFFICIENT_OF_VARIATION= 'Geometric Coefficient of Variation'
# 	INTER_QUARTILE_RANGE='Inter-Quartile Range'
# 	CONFIDENCE_INTERVAL_90='90% Confidence Interval'
# 	CONFIDENCE_INTERVAL_80='80% Confidence Interval'
# 	CONFIDENCE_INTERVAL_97='97% Confidence Interval'
# 	CONFIDENCE_INTERVAL_99='99% Confidence Interval'
# 	CONFIDENCE_INTERVAL_60='60% Confidence Interval'
# 	CONFIDENCE_INTERVAL_96='96% Confidence Interval'
# 	CONFIDENCE_INTERVAL_98='98% Confidence Interval'
# 	CONFIDENCE_INTERVAL_70='70% Confidence Interval'
# 	CONFIDENCE_INTERVAL_85='85% Confidence Interval'
# 	CONFIDENCE_INTERVAL_75='75% Confidence Interval'
# 	CONFIDENCE_INTERVAL_94='94% Confidence Interval'
# 	CONFIDENCE_INTERVAL_100='100% Confidence Interval'
# 	NA='NA'


class measure_dispersion_param(enum.Enum):
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


class max_age_units(enum.Enum):
	YEARS='years',
	MONTHS='Months',
	WEEKS='Weeks',
	DAYS='Days',
	HOURS='Hours',
	MINUTES='Minutes',
	NA='NA'


class min_age_units(enum.Enum):
	YEARS='years',
	MONTHS='Months',
	WEEKS='Weeks',
	DAYS='Days',
	HOURS='Hours',
	MINUTES='Minutes',
	NA='NA'


class insight_Type(enum.Enum):
	STUDY='study',
	BASELINE='baseline',
	MEASURE='measure',
	ADVERSE_EFFECT='adverse_effect'


class study_status(enum.Enum):
	NOT_YET_RECRUITING='not yet recruiting'
	RECRUITING='recruiting'
	ENROLLING='enrolling'
	ACTIVE='active'
	ACTIVE_NOT_RECRUITING='active not recruiting'
	COMPLETED='completed'
	SUSPENDED='suspended'
	TERMINATED='terminated'
	WITHDRAWN='withdrawn'
	ENROLLING_BY_INVITATION='enrolling by invitation'
	NO_LONGER_AVAILABLE='no longer available'
	AVAILABLE='available'
	APPROVED_FOR_MARKETING='approved for marketing'
	TEMPORARILY_NOT_AVAILABLE='temporarily not available'
	UNKNOWN_STATUS='unknown status'
	WITHHELD='withheld'


class completion_date_type(enum.Enum):
	ACTUAL='actual'
	ANTICIPATED='anticipated'
	NA='NA'


class design_allocation(enum.Enum):
	RANDOMIZED='randomized'
	NON_RANDOMIZED='non_randomized'
	NA='NA'


class observational_model(enum.Enum):
	COHORT='cohort'
	CASE_CONTROL='case control'
	CASE_ONLY='case only'
	OTHER='other'
	ECOLOGIC_OR_COMMUNITY='ecologic or community'
	CASE_CROSSOVER='case crossover'
	DEFINED_POPULATION='defined population'
	FAMILY_BASED='family based'
	NATURAL_HISTORY='natural history'
	NA='NA'


class design_time_perspective(enum.Enum):
	PROSPECTIVE='prospective'
	RETROSPECTIVE='retrospective'
	CROSS_SECTIONAL='cross sectional'
	OTHER='other'
	NA='NA'


class design_masking(enum.Enum):
	NONE='none'
	SINGLE='single'
	DOUBLE='double'
	QUADRUPLE='quadruple'
	TRIPLE='triple'
	NA='NA'


class who_masked(enum.Enum):
	PARTICIPANT='participant'
	INVESTIGATOR='investigator'
	OUTCOMES_ASSESSOR='outcomes assessor'
	CARE_PROVIDER='care provider'
	NA='NA'


class Study(db.Model):

	__tablename__ = 'studies'

	id = db.Column(db.Integer, BOARD_ID_SEQ, server_default=BOARD_ID_SEQ.next_value(), primary_key=True)
	nct_id = db.Column(db.String(11))
	upload_date = db.Column(db.Date)
	short_title = db.Column(db.String(300))
	official_title = db.Column(db.String(600))
	description = db.Column(db.String(5000))
	responsible_party = db.Column(db.String(160))
	sponsor = db.Column(db.String(160))
	phase = db.Column(db.Enum(phase_type))
	type = db.Column(db.Enum(study_type))
	purpose = db.Column(db.Enum(purpose))
	intervention_type = db.Column(db.Enum(intervention_type))
	min_age = db.Column(db.Integer)
	min_age_units = db.Column(db.Enum(min_age_units))
	max_age = db.Column(db.Integer)
	max_age_units = db.Column(db.Enum(max_age_units))
	gender = db.Column(db.Enum(gender))
	results_summary = db.Column(db.Integer)
	completion_date = db.Column(db.Date)
	completion_date_type = db.Column(db.Enum(completion_date_type))
	stopped_reason = db.Column(db.String(251))
	status = db.Column(db.Enum(study_status))
	primary_success = db.Column(db.SmallInteger, nullable=False, server_default='-1')

	design_allocation = db.Column(db.Enum(design_allocation))
	design_masking = db.Column(db.Enum(design_masking))
	design_time_perspective = db.Column(db.Enum(design_time_perspective))
	who_masked = db.Column(db.ARRAY(db.Enum(who_masked)))
	observational_model = db.Column(db.Enum(observational_model))
	masking_description = db.Column(db.String(1200))
	model_description = db.Column(db.String(1100))

	criteria = db.relationship('Criteria', lazy='dynamic')

	conditions = db.relationship(
		'Condition',
		secondary="study_conditions",
		back_populates="studies")

	treatments = db.relationship(
		'Treatment',
		secondary="study_treatments",
		back_populates="studies")

	measures = db.relationship('Measure')
	analytics = db.relationship('Analytics')
	baselines = db.relationship('Baseline', lazy='dynamic')
	groups = db.relationship('Group', lazy='dynamic')
	effects = db.relationship('Effect')

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
			'conditions': [x.to_dict() for x in self.conditions],
			'treatments': [x.to_dict() for x in self.treatments]
		}

	def to_summary_dict(self):
		return {
			**self.to_core_dict(),
			'conditions': [x.to_dict() for x in self.conditions],
			'treatments': [x.to_dict() for x in self.treatments],
		}

	def to_summary_effects_dict(self):
		effects = {x['name']: x for x in [x.to_min_dict() for x in sorted(self.effects, key=lambda x: x.no_effected)]}
		effects = list(effects.values())

		return {
			**self.to_core_dict(),
			'conditions': [x.to_dict() for x in self.conditions],
			'treatments': [x.to_dict() for x in self.treatments],
			'effects': effects
		}

	def to_core_dict(self):
		return {
			'id': self.id,
			'upload_date': self.upload_date,
			'short_title': self.short_title,
			'official_title': self.official_title,
			'description': self.description,
			'responsible_party': self.responsible_party,
			'results_summary': self.results_summary,
			'sponsor': self.sponsor,
			'type': enum2String(self.type),
			'purpose': enum2String(self.purpose),
			'intervention_type': str(self.intervention_type),
			'phase': enum2String(self.phase),
			'min_age': self.min_age,
			'min_age_units': str(self.min_age_units),
			'max_age': self.max_age,
			'min_age_units': str(self.max_age_units),
			'gender': str(self.gender),
			'completion_date': str(self.completion_date),
			'status': enum2String(self.status),
			'stopped_reason': self.stopped_reason,
			'external_ids': [self.nct_id],
			'primary_success': self.primary_success
		}


class Search(db.Model):

	__tablename__ = 'searches'

	id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	name = db.Column(db.String(300), nullable=False)
	search_string = db.Column(db.String(2000))
	original_user = db.Column(db.String(1000), index=True)

	def to_dict(self):
		# Not going to return the original user
		return {
			'id': self.id,
			'name': self.name,
			'search_string': self.search_string
		}


	def from_dict(self, data):
		for field, value in data.items():
			setattr(self, field, value)


class Insight(db.Model):

	__tablename__ = 'insights'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'))
	measure = db.Column(db.Integer, db.ForeignKey('measures.id'))
	type = db.Column(db.Enum(insight_Type))
	body = db.Column(db.String(1000))

	def to_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'measure': self.measure,
			'type': str(self.type),
			'body': self.body
		}

	def from_dict(self, data):
		for field, value in data.items():
			setattr(self, field, value)


class Criteria(db.Model):

	__tablename__ = 'criteria'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'))
	criteria = db.Column(db.String(500))
	is_inclusion = db.Column(db.Boolean)


class ConditionGroup(db.Model):

	__tablename__ = 'condition_groups'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(400))

	conditions = db.relationship('Condition')

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'conditions': [condition.to_dict() for condition in self.conditions]
		}


class Condition(db.Model):

	__tablename__ = 'conditions'

	id = db.Column(db.Integer, primary_key=True)
	condition_group = db.Column(db.Integer, db.ForeignKey('condition_groups.id'))
	name = db.Column(db.String(200), index=True, unique=True)

	studies = db.relationship(
		'Study',
		secondary='study_conditions',
		back_populates='conditions')
	
	treatment_scores = db.relationship('ConditionScore', lazy='dynamic')

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'condition_group': self.condition_group,
		}


class StudyCondition(db.Model):

	__tablename__ = 'study_conditions'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'), index=True)
	condition = db.Column(db.Integer, db.ForeignKey('conditions.id'), index=True)


class TreatmentGroup(db.Model):

	__tablename__ = 'treatment_groups'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(400))

	treatments = db.relationship('Treatment', lazy='dynamic')


class StudyTreatment(db.Model):

	__tablename__ = 'study_treatments'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'), index=True)
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'), index=True)


class MeasureGroup(db.Model):

	__tablename__ = 'measure_groups'

	id = db.Column(db.Integer, primary_key=True)
	condition = db.Column(db.Integer, db.ForeignKey('conditions.id'))
	name = db.Column(db.String(256))
	type = db.Column(db.Enum(measure_group_type))

	measures = db.relationship(
		'Measure',
		secondary='measure_group_measures',
		back_populates='measureGroups')

	def to_dict(self):
		return {
			'id': self.id,
			'condition': self.condition,
			'name': self.name,
			'type': str(self.type),
		}


class MeasureGroupMeasure(db.Model):

	__tablename__ = 'measure_group_measures'

	id = db.Column(db.Integer, primary_key=True)
	measure = db.Column(db.Integer, db.ForeignKey('measures.id'))
	measureGroup = db.Column(db.Integer, db.ForeignKey('measure_groups.id'))


class Measure(db.Model):

	__tablename__ = 'measures'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'))
	title = db.Column(db.String(256))
	description = db.Column(db.String(1005))
	dispersion = db.Column(db.String(50))
	type = db.Column(db.Enum(measure_type))
	param = db.Column(db.Enum(measure_param))
	units = db.Column(db.String(40))

	outcomes = db.relationship('Outcome')
	analytics = db.relationship('Analytics')

	measureGroups = db.relationship(
		'MeasureGroup',
		secondary='measure_group_measures',
		back_populates='measures')
    
	def to_dict(self):
		return {
			**self.to_small_dict(),
			'outcomes': [x.to_dict() for x in self.outcomes],
			'analytics': [x.to_dict() for x in self.analytics]
		}
    
	def to_outcome_dict(self):
		return {
			**self.to_small_dict(),
			'outcomes': [x.to_dict() for x in self.outcomes],
		}

	def to_small_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'title': self.title,
			'description': self.description,
			'dispersion': str(self.dispersion),
			'type': str(self.type),
			'param': str(self.param),
			'units': self.units,
		}


class Company(db.Model):

	__tablename__ = 'companies'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))


class Treatment(db.Model):

	__tablename__ = 'treatments'

	id = db.Column(db.Integer, primary_key=True)
	treatmentGroup = db.Column(db.Integer, db.ForeignKey('treatment_groups.id'))
	name = db.Column(db.String(400), unique=True)
	description = db.Column(db.String(5000))
	from_study = db.Column(db.Boolean)
	no_studies = db.Column(db.Integer)
	no_prescriptions = db.Column(db.Integer)

	studies = db.relationship(
		'Study',
		secondary='study_treatments',
		back_populates='treatments')

	groups = db.relationship(
		'Group',
		secondary='administrations',
		back_populates='treatments')

	bases = db.relationship(
		'TreatmentDiff',
		secondary='base_treatments_diffs',
		back_populates='bases')

	diffs = db.relationship(
		'TreatmentDiff',
		secondary='diff_treatments_diffs',
		back_populates='diffs')

	condition_scores = db.relationship('ConditionScore', lazy='dynamic')
	effect_administrations = db.relationship('EffectAdministration', lazy='select', backref='treatments')

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'treatment_group': self.treatmentGroup,
			'description': self.description,
			'from_study': self.from_study,
			'no_studies': self.no_studies
		}

	def from_dict(self, data):
		for field, value in data.items():
			setattr(self, field, value)


class TreatmentBrandName(db.Model):

	__tablename__ = 'treatment_brand_names'

	id = db.Column(db.Integer, primary_key=True)
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))
	brand_name = db.Column(db.String(400))


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
	study = db.Column(db.Integer, db.ForeignKey('studies.id'))
	title = db.Column(db.String(100))
	study_id = db.Column(db.Integer)
	description = db.Column(db.String(1500))
	annotated = db.Column(db.Boolean)

	treatments = db.relationship(
		'Treatment', 
		secondary='administrations',
		back_populates='groups')
	analytics = db.relationship(
		'Analytics', 
		secondary='comparison',
		back_populates='groups')
	outcomes = db.relationship('Outcome', backref='groups')

	def to_small_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'study_id': self.study_id,
			'description': self.description,
			'study': self.study,
			'annotated': self.annotated,
			'treatments': [x.to_dict() for x in self.treatments]
		}

	def to_measure_dict(self):
		return {
			**self.to_dict(),
			'outcomes': [x.to_dict() for x in self.outcomes],
		}

	def to_dict(self):
		return {
			**self.to_small_dict(),
		}

	def from_dict(self, data):
		for field, value in data.items():
			setattr(self, field, value)


class Outcome(db.Model):

	__tablename__ = 'outcomes'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'))
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
	annotated = db.Column(db.Boolean)

	def to_dict(self):
		return {
			'id': self.id,
			'group': self.group,
			'treatment': self.treatment,
		}

	def from_dict(self, data):
		for field, value in data.items():
			setattr(self, field, value)


class TreatmentDiff(db.Model):

	__tablename__ = 'treatment_diffs'

	id = db.Column(db.Integer, primary_key=True)
	condition = db.Column(db.Integer, db.ForeignKey('conditions.id'))

	# base
	# diff
	# measures (or groups?? - groups are more specific, but we need pairs of groups)
	# groups (how to store pairs?) (string or pairwise table)
	# string would be easier to implement but harder to update
	# I think we should do a pairwise table

	bases = db.relationship(
		'Treatment', 
		secondary='base_treatments_diffs',
		back_populates='bases')

	diffs = db.relationship(
		'Treatment', 
		secondary='diff_treatments_diffs',
		back_populates='diffs')

	group_pairs = db.relationship(
		'GroupPair', 
		secondary='group_pair_diffs',
		back_populates='diffs')

class BaseTreatmentsDiff(db.Model):

	__tablename__ = 'base_treatments_diffs'

	id = db.Column(db.Integer, primary_key=True)
	treatment_diff = db.Column(db.Integer, db.ForeignKey('treatment_diffs.id'))
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))


class DiffTreatmentsDiff(db.Model):

	__tablename__ = 'diff_treatments_diffs'

	id = db.Column(db.Integer, primary_key=True)
	treatment_diff = db.Column(db.Integer, db.ForeignKey('treatment_diffs.id'))
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))


class GroupPairsDiff(db.Model):

	__tablename__ = 'group_pair_diffs'

	id = db.Column(db.Integer, primary_key=True)
	group_pair = db.Column(db.Integer, db.ForeignKey('group_pairs.id'))
	treatment_diff = db.Column(db.Integer, db.ForeignKey('treatment_diffs.id'))


class GroupPair(db.Model):

	__tablename__ = 'group_pairs'

	id = db.Column(db.Integer, primary_key=True)
	group_a = db.Column(db.Integer, db.ForeignKey('groups.id'))
	group_b = db.Column(db.Integer, db.ForeignKey('groups.id'))

	diffs = db.relationship(
		'TreatmentDiff',
		secondary='group_pair_diffs',
		back_populates='group_pairs')


class Analytics(db.Model):

	__tablename__ = 'analytics'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'))
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

	groups = db.relationship(
		'Group',
		secondary='comparison',
		back_populates='analytics')

	def to_core_dict(self):
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
		}

	def to_dict(self):
		return {
			**self.to_core_dict(),
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
	study = db.Column(db.Integer, db.ForeignKey('studies.id'), index=True)
	base = db.Column(db.String(100))
	clss = db.Column(db.String(100))
	category = db.Column(db.String(100))
	param_type = db.Column(db.Enum(baseline_param))
	dispersion = db.Column(db.String(50))
	unit = db.Column(db.String(40))
	value = db.Column(db.Float)
	spread = db.Column(db.Float)
	upper = db.Column(db.Float)
	lower = db.Column(db.Float)
	type = db.Column(db.Enum(baseline_type))
	sub_type = db.Column(db.Enum(baseline_subtype))

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


class EffectCluster(db.Model):

	__tablename__ = 'effects_cluster'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))

	effects = db.relationship('Effect', lazy='dynamic')


class Effect(db.Model):

	__tablename__ = 'effects'

	id = db.Column(db.Integer, primary_key=True)
	study = db.Column(db.Integer, db.ForeignKey('studies.id'), index=True)
	group = db.Column(db.Integer, db.ForeignKey('effectsgroups.id'))
	cluster = db.Column(db.Integer, db.ForeignKey('effects_cluster.id'))
	cluster_name = db.Column(db.String(100))
	name = db.Column(db.String(100))
	organ_system = db.Column(db.Enum(organ_system))
	effect_type = db.Column(db.Enum(effect_type))
	assessment = db.Column(db.Enum(effect_collection_method))
	no_effected = db.Column(db.Float)
	no_at_risk = db.Column(db.Integer)
	collection_threshold = db.Column(db.Float)

	def to_min_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'no_effected': self.no_effected,
			'no_at_risk': self.no_at_risk
		}

	def to_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'group': self.group,
			'cluster': self.cluster,
			'cluster_name': self.cluster_name,
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
	study = db.Column(db.Integer, db.ForeignKey('studies.id'))
	title = db.Column(db.String(101))
	description = db.Column(db.String(1500))
	study_id = db.Column(db.Integer)

	effects = db.relationship('Effect', lazy='joined')
	administrations = db.relationship('EffectAdministration', lazy='joined')

	def to_dict(self):
		return {
			'id': self.id,
			'study': self.study,
			'title': self.title,
			'description': self.description,
			'treatments': [x.treatments.to_dict() for x in self.administrations],
			'effects': [x.to_dict() for x in self.effects]
		}


class EffectAdministration(db.Model):

	__tablename__ = 'effectsadministrations'

	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.Integer, db.ForeignKey('effectsgroups.id'))
	treatment = db.Column(db.Integer, db.ForeignKey('treatments.id'))

