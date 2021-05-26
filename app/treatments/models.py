from app import db 

import enum

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
	DEVICE FEASIBILITY='Device Feasibility'
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


class Study(db.model):

	__tablename__ = 'studies'

	nct_id = db.Column(db.String(11), primary_key=True)
	upload_date = db.Column(db.Date)
	name = db.Column(db.String(300))
	description = db.Column(db.String(5000))
	responsible_party = db.Column(db.String(100))


