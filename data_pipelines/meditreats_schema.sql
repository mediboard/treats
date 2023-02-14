--
-- PostgreSQL database dump
--

-- Dumped from database version 12.13
-- Dumped by pg_dump version 12.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: temp_schema; Type: SCHEMA; Schema: -; Owner: meditreats
--

CREATE SCHEMA temp_schema;


ALTER SCHEMA temp_schema OWNER TO meditreats;

--
-- Name: age_units; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.age_units AS ENUM (
    'YEARS',
    'MONTHS',
    'WEEKS',
    'DAYS',
    'HOURS',
    'MINUTES',
    'NA'
);


ALTER TYPE temp_schema.age_units OWNER TO meditreats;

--
-- Name: baseline_subtype; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.baseline_subtype AS ENUM (
    'WHITE',
    'BLACK',
    'ASIAN',
    'INDIAN',
    'PACIFIC',
    'MALE',
    'FEMALE',
    'NA'
);


ALTER TYPE temp_schema.baseline_subtype OWNER TO meditreats;

--
-- Name: baseline_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.baseline_type AS ENUM (
    'RACE',
    'GENDER',
    'ETHNICITY',
    'AGE',
    'OTHER'
);


ALTER TYPE temp_schema.baseline_type OWNER TO meditreats;

--
-- Name: dispersion_param; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.dispersion_param AS ENUM (
    'STANDARD_DEVIATION',
    'CONFIDENCE_INTERVAL_95',
    'STANDARD_ERROR',
    'FULL_RANGE',
    'GEOMETRIC_COEFFICIENT_OF_VARIATION',
    'INTER_QUARTILE_RANGE',
    'CONFIDENCE_INTERVAL_90',
    'CONFIDENCE_INTERVAL_80',
    'CONFIDENCE_INTERVAL_97',
    'CONFIDENCE_INTERVAL_99',
    'CONFIDENCE_INTERVAL_60',
    'CONFIDENCE_INTERVAL_96',
    'CONFIDENCE_INTERVAL_98',
    'CONFIDENCE_INTERVAL_70',
    'CONFIDENCE_INTERVAL_85',
    'CONFIDENCE_INTERVAL_75',
    'CONFIDENCE_INTERVAL_94',
    'CONFIDENCE_INTERVAL_100',
    'NA'
);


ALTER TYPE temp_schema.dispersion_param OWNER TO meditreats;

--
-- Name: effect_collection_method; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.effect_collection_method AS ENUM (
    'SYSTEMATIC_ASSESSMENT',
    'NON_SYSTEMATIC_ASSESSMENT',
    'NA'
);


ALTER TYPE temp_schema.effect_collection_method OWNER TO meditreats;

--
-- Name: effect_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.effect_type AS ENUM (
    'SERIOUS',
    'OTHER'
);


ALTER TYPE temp_schema.effect_type OWNER TO meditreats;

--
-- Name: gender; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.gender AS ENUM (
    'ALL',
    'FEMALE',
    'MALE',
    'NA'
);


ALTER TYPE temp_schema.gender OWNER TO meditreats;

--
-- Name: insight_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.insight_type AS ENUM (
    'STUDY',
    'BASELINE',
    'MEASURE',
    'ADVERSE_EFFECT'
);


ALTER TYPE temp_schema.insight_type OWNER TO meditreats;

--
-- Name: intervention_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.intervention_type AS ENUM (
    'PARALLEL_ASSIGNMENT',
    'SINGLE_GROUP_ASSIGNMENT',
    'CROSSOVER_ASSIGNMENT',
    'FACTORIAL_ASSIGNMENT',
    'SEQUENTIAL_ASSIGNMENT',
    'NA'
);


ALTER TYPE temp_schema.intervention_type OWNER TO meditreats;

--
-- Name: measure_group_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.measure_group_type AS ENUM (
    'PRIMARY',
    'SECONDARY',
    'OTHER',
    'IRRELEVANT'
);


ALTER TYPE temp_schema.measure_group_type OWNER TO meditreats;

--
-- Name: measure_param; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.measure_param AS ENUM (
    'MEAN',
    'NUMBER',
    'MEDIAN',
    'COUNT_OF_PARTICIPANTS',
    'LEAST_SQUARES_MEAN',
    'GEOMETRIC_MEAN',
    'COUNT_OF_UNITS',
    'GEOMETRIC_LEAST_SQUARES_MEAN',
    'LOG_MEAN',
    'NA'
);


ALTER TYPE temp_schema.measure_param OWNER TO meditreats;

--
-- Name: measure_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.measure_type AS ENUM (
    'PRIMARY',
    'SECONDARY',
    'OTHER'
);


ALTER TYPE temp_schema.measure_type OWNER TO meditreats;

--
-- Name: non_inferiority_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.non_inferiority_type AS ENUM (
    'SUPERIORITY_OR_OTHER',
    'SUPERIORITY',
    'OTHER',
    'SUPERIORITY_OR_OTHER_LEGACY',
    'NON_INFERIORITY_OR_EQUIVALENCE',
    'NON_INFERIORITY',
    'NON_INFERIORITY_OR_EQUIVALENCE_LEGACY',
    'EQUIVALENCE',
    'NA'
);


ALTER TYPE temp_schema.non_inferiority_type OWNER TO meditreats;

--
-- Name: organ_system; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.organ_system AS ENUM (
    'BLOOD_AND_LYMPHATIC_SYSTEM_DISORDERS',
    'CARDIAC_DISORDERS',
    'CONGENITAL_FAMILIAL_AND_GENETIC_DISORDERS',
    'EAR_AND_LABYRINTH_DISORDERS',
    'ENDOCRINE_DISORDERS',
    'EYE_DISORDERS',
    'GASTROINTESTINAL_DISORDERS',
    'GENERAL_DISORDERS',
    'HEPATOBILIARY_DISORDERS',
    'IMMUNE_SYSTEM_DISORDERS',
    'INFECTIONS_AND_INFESTATIONS',
    'INJURY_POISONING_AND_PROCEDURAL_COMPLICATIONS',
    'INVESTIGATIONS',
    'METABOLISM_AND_NUTRITION_DISORDERS',
    'MUSCULOSKELETAL_AND_CONNECTIVE_TISSUE_DISORDERS',
    'NEOPLASMS_BENIGN_MALIGNANT_AND_UNSPECIFIED',
    'NERVOUS_SYSTEM_DISORDERS',
    'PREGNANCY_PUERPERIUM_AND_PERINATAL_CONDITIONS',
    'PRODUCT_ISSUES',
    'PSYCHIATRIC_DISORDERS',
    'RENAL_AND_URINARY_DISORDERS',
    'REPRODUCTIVE_SYSTEM_AND_BREAST_DISORDERS',
    'RESPIRATORY_THORACIC_AND_MEDIASTINAL_DISORDERS',
    'SKIN_AND_SUBCUTANEOUS_TISSUE_DISORDERS',
    'SOCIAL_CIRCUMSTANCES',
    'SURGICAL_AND_MEDICAL_PROCEDURES',
    'VASCULAR_DISORDERS'
);


ALTER TYPE temp_schema.organ_system OWNER TO meditreats;

--
-- Name: phase_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.phase_type AS ENUM (
    'NA',
    'EARLY_PHASE_1',
    'PHASE_1',
    'PHASE_1_PHASE_2',
    'PHASE_2',
    'PHASE_2_PHASE_3',
    'PHASE_3',
    'PHASE_4'
);


ALTER TYPE temp_schema.phase_type OWNER TO meditreats;

--
-- Name: purpose; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.purpose AS ENUM (
    'TREATMENT',
    'PREVENTION',
    'BASIC_SCIENCE',
    'OTHER',
    'SUPPORTIVE_CARE',
    'DIAGNOSTIC',
    'HEALTH_SERVICES_RESEARCH',
    'SCREENING',
    'DEVICE_FEASIBILITY',
    'NA',
    'EDUCATIONAL_COUNSELING_TRAINING'
);


ALTER TYPE temp_schema.purpose OWNER TO meditreats;

--
-- Name: study_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.study_type AS ENUM (
    'INTERVENTIONAL',
    'OBSERVATIONAL',
    'PATIENT_REGISTRY',
    'EXPANDED_ACCESS'
);


ALTER TYPE temp_schema.study_type OWNER TO meditreats;

--
-- Name: age_units; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.age_units AS ENUM (
    'YEARS',
    'MONTHS',
    'WEEKS',
    'DAYS',
    'HOURS',
    'MINUTES',
    'NA'
);


ALTER TYPE temp_schema.age_units OWNER TO meditreats;

--
-- Name: baseline_subtype; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.baseline_subtype AS ENUM (
    'WHITE',
    'BLACK',
    'ASIAN',
    'INDIAN',
    'PACIFIC',
    'MALE',
    'FEMALE',
    'NA'
);


ALTER TYPE temp_schema.baseline_subtype OWNER TO meditreats;

--
-- Name: baseline_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.baseline_type AS ENUM (
    'RACE',
    'GENDER',
    'ETHNICITY',
    'AGE',
    'OTHER'
);


ALTER TYPE temp_schema.baseline_type OWNER TO meditreats;

--
-- Name: dispersion_param; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.dispersion_param AS ENUM (
    'STANDARD_DEVIATION',
    'CONFIDENCE_INTERVAL_95',
    'STANDARD_ERROR',
    'FULL_RANGE',
    'GEOMETRIC_COEFFICIENT_OF_VARIATION',
    'INTER_QUARTILE_RANGE',
    'CONFIDENCE_INTERVAL_90',
    'CONFIDENCE_INTERVAL_80',
    'CONFIDENCE_INTERVAL_97',
    'CONFIDENCE_INTERVAL_99',
    'CONFIDENCE_INTERVAL_60',
    'CONFIDENCE_INTERVAL_96',
    'CONFIDENCE_INTERVAL_98',
    'CONFIDENCE_INTERVAL_70',
    'CONFIDENCE_INTERVAL_85',
    'CONFIDENCE_INTERVAL_75',
    'CONFIDENCE_INTERVAL_94',
    'CONFIDENCE_INTERVAL_100',
    'NA'
);


ALTER TYPE temp_schema.dispersion_param OWNER TO meditreats;

--
-- Name: effect_collection_method; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.effect_collection_method AS ENUM (
    'SYSTEMATIC_ASSESSMENT',
    'NON_SYSTEMATIC_ASSESSMENT',
    'NA'
);


ALTER TYPE temp_schema.effect_collection_method OWNER TO meditreats;

--
-- Name: effect_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.effect_type AS ENUM (
    'SERIOUS',
    'OTHER'
);


ALTER TYPE temp_schema.effect_type OWNER TO meditreats;

--
-- Name: gender; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.gender AS ENUM (
    'ALL',
    'FEMALE',
    'MALE',
    'NA'
);


ALTER TYPE temp_schema.gender OWNER TO meditreats;

--
-- Name: insight_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.insight_type AS ENUM (
    'STUDY',
    'BASELINE',
    'MEASURE',
    'ADVERSE_EFFECT'
);


ALTER TYPE temp_schema.insight_type OWNER TO meditreats;

--
-- Name: intervention_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.intervention_type AS ENUM (
    'PARALLEL_ASSIGNMENT',
    'SINGLE_GROUP_ASSIGNMENT',
    'CROSSOVER_ASSIGNMENT',
    'FACTORIAL_ASSIGNMENT',
    'SEQUENTIAL_ASSIGNMENT',
    'NA'
);


ALTER TYPE temp_schema.intervention_type OWNER TO meditreats;

--
-- Name: measure_group_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.measure_group_type AS ENUM (
    'PRIMARY',
    'SECONDARY',
    'OTHER',
    'IRRELEVANT'
);


ALTER TYPE temp_schema.measure_group_type OWNER TO meditreats;

--
-- Name: measure_param; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.measure_param AS ENUM (
    'MEAN',
    'NUMBER',
    'MEDIAN',
    'COUNT_OF_PARTICIPANTS',
    'LEAST_SQUARES_MEAN',
    'GEOMETRIC_MEAN',
    'COUNT_OF_UNITS',
    'GEOMETRIC_LEAST_SQUARES_MEAN',
    'LOG_MEAN',
    'NA'
);


ALTER TYPE temp_schema.measure_param OWNER TO meditreats;

--
-- Name: measure_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.measure_type AS ENUM (
    'PRIMARY',
    'SECONDARY',
    'OTHER'
);


ALTER TYPE temp_schema.measure_type OWNER TO meditreats;

--
-- Name: non_inferiority_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.non_inferiority_type AS ENUM (
    'SUPERIORITY_OR_OTHER',
    'SUPERIORITY',
    'OTHER',
    'SUPERIORITY_OR_OTHER_LEGACY',
    'NON_INFERIORITY_OR_EQUIVALENCE',
    'NON_INFERIORITY',
    'NON_INFERIORITY_OR_EQUIVALENCE_LEGACY',
    'EQUIVALENCE',
    'NA'
);


ALTER TYPE temp_schema.non_inferiority_type OWNER TO meditreats;

--
-- Name: organ_system; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.organ_system AS ENUM (
    'BLOOD_AND_LYMPHATIC_SYSTEM_DISORDERS',
    'CARDIAC_DISORDERS',
    'CONGENITAL_FAMILIAL_AND_GENETIC_DISORDERS',
    'EAR_AND_LABYRINTH_DISORDERS',
    'ENDOCRINE_DISORDERS',
    'EYE_DISORDERS',
    'GASTROINTESTINAL_DISORDERS',
    'GENERAL_DISORDERS',
    'HEPATOBILIARY_DISORDERS',
    'IMMUNE_SYSTEM_DISORDERS',
    'INFECTIONS_AND_INFESTATIONS',
    'INJURY_POISONING_AND_PROCEDURAL_COMPLICATIONS',
    'INVESTIGATIONS',
    'METABOLISM_AND_NUTRITION_DISORDERS',
    'MUSCULOSKELETAL_AND_CONNECTIVE_TISSUE_DISORDERS',
    'NEOPLASMS_BENIGN_MALIGNANT_AND_UNSPECIFIED',
    'NERVOUS_SYSTEM_DISORDERS',
    'PREGNANCY_PUERPERIUM_AND_PERINATAL_CONDITIONS',
    'PRODUCT_ISSUES',
    'PSYCHIATRIC_DISORDERS',
    'RENAL_AND_URINARY_DISORDERS',
    'REPRODUCTIVE_SYSTEM_AND_BREAST_DISORDERS',
    'RESPIRATORY_THORACIC_AND_MEDIASTINAL_DISORDERS',
    'SKIN_AND_SUBCUTANEOUS_TISSUE_DISORDERS',
    'SOCIAL_CIRCUMSTANCES',
    'SURGICAL_AND_MEDICAL_PROCEDURES',
    'VASCULAR_DISORDERS'
);


ALTER TYPE temp_schema.organ_system OWNER TO meditreats;

--
-- Name: purpose; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.purpose AS ENUM (
    'TREATMENT',
    'PREVENTION',
    'BASIC_SCIENCE',
    'OTHER',
    'SUPPORTIVE_CARE',
    'DIAGNOSTIC',
    'HEALTH_SERVICES_RESEARCH',
    'SCREENING',
    'DEVICE_FEASIBILITY',
    'NA',
    'EDUCATIONAL_COUNSELING_TRAINING'
);


ALTER TYPE temp_schema.purpose OWNER TO meditreats;

--
-- Name: study_type; Type: TYPE; Schema: temp_schema; Owner: meditreats
--

CREATE TYPE temp_schema.study_type AS ENUM (
    'INTERVENTIONAL',
    'OBSERVATIONAL',
    'PATIENT_REGISTRY',
    'EXPANDED_ACCESS'
);


ALTER TYPE temp_schema.study_type OWNER TO meditreats;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: administrations; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.administrations (
    id integer NOT NULL,
    "group" integer,
    treatment integer,
    description character varying(1500),
    annotated boolean
);


ALTER TABLE temp_schema.administrations OWNER TO meditreats;

--
-- Name: administrations_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.administrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.administrations_id_seq OWNER TO meditreats;

--
-- Name: administrations_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.administrations_id_seq OWNED BY temp_schema.administrations.id;


--
-- Name: alembic_version; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE temp_schema.alembic_version OWNER TO meditreats;

--
-- Name: analytics; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.analytics (
    id integer NOT NULL,
    study character varying(11),
    measure integer,
    from_study boolean,
    method character varying(100),
    p_value double precision,
    param_type character varying(100),
    is_non_inferiority boolean,
    non_inferiority_type temp_schema.non_inferiority_type,
    non_inferiority_comment character varying(500),
    param_value double precision,
    ci_pct integer,
    ci_lower double precision,
    ci_upper double precision
);


ALTER TABLE temp_schema.analytics OWNER TO meditreats;

--
-- Name: analytics_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.analytics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.analytics_id_seq OWNER TO meditreats;

--
-- Name: analytics_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.analytics_id_seq OWNED BY temp_schema.analytics.id;


--
-- Name: base_treatments_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.base_treatments_diffs (
    id integer NOT NULL,
    treatment_diff integer,
    treatment integer
);


ALTER TABLE temp_schema.base_treatments_diffs OWNER TO meditreats;

--
-- Name: base_treatments_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.base_treatments_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.base_treatments_diffs_id_seq OWNER TO meditreats;

--
-- Name: base_treatments_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.base_treatments_diffs_id_seq OWNED BY temp_schema.base_treatments_diffs.id;


--
-- Name: baselines; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.baselines (
    id integer NOT NULL,
    base character varying(100),
    clss character varying(100),
    category character varying(100),
    param_type temp_schema.measure_param,
    dispersion temp_schema.dispersion_param,
    unit character varying(40),
    value double precision,
    spread double precision,
    upper double precision,
    lower double precision,
    type temp_schema.baseline_type,
    sub_type temp_schema.baseline_subtype,
    study character varying(11)
);


ALTER TABLE temp_schema.baselines OWNER TO meditreats;

--
-- Name: baselines_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.baselines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.baselines_id_seq OWNER TO meditreats;

--
-- Name: baselines_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.baselines_id_seq OWNED BY temp_schema.baselines.id;


--
-- Name: companies; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.companies (
    id integer NOT NULL,
    name character varying(100)
);


ALTER TABLE temp_schema.companies OWNER TO meditreats;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.companies_id_seq OWNER TO meditreats;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.companies_id_seq OWNED BY temp_schema.companies.id;


--
-- Name: comparison; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.comparison (
    id integer NOT NULL,
    analytic integer,
    administration integer,
    "group" integer
);


ALTER TABLE temp_schema.comparison OWNER TO meditreats;

--
-- Name: comparison_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.comparison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.comparison_id_seq OWNER TO meditreats;

--
-- Name: comparison_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.comparison_id_seq OWNED BY temp_schema.comparison.id;


--
-- Name: condition_groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.condition_groups (
    id integer NOT NULL,
    name character varying(400)
);


ALTER TABLE temp_schema.condition_groups OWNER TO meditreats;

--
-- Name: condition_groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.condition_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.condition_groups_id_seq OWNER TO meditreats;

--
-- Name: condition_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.condition_groups_id_seq OWNED BY temp_schema.condition_groups.id;


--
-- Name: conditions; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.conditions (
    id integer NOT NULL,
    name character varying(150),
    condition_group integer
);


ALTER TABLE temp_schema.conditions OWNER TO meditreats;

--
-- Name: conditions_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.conditions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.conditions_id_seq OWNER TO meditreats;

--
-- Name: conditions_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.conditions_id_seq OWNED BY temp_schema.conditions.id;


--
-- Name: conditionscores; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.conditionscores (
    id integer NOT NULL,
    treatment integer,
    condition integer,
    mixed_score double precision,
    singular_score double precision
);


ALTER TABLE temp_schema.conditionscores OWNER TO meditreats;

--
-- Name: conditionscores_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.conditionscores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.conditionscores_id_seq OWNER TO meditreats;

--
-- Name: conditionscores_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.conditionscores_id_seq OWNED BY temp_schema.conditionscores.id;


--
-- Name: criteria; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.criteria (
    id integer NOT NULL,
    study character varying(11),
    criteria character varying(500),
    is_inclusion boolean
);


ALTER TABLE temp_schema.criteria OWNER TO meditreats;

--
-- Name: criteria_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.criteria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.criteria_id_seq OWNER TO meditreats;

--
-- Name: criteria_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.criteria_id_seq OWNED BY temp_schema.criteria.id;


--
-- Name: diff_treatments_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.diff_treatments_diffs (
    id integer NOT NULL,
    treatment_diff integer,
    treatment integer
);


ALTER TABLE temp_schema.diff_treatments_diffs OWNER TO meditreats;

--
-- Name: diff_treatments_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.diff_treatments_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.diff_treatments_diffs_id_seq OWNER TO meditreats;

--
-- Name: diff_treatments_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.diff_treatments_diffs_id_seq OWNED BY temp_schema.diff_treatments_diffs.id;


--
-- Name: effects; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effects (
    id integer NOT NULL,
    study character varying(11),
    "group" integer,
    name character varying(100),
    organ_system temp_schema.organ_system,
    assessment temp_schema.effect_collection_method,
    no_effected double precision,
    collection_threshold double precision,
    effect_type temp_schema.effect_type,
    no_at_risk integer,
    cluster integer,
    cluster_name character varying(100)
);


ALTER TABLE temp_schema.effects OWNER TO meditreats;

--
-- Name: effects_cluster; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effects_cluster (
    id integer NOT NULL,
    name character varying(100)
);


ALTER TABLE temp_schema.effects_cluster OWNER TO meditreats;

--
-- Name: effects_cluster_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effects_cluster_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effects_cluster_id_seq OWNER TO meditreats;

--
-- Name: effects_cluster_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effects_cluster_id_seq OWNED BY temp_schema.effects_cluster.id;


--
-- Name: effects_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effects_id_seq OWNER TO meditreats;

--
-- Name: effects_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effects_id_seq OWNED BY temp_schema.effects.id;


--
-- Name: effectsadministrations; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effectsadministrations (
    id integer NOT NULL,
    "group" integer,
    treatment integer
);


ALTER TABLE temp_schema.effectsadministrations OWNER TO meditreats;

--
-- Name: effectsadministrations_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effectsadministrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effectsadministrations_id_seq OWNER TO meditreats;

--
-- Name: effectsadministrations_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effectsadministrations_id_seq OWNED BY temp_schema.effectsadministrations.id;


--
-- Name: effectsgroups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effectsgroups (
    id integer NOT NULL,
    title character varying(101),
    description character varying(1500),
    study_id character varying(7),
    study character varying(11)
);


ALTER TABLE temp_schema.effectsgroups OWNER TO meditreats;

--
-- Name: effectsgroups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effectsgroups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effectsgroups_id_seq OWNER TO meditreats;

--
-- Name: effectsgroups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effectsgroups_id_seq OWNED BY temp_schema.effectsgroups.id;


--
-- Name: group_pair_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.group_pair_diffs (
    id integer NOT NULL,
    group_pair integer,
    treatment_diff integer
);


ALTER TABLE temp_schema.group_pair_diffs OWNER TO meditreats;

--
-- Name: group_pair_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.group_pair_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.group_pair_diffs_id_seq OWNER TO meditreats;

--
-- Name: group_pair_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.group_pair_diffs_id_seq OWNED BY temp_schema.group_pair_diffs.id;


--
-- Name: group_pairs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.group_pairs (
    id integer NOT NULL,
    group_a integer,
    group_b integer
);


ALTER TABLE temp_schema.group_pairs OWNER TO meditreats;

--
-- Name: group_pairs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.group_pairs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.group_pairs_id_seq OWNER TO meditreats;

--
-- Name: group_pairs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.group_pairs_id_seq OWNED BY temp_schema.group_pairs.id;


--
-- Name: groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.groups (
    id integer NOT NULL,
    title character varying(100),
    study_id character varying(7),
    description character varying(1500),
    study character varying(11),
    annotated boolean
);


ALTER TABLE temp_schema.groups OWNER TO meditreats;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.groups_id_seq OWNER TO meditreats;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.groups_id_seq OWNED BY temp_schema.groups.id;


--
-- Name: insights; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.insights (
    id integer NOT NULL,
    study character varying(11),
    measure integer,
    type temp_schema.insight_type,
    body character varying(1000)
);


ALTER TABLE temp_schema.insights OWNER TO meditreats;

--
-- Name: insights_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.insights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.insights_id_seq OWNER TO meditreats;

--
-- Name: insights_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.insights_id_seq OWNED BY temp_schema.insights.id;


--
-- Name: measure_group_measures; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.measure_group_measures (
    id integer NOT NULL,
    measure integer,
    "measureGroup" integer
);


ALTER TABLE temp_schema.measure_group_measures OWNER TO meditreats;

--
-- Name: measure_group_measures_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.measure_group_measures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.measure_group_measures_id_seq OWNER TO meditreats;

--
-- Name: measure_group_measures_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.measure_group_measures_id_seq OWNED BY temp_schema.measure_group_measures.id;


--
-- Name: measure_groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.measure_groups (
    id integer NOT NULL,
    name character varying(256),
    condition integer,
    type temp_schema.measure_group_type
);


ALTER TABLE temp_schema.measure_groups OWNER TO meditreats;

--
-- Name: measure_groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.measure_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.measure_groups_id_seq OWNER TO meditreats;

--
-- Name: measure_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.measure_groups_id_seq OWNED BY temp_schema.measure_groups.id;


--
-- Name: measures; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.measures (
    id integer NOT NULL,
    study character varying(11),
    title character varying(256),
    description character varying(1005),
    dispersion temp_schema.dispersion_param,
    type temp_schema.measure_type,
    param temp_schema.measure_param,
    units character varying(40)
);


ALTER TABLE temp_schema.measures OWNER TO meditreats;

--
-- Name: measures_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.measures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.measures_id_seq OWNER TO meditreats;

--
-- Name: measures_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.measures_id_seq OWNED BY temp_schema.measures.id;


--
-- Name: outcomes; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.outcomes (
    id integer NOT NULL,
    study character varying(11),
    measure integer,
    title character varying(225),
    value double precision,
    dispersion double precision,
    upper double precision,
    lower double precision,
    no_participants integer,
    "group" integer
);


ALTER TABLE temp_schema.outcomes OWNER TO meditreats;

--
-- Name: outcomes_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.outcomes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.outcomes_id_seq OWNER TO meditreats;

--
-- Name: outcomes_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.outcomes_id_seq OWNED BY temp_schema.outcomes.id;


--
-- Name: studies; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.studies (
    id character varying(11) NOT NULL,
    upload_date date,
    short_title character varying(300),
    official_title character varying(600),
    description character varying(5000),
    responsible_party character varying(160),
    sponsor character varying(160),
    type temp_schema.study_type,
    purpose temp_schema.purpose,
    intervention_type temp_schema.intervention_type,
    min_age integer,
    min_age_units temp_schema.age_units,
    max_age integer,
    max_age_units temp_schema.age_units,
    gender temp_schema.gender,
    results_summary integer,
    nct_id character varying(11),
    phase temp_schema.phase_type
);


ALTER TABLE temp_schema.studies OWNER TO meditreats;

--
-- Name: study_conditions; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.study_conditions (
    id integer NOT NULL,
    study character varying(11),
    condition integer
);


ALTER TABLE temp_schema.study_conditions OWNER TO meditreats;

--
-- Name: study_conditions_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.study_conditions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.study_conditions_id_seq OWNER TO meditreats;

--
-- Name: study_conditions_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.study_conditions_id_seq OWNED BY temp_schema.study_conditions.id;


--
-- Name: study_treatments; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.study_treatments (
    id integer NOT NULL,
    study character varying(11),
    treatment integer
);


ALTER TABLE temp_schema.study_treatments OWNER TO meditreats;

--
-- Name: study_treatments_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.study_treatments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.study_treatments_id_seq OWNER TO meditreats;

--
-- Name: study_treatments_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.study_treatments_id_seq OWNED BY temp_schema.study_treatments.id;


--
-- Name: treatment_brand_names; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatment_brand_names (
    id integer NOT NULL,
    treatment integer,
    brand_name character varying(400)
);


ALTER TABLE temp_schema.treatment_brand_names OWNER TO meditreats;

--
-- Name: treatment_brand_names_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatment_brand_names_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatment_brand_names_id_seq OWNER TO meditreats;

--
-- Name: treatment_brand_names_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatment_brand_names_id_seq OWNED BY temp_schema.treatment_brand_names.id;


--
-- Name: treatment_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatment_diffs (
    id integer NOT NULL,
    condition integer
);


ALTER TABLE temp_schema.treatment_diffs OWNER TO meditreats;

--
-- Name: treatment_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatment_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatment_diffs_id_seq OWNER TO meditreats;

--
-- Name: treatment_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatment_diffs_id_seq OWNED BY temp_schema.treatment_diffs.id;


--
-- Name: treatment_groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatment_groups (
    id integer NOT NULL,
    name character varying(400)
);


ALTER TABLE temp_schema.treatment_groups OWNER TO meditreats;

--
-- Name: treatment_groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatment_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatment_groups_id_seq OWNER TO meditreats;

--
-- Name: treatment_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatment_groups_id_seq OWNED BY temp_schema.treatment_groups.id;


--
-- Name: treatments; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatments (
    id integer NOT NULL,
    name character varying(400),
    from_study boolean,
    no_studies integer,
    "treatmentGroup" integer,
    description character varying(5000),
    no_prescriptions integer
);


ALTER TABLE temp_schema.treatments OWNER TO meditreats;

--
-- Name: treatments_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatments_id_seq OWNER TO meditreats;

--
-- Name: treatments_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatments_id_seq OWNED BY temp_schema.treatments.id;


--
-- Name: administrations; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.administrations (
    id integer NOT NULL,
    "group" integer,
    treatment integer,
    description character varying(1500),
    annotated boolean
);


ALTER TABLE temp_schema.administrations OWNER TO meditreats;

--
-- Name: administrations_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.administrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.administrations_id_seq OWNER TO meditreats;

--
-- Name: administrations_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.administrations_id_seq OWNED BY temp_schema.administrations.id;


--
-- Name: alembic_version; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE temp_schema.alembic_version OWNER TO meditreats;

--
-- Name: analytics; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.analytics (
    id integer NOT NULL,
    study character varying(11),
    measure integer,
    from_study boolean,
    method character varying(100),
    p_value double precision,
    param_type character varying(100),
    is_non_inferiority boolean,
    non_inferiority_type temp_schema.non_inferiority_type,
    non_inferiority_comment character varying(500),
    param_value double precision,
    ci_pct integer,
    ci_lower double precision,
    ci_upper double precision
);


ALTER TABLE temp_schema.analytics OWNER TO meditreats;

--
-- Name: analytics_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.analytics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.analytics_id_seq OWNER TO meditreats;

--
-- Name: analytics_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.analytics_id_seq OWNED BY temp_schema.analytics.id;


--
-- Name: base_treatments_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.base_treatments_diffs (
    id integer NOT NULL,
    treatment_diff integer,
    treatment integer
);


ALTER TABLE temp_schema.base_treatments_diffs OWNER TO meditreats;

--
-- Name: base_treatments_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.base_treatments_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.base_treatments_diffs_id_seq OWNER TO meditreats;

--
-- Name: base_treatments_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.base_treatments_diffs_id_seq OWNED BY temp_schema.base_treatments_diffs.id;


--
-- Name: baselines; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.baselines (
    id integer NOT NULL,
    base character varying(100),
    clss character varying(100),
    category character varying(100),
    param_type temp_schema.measure_param,
    dispersion temp_schema.dispersion_param,
    unit character varying(40),
    value double precision,
    spread double precision,
    upper double precision,
    lower double precision,
    type temp_schema.baseline_type,
    sub_type temp_schema.baseline_subtype,
    study character varying(11)
);


ALTER TABLE temp_schema.baselines OWNER TO meditreats;

--
-- Name: baselines_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.baselines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.baselines_id_seq OWNER TO meditreats;

--
-- Name: baselines_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.baselines_id_seq OWNED BY temp_schema.baselines.id;


--
-- Name: companies; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.companies (
    id integer NOT NULL,
    name character varying(100)
);


ALTER TABLE temp_schema.companies OWNER TO meditreats;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.companies_id_seq OWNER TO meditreats;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.companies_id_seq OWNED BY temp_schema.companies.id;


--
-- Name: comparison; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.comparison (
    id integer NOT NULL,
    analytic integer,
    administration integer
);


ALTER TABLE temp_schema.comparison OWNER TO meditreats;

--
-- Name: comparison_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.comparison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.comparison_id_seq OWNER TO meditreats;

--
-- Name: comparison_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.comparison_id_seq OWNED BY temp_schema.comparison.id;


--
-- Name: condition_groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.condition_groups (
    id integer NOT NULL,
    name character varying(400)
);


ALTER TABLE temp_schema.condition_groups OWNER TO meditreats;

--
-- Name: condition_groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.condition_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.condition_groups_id_seq OWNER TO meditreats;

--
-- Name: condition_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.condition_groups_id_seq OWNED BY temp_schema.condition_groups.id;


--
-- Name: conditions; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.conditions (
    id integer NOT NULL,
    name character varying(150),
    condition_group integer
);


ALTER TABLE temp_schema.conditions OWNER TO meditreats;

--
-- Name: conditions_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.conditions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.conditions_id_seq OWNER TO meditreats;

--
-- Name: conditions_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.conditions_id_seq OWNED BY temp_schema.conditions.id;


--
-- Name: conditionscores; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.conditionscores (
    id integer NOT NULL,
    treatment integer,
    condition integer,
    mixed_score double precision,
    singular_score double precision
);


ALTER TABLE temp_schema.conditionscores OWNER TO meditreats;

--
-- Name: conditionscores_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.conditionscores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.conditionscores_id_seq OWNER TO meditreats;

--
-- Name: conditionscores_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.conditionscores_id_seq OWNED BY temp_schema.conditionscores.id;


--
-- Name: criteria; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.criteria (
    id integer NOT NULL,
    study character varying(11),
    criteria character varying(500),
    is_inclusion boolean
);


ALTER TABLE temp_schema.criteria OWNER TO meditreats;

--
-- Name: criteria_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.criteria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.criteria_id_seq OWNER TO meditreats;

--
-- Name: criteria_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.criteria_id_seq OWNED BY temp_schema.criteria.id;


--
-- Name: diff_treatments_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.diff_treatments_diffs (
    id integer NOT NULL,
    treatment_diff integer,
    treatment integer
);


ALTER TABLE temp_schema.diff_treatments_diffs OWNER TO meditreats;

--
-- Name: diff_treatments_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.diff_treatments_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.diff_treatments_diffs_id_seq OWNER TO meditreats;

--
-- Name: diff_treatments_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.diff_treatments_diffs_id_seq OWNED BY temp_schema.diff_treatments_diffs.id;


--
-- Name: effects; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effects (
    id integer NOT NULL,
    study character varying(11),
    "group" integer,
    name character varying(100),
    organ_system temp_schema.organ_system,
    assessment temp_schema.effect_collection_method,
    no_effected double precision,
    collection_threshold double precision,
    effect_type temp_schema.effect_type,
    no_at_risk integer,
    cluster integer,
    cluster_name character varying(100)
);


ALTER TABLE temp_schema.effects OWNER TO meditreats;

--
-- Name: effects_cluster; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effects_cluster (
    id integer NOT NULL,
    name character varying(100)
);


ALTER TABLE temp_schema.effects_cluster OWNER TO meditreats;

--
-- Name: effects_cluster_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effects_cluster_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effects_cluster_id_seq OWNER TO meditreats;

--
-- Name: effects_cluster_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effects_cluster_id_seq OWNED BY temp_schema.effects_cluster.id;


--
-- Name: effects_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effects_id_seq OWNER TO meditreats;

--
-- Name: effects_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effects_id_seq OWNED BY temp_schema.effects.id;


--
-- Name: effectsadministrations; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effectsadministrations (
    id integer NOT NULL,
    "group" integer,
    treatment integer
);


ALTER TABLE temp_schema.effectsadministrations OWNER TO meditreats;

--
-- Name: effectsadministrations_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effectsadministrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effectsadministrations_id_seq OWNER TO meditreats;

--
-- Name: effectsadministrations_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effectsadministrations_id_seq OWNED BY temp_schema.effectsadministrations.id;


--
-- Name: effectsgroups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.effectsgroups (
    id integer NOT NULL,
    title character varying(101),
    description character varying(1500),
    study_id character varying(7),
    study character varying(11)
);


ALTER TABLE temp_schema.effectsgroups OWNER TO meditreats;

--
-- Name: effectsgroups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.effectsgroups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.effectsgroups_id_seq OWNER TO meditreats;

--
-- Name: effectsgroups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.effectsgroups_id_seq OWNED BY temp_schema.effectsgroups.id;


--
-- Name: group_pair_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.group_pair_diffs (
    id integer NOT NULL,
    group_pair integer,
    treatment_diff integer
);


ALTER TABLE temp_schema.group_pair_diffs OWNER TO meditreats;

--
-- Name: group_pair_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.group_pair_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.group_pair_diffs_id_seq OWNER TO meditreats;

--
-- Name: group_pair_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.group_pair_diffs_id_seq OWNED BY temp_schema.group_pair_diffs.id;


--
-- Name: group_pairs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.group_pairs (
    id integer NOT NULL,
    group_a integer,
    group_b integer
);


ALTER TABLE temp_schema.group_pairs OWNER TO meditreats;

--
-- Name: group_pairs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.group_pairs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.group_pairs_id_seq OWNER TO meditreats;

--
-- Name: group_pairs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.group_pairs_id_seq OWNED BY temp_schema.group_pairs.id;


--
-- Name: groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.groups (
    id integer NOT NULL,
    title character varying(100),
    study_id character varying(7),
    description character varying(1500),
    study character varying(11),
    annotated boolean
);


ALTER TABLE temp_schema.groups OWNER TO meditreats;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.groups_id_seq OWNER TO meditreats;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.groups_id_seq OWNED BY temp_schema.groups.id;


--
-- Name: insights; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.insights (
    id integer NOT NULL,
    study character varying(11),
    measure integer,
    type temp_schema.insight_type,
    body character varying(1000)
);


ALTER TABLE temp_schema.insights OWNER TO meditreats;

--
-- Name: insights_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.insights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.insights_id_seq OWNER TO meditreats;

--
-- Name: insights_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.insights_id_seq OWNED BY temp_schema.insights.id;


--
-- Name: measure_group_measures; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.measure_group_measures (
    id integer NOT NULL,
    measure integer,
    "measureGroup" integer
);


ALTER TABLE temp_schema.measure_group_measures OWNER TO meditreats;

--
-- Name: measure_group_measures_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.measure_group_measures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.measure_group_measures_id_seq OWNER TO meditreats;

--
-- Name: measure_group_measures_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.measure_group_measures_id_seq OWNED BY temp_schema.measure_group_measures.id;


--
-- Name: measure_groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.measure_groups (
    id integer NOT NULL,
    name character varying(256),
    condition integer,
    type temp_schema.measure_group_type
);


ALTER TABLE temp_schema.measure_groups OWNER TO meditreats;

--
-- Name: measure_groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.measure_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.measure_groups_id_seq OWNER TO meditreats;

--
-- Name: measure_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.measure_groups_id_seq OWNED BY temp_schema.measure_groups.id;


--
-- Name: measures; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.measures (
    id integer NOT NULL,
    study character varying(11),
    title character varying(256),
    description character varying(1005),
    dispersion temp_schema.dispersion_param,
    type temp_schema.measure_type,
    param temp_schema.measure_param,
    units character varying(40)
);


ALTER TABLE temp_schema.measures OWNER TO meditreats;

--
-- Name: measures_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.measures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.measures_id_seq OWNER TO meditreats;

--
-- Name: measures_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.measures_id_seq OWNED BY temp_schema.measures.id;


--
-- Name: outcomes; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.outcomes (
    id integer NOT NULL,
    study character varying(11),
    measure integer,
    title character varying(225),
    value double precision,
    dispersion double precision,
    upper double precision,
    lower double precision,
    no_participants integer,
    "group" integer
);


ALTER TABLE temp_schema.outcomes OWNER TO meditreats;

--
-- Name: outcomes_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.outcomes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.outcomes_id_seq OWNER TO meditreats;

--
-- Name: outcomes_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.outcomes_id_seq OWNED BY temp_schema.outcomes.id;


--
-- Name: studies; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.studies (
    id character varying(11) NOT NULL,
    upload_date date,
    short_title character varying(300),
    official_title character varying(600),
    description character varying(5000),
    responsible_party character varying(160),
    sponsor character varying(160),
    type temp_schema.study_type,
    purpose temp_schema.purpose,
    intervention_type temp_schema.intervention_type,
    min_age integer,
    min_age_units temp_schema.age_units,
    max_age integer,
    max_age_units temp_schema.age_units,
    gender temp_schema.gender,
    results_summary integer,
    nct_id character varying(11)
);


ALTER TABLE temp_schema.studies OWNER TO meditreats;

--
-- Name: study_conditions; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.study_conditions (
    id integer NOT NULL,
    study character varying(11),
    condition integer
);


ALTER TABLE temp_schema.study_conditions OWNER TO meditreats;

--
-- Name: study_conditions_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.study_conditions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.study_conditions_id_seq OWNER TO meditreats;

--
-- Name: study_conditions_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.study_conditions_id_seq OWNED BY temp_schema.study_conditions.id;


--
-- Name: study_treatments; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.study_treatments (
    id integer NOT NULL,
    study character varying(11),
    treatment integer
);


ALTER TABLE temp_schema.study_treatments OWNER TO meditreats;

--
-- Name: study_treatments_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.study_treatments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.study_treatments_id_seq OWNER TO meditreats;

--
-- Name: study_treatments_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.study_treatments_id_seq OWNED BY temp_schema.study_treatments.id;


--
-- Name: treatment_brand_names; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatment_brand_names (
    id integer NOT NULL,
    treatment integer,
    brand_name character varying(400)
);


ALTER TABLE temp_schema.treatment_brand_names OWNER TO meditreats;

--
-- Name: treatment_brand_names_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatment_brand_names_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatment_brand_names_id_seq OWNER TO meditreats;

--
-- Name: treatment_brand_names_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatment_brand_names_id_seq OWNED BY temp_schema.treatment_brand_names.id;


--
-- Name: treatment_diffs; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatment_diffs (
    id integer NOT NULL,
    condition integer
);


ALTER TABLE temp_schema.treatment_diffs OWNER TO meditreats;

--
-- Name: treatment_diffs_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatment_diffs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatment_diffs_id_seq OWNER TO meditreats;

--
-- Name: treatment_diffs_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatment_diffs_id_seq OWNED BY temp_schema.treatment_diffs.id;


--
-- Name: treatment_groups; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatment_groups (
    id integer NOT NULL,
    name character varying(400)
);


ALTER TABLE temp_schema.treatment_groups OWNER TO meditreats;

--
-- Name: treatment_groups_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatment_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatment_groups_id_seq OWNER TO meditreats;

--
-- Name: treatment_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatment_groups_id_seq OWNED BY temp_schema.treatment_groups.id;


--
-- Name: treatments; Type: TABLE; Schema: temp_schema; Owner: meditreats
--

CREATE TABLE temp_schema.treatments (
    id integer NOT NULL,
    name character varying(400),
    from_study boolean,
    no_studies integer,
    "treatmentGroup" integer,
    description character varying(5000),
    no_prescriptions integer
);


ALTER TABLE temp_schema.treatments OWNER TO meditreats;

--
-- Name: treatments_id_seq; Type: SEQUENCE; Schema: temp_schema; Owner: meditreats
--

CREATE SEQUENCE temp_schema.treatments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_schema.treatments_id_seq OWNER TO meditreats;

--
-- Name: treatments_id_seq; Type: SEQUENCE OWNED BY; Schema: temp_schema; Owner: meditreats
--

ALTER SEQUENCE temp_schema.treatments_id_seq OWNED BY temp_schema.treatments.id;


--
-- Name: administrations id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations ALTER COLUMN id SET DEFAULT nextval('temp_schema.administrations_id_seq'::regclass);


--
-- Name: analytics id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics ALTER COLUMN id SET DEFAULT nextval('temp_schema.analytics_id_seq'::regclass);


--
-- Name: base_treatments_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.base_treatments_diffs_id_seq'::regclass);


--
-- Name: baselines id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.baselines ALTER COLUMN id SET DEFAULT nextval('temp_schema.baselines_id_seq'::regclass);


--
-- Name: companies id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.companies ALTER COLUMN id SET DEFAULT nextval('temp_schema.companies_id_seq'::regclass);


--
-- Name: comparison id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison ALTER COLUMN id SET DEFAULT nextval('temp_schema.comparison_id_seq'::regclass);


--
-- Name: condition_groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.condition_groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.condition_groups_id_seq'::regclass);


--
-- Name: conditions id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditions ALTER COLUMN id SET DEFAULT nextval('temp_schema.conditions_id_seq'::regclass);


--
-- Name: conditionscores id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores ALTER COLUMN id SET DEFAULT nextval('temp_schema.conditionscores_id_seq'::regclass);


--
-- Name: criteria id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.criteria ALTER COLUMN id SET DEFAULT nextval('temp_schema.criteria_id_seq'::regclass);


--
-- Name: diff_treatments_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.diff_treatments_diffs_id_seq'::regclass);


--
-- Name: effects id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects ALTER COLUMN id SET DEFAULT nextval('temp_schema.effects_id_seq'::regclass);


--
-- Name: effects_cluster id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects_cluster ALTER COLUMN id SET DEFAULT nextval('temp_schema.effects_cluster_id_seq'::regclass);


--
-- Name: effectsadministrations id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations ALTER COLUMN id SET DEFAULT nextval('temp_schema.effectsadministrations_id_seq'::regclass);


--
-- Name: effectsgroups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsgroups ALTER COLUMN id SET DEFAULT nextval('temp_schema.effectsgroups_id_seq'::regclass);


--
-- Name: group_pair_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.group_pair_diffs_id_seq'::regclass);


--
-- Name: group_pairs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs ALTER COLUMN id SET DEFAULT nextval('temp_schema.group_pairs_id_seq'::regclass);


--
-- Name: groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.groups_id_seq'::regclass);


--
-- Name: insights id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights ALTER COLUMN id SET DEFAULT nextval('temp_schema.insights_id_seq'::regclass);


--
-- Name: measure_group_measures id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures ALTER COLUMN id SET DEFAULT nextval('temp_schema.measure_group_measures_id_seq'::regclass);


--
-- Name: measure_groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.measure_groups_id_seq'::regclass);


--
-- Name: measures id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measures ALTER COLUMN id SET DEFAULT nextval('temp_schema.measures_id_seq'::regclass);


--
-- Name: outcomes id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes ALTER COLUMN id SET DEFAULT nextval('temp_schema.outcomes_id_seq'::regclass);


--
-- Name: study_conditions id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions ALTER COLUMN id SET DEFAULT nextval('temp_schema.study_conditions_id_seq'::regclass);


--
-- Name: study_treatments id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments ALTER COLUMN id SET DEFAULT nextval('temp_schema.study_treatments_id_seq'::regclass);


--
-- Name: treatment_brand_names id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_brand_names ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatment_brand_names_id_seq'::regclass);


--
-- Name: treatment_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatment_diffs_id_seq'::regclass);


--
-- Name: treatment_groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatment_groups_id_seq'::regclass);


--
-- Name: treatments id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatments_id_seq'::regclass);


--
-- Name: administrations id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations ALTER COLUMN id SET DEFAULT nextval('temp_schema.administrations_id_seq'::regclass);


--
-- Name: analytics id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics ALTER COLUMN id SET DEFAULT nextval('temp_schema.analytics_id_seq'::regclass);


--
-- Name: base_treatments_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.base_treatments_diffs_id_seq'::regclass);


--
-- Name: baselines id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.baselines ALTER COLUMN id SET DEFAULT nextval('temp_schema.baselines_id_seq'::regclass);


--
-- Name: companies id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.companies ALTER COLUMN id SET DEFAULT nextval('temp_schema.companies_id_seq'::regclass);


--
-- Name: comparison id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison ALTER COLUMN id SET DEFAULT nextval('temp_schema.comparison_id_seq'::regclass);


--
-- Name: condition_groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.condition_groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.condition_groups_id_seq'::regclass);


--
-- Name: conditions id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditions ALTER COLUMN id SET DEFAULT nextval('temp_schema.conditions_id_seq'::regclass);


--
-- Name: conditionscores id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores ALTER COLUMN id SET DEFAULT nextval('temp_schema.conditionscores_id_seq'::regclass);


--
-- Name: criteria id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.criteria ALTER COLUMN id SET DEFAULT nextval('temp_schema.criteria_id_seq'::regclass);


--
-- Name: diff_treatments_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.diff_treatments_diffs_id_seq'::regclass);


--
-- Name: effects id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects ALTER COLUMN id SET DEFAULT nextval('temp_schema.effects_id_seq'::regclass);


--
-- Name: effects_cluster id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects_cluster ALTER COLUMN id SET DEFAULT nextval('temp_schema.effects_cluster_id_seq'::regclass);


--
-- Name: effectsadministrations id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations ALTER COLUMN id SET DEFAULT nextval('temp_schema.effectsadministrations_id_seq'::regclass);


--
-- Name: effectsgroups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsgroups ALTER COLUMN id SET DEFAULT nextval('temp_schema.effectsgroups_id_seq'::regclass);


--
-- Name: group_pair_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.group_pair_diffs_id_seq'::regclass);


--
-- Name: group_pairs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs ALTER COLUMN id SET DEFAULT nextval('temp_schema.group_pairs_id_seq'::regclass);


--
-- Name: groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.groups_id_seq'::regclass);


--
-- Name: insights id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights ALTER COLUMN id SET DEFAULT nextval('temp_schema.insights_id_seq'::regclass);


--
-- Name: measure_group_measures id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures ALTER COLUMN id SET DEFAULT nextval('temp_schema.measure_group_measures_id_seq'::regclass);


--
-- Name: measure_groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.measure_groups_id_seq'::regclass);


--
-- Name: measures id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measures ALTER COLUMN id SET DEFAULT nextval('temp_schema.measures_id_seq'::regclass);


--
-- Name: outcomes id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes ALTER COLUMN id SET DEFAULT nextval('temp_schema.outcomes_id_seq'::regclass);


--
-- Name: study_conditions id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions ALTER COLUMN id SET DEFAULT nextval('temp_schema.study_conditions_id_seq'::regclass);


--
-- Name: study_treatments id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments ALTER COLUMN id SET DEFAULT nextval('temp_schema.study_treatments_id_seq'::regclass);


--
-- Name: treatment_brand_names id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_brand_names ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatment_brand_names_id_seq'::regclass);


--
-- Name: treatment_diffs id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_diffs ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatment_diffs_id_seq'::regclass);


--
-- Name: treatment_groups id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_groups ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatment_groups_id_seq'::regclass);


--
-- Name: treatments id; Type: DEFAULT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments ALTER COLUMN id SET DEFAULT nextval('temp_schema.treatments_id_seq'::regclass);


--
-- Name: administrations administrations_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations
    ADD CONSTRAINT administrations_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: analytics analytics_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics
    ADD CONSTRAINT analytics_pkey PRIMARY KEY (id);


--
-- Name: base_treatments_diffs base_treatments_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs
    ADD CONSTRAINT base_treatments_diffs_pkey PRIMARY KEY (id);


--
-- Name: baselines baselines_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.baselines
    ADD CONSTRAINT baselines_pkey PRIMARY KEY (id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: comparison comparison_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison
    ADD CONSTRAINT comparison_pkey PRIMARY KEY (id);


--
-- Name: condition_groups condition_groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.condition_groups
    ADD CONSTRAINT condition_groups_pkey PRIMARY KEY (id);


--
-- Name: conditions conditions_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditions
    ADD CONSTRAINT conditions_pkey PRIMARY KEY (id);


--
-- Name: conditionscores conditionscores_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT conditionscores_pkey PRIMARY KEY (id);


--
-- Name: criteria criteria_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.criteria
    ADD CONSTRAINT criteria_pkey PRIMARY KEY (id);


--
-- Name: diff_treatments_diffs diff_treatments_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs
    ADD CONSTRAINT diff_treatments_diffs_pkey PRIMARY KEY (id);


--
-- Name: effects_cluster effects_cluster_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects_cluster
    ADD CONSTRAINT effects_cluster_pkey PRIMARY KEY (id);


--
-- Name: effects effects_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_pkey PRIMARY KEY (id);


--
-- Name: effectsadministrations effectsadministrations_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations
    ADD CONSTRAINT effectsadministrations_pkey PRIMARY KEY (id);


--
-- Name: effectsgroups effectsgroups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsgroups
    ADD CONSTRAINT effectsgroups_pkey PRIMARY KEY (id);


--
-- Name: group_pair_diffs group_pair_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs
    ADD CONSTRAINT group_pair_diffs_pkey PRIMARY KEY (id);


--
-- Name: group_pairs group_pairs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs
    ADD CONSTRAINT group_pairs_pkey PRIMARY KEY (id);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: insights insights_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights
    ADD CONSTRAINT insights_pkey PRIMARY KEY (id);


--
-- Name: measure_group_measures measure_group_measures_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures
    ADD CONSTRAINT measure_group_measures_pkey PRIMARY KEY (id);


--
-- Name: measure_groups measure_groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_groups
    ADD CONSTRAINT measure_groups_pkey PRIMARY KEY (id);


--
-- Name: measures measures_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measures
    ADD CONSTRAINT measures_pkey PRIMARY KEY (id);


--
-- Name: outcomes outcomes_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_pkey PRIMARY KEY (id);


--
-- Name: studies studies_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.studies
    ADD CONSTRAINT studies_pkey PRIMARY KEY (id);


--
-- Name: study_conditions study_conditions_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions
    ADD CONSTRAINT study_conditions_pkey PRIMARY KEY (id);


--
-- Name: study_treatments study_treatments_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_pkey PRIMARY KEY (id);


--
-- Name: treatment_brand_names treatment_brand_names_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_brand_names
    ADD CONSTRAINT treatment_brand_names_pkey PRIMARY KEY (id);


--
-- Name: treatment_diffs treatment_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_diffs
    ADD CONSTRAINT treatment_diffs_pkey PRIMARY KEY (id);


--
-- Name: treatment_groups treatment_groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_groups
    ADD CONSTRAINT treatment_groups_pkey PRIMARY KEY (id);


--
-- Name: treatments treatments_name_key; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments
    ADD CONSTRAINT treatments_name_key UNIQUE (name);


--
-- Name: treatments treatments_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments
    ADD CONSTRAINT treatments_pkey PRIMARY KEY (id);


--
-- Name: conditionscores uq_treatment_condition; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT uq_treatment_condition UNIQUE (treatment, condition);


--
-- Name: administrations administrations_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations
    ADD CONSTRAINT administrations_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: analytics analytics_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics
    ADD CONSTRAINT analytics_pkey PRIMARY KEY (id);


--
-- Name: base_treatments_diffs base_treatments_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs
    ADD CONSTRAINT base_treatments_diffs_pkey PRIMARY KEY (id);


--
-- Name: baselines baselines_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.baselines
    ADD CONSTRAINT baselines_pkey PRIMARY KEY (id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: comparison comparison_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison
    ADD CONSTRAINT comparison_pkey PRIMARY KEY (id);


--
-- Name: condition_groups condition_groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.condition_groups
    ADD CONSTRAINT condition_groups_pkey PRIMARY KEY (id);


--
-- Name: conditions conditions_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditions
    ADD CONSTRAINT conditions_pkey PRIMARY KEY (id);


--
-- Name: conditionscores conditionscores_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT conditionscores_pkey PRIMARY KEY (id);


--
-- Name: criteria criteria_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.criteria
    ADD CONSTRAINT criteria_pkey PRIMARY KEY (id);


--
-- Name: diff_treatments_diffs diff_treatments_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs
    ADD CONSTRAINT diff_treatments_diffs_pkey PRIMARY KEY (id);


--
-- Name: effects_cluster effects_cluster_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects_cluster
    ADD CONSTRAINT effects_cluster_pkey PRIMARY KEY (id);


--
-- Name: effects effects_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_pkey PRIMARY KEY (id);


--
-- Name: effectsadministrations effectsadministrations_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations
    ADD CONSTRAINT effectsadministrations_pkey PRIMARY KEY (id);


--
-- Name: effectsgroups effectsgroups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsgroups
    ADD CONSTRAINT effectsgroups_pkey PRIMARY KEY (id);


--
-- Name: group_pair_diffs group_pair_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs
    ADD CONSTRAINT group_pair_diffs_pkey PRIMARY KEY (id);


--
-- Name: group_pairs group_pairs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs
    ADD CONSTRAINT group_pairs_pkey PRIMARY KEY (id);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: insights insights_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights
    ADD CONSTRAINT insights_pkey PRIMARY KEY (id);


--
-- Name: measure_group_measures measure_group_measures_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures
    ADD CONSTRAINT measure_group_measures_pkey PRIMARY KEY (id);


--
-- Name: measure_groups measure_groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_groups
    ADD CONSTRAINT measure_groups_pkey PRIMARY KEY (id);


--
-- Name: measures measures_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measures
    ADD CONSTRAINT measures_pkey PRIMARY KEY (id);


--
-- Name: outcomes outcomes_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_pkey PRIMARY KEY (id);


--
-- Name: studies studies_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.studies
    ADD CONSTRAINT studies_pkey PRIMARY KEY (id);


--
-- Name: study_conditions study_conditions_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions
    ADD CONSTRAINT study_conditions_pkey PRIMARY KEY (id);


--
-- Name: study_treatments study_treatments_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_pkey PRIMARY KEY (id);


--
-- Name: treatment_brand_names treatment_brand_names_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_brand_names
    ADD CONSTRAINT treatment_brand_names_pkey PRIMARY KEY (id);


--
-- Name: treatment_diffs treatment_diffs_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_diffs
    ADD CONSTRAINT treatment_diffs_pkey PRIMARY KEY (id);


--
-- Name: treatment_groups treatment_groups_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_groups
    ADD CONSTRAINT treatment_groups_pkey PRIMARY KEY (id);


--
-- Name: treatments treatments_name_key; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments
    ADD CONSTRAINT treatments_name_key UNIQUE (name);


--
-- Name: treatments treatments_pkey; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments
    ADD CONSTRAINT treatments_pkey PRIMARY KEY (id);


--
-- Name: conditionscores uq_treatment_condition; Type: CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT uq_treatment_condition UNIQUE (treatment, condition);


--
-- Name: base_treatments_diffs_treatment_diffs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX base_treatments_diffs_treatment_diffs ON temp_schema.base_treatments_diffs USING btree (treatment_diff);


--
-- Name: base_treatments_diffs_treatments; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX base_treatments_diffs_treatments ON temp_schema.base_treatments_diffs USING btree (treatment);


--
-- Name: diff_treatments_diffs_treatment_diffs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX diff_treatments_diffs_treatment_diffs ON temp_schema.diff_treatments_diffs USING btree (treatment_diff);


--
-- Name: diff_treatments_diffs_treatments; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX diff_treatments_diffs_treatments ON temp_schema.diff_treatments_diffs USING btree (treatment);


--
-- Name: effects_group_ind; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX effects_group_ind ON temp_schema.effects USING btree ("group");


--
-- Name: effects_study_ind; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX effects_study_ind ON temp_schema.effects USING btree (study);


--
-- Name: effectsgroups_study_ind; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX effectsgroups_study_ind ON temp_schema.effectsgroups USING btree (study);


--
-- Name: group_pair_diffs_group_pairs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pair_diffs_group_pairs ON temp_schema.group_pair_diffs USING btree (group_pair);


--
-- Name: group_pair_diffs_treatment_diffs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pair_diffs_treatment_diffs ON temp_schema.group_pair_diffs USING btree (treatment_diff);


--
-- Name: group_pairs_a_groups; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pairs_a_groups ON temp_schema.group_pairs USING btree (group_a);


--
-- Name: group_pairs_b_groups; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pairs_b_groups ON temp_schema.group_pairs USING btree (group_b);


--
-- Name: ix_conditions_name; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE UNIQUE INDEX ix_conditions_name ON temp_schema.conditions USING btree (name);


--
-- Name: base_treatments_diffs_treatment_diffs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX base_treatments_diffs_treatment_diffs ON temp_schema.base_treatments_diffs USING btree (treatment_diff);


--
-- Name: base_treatments_diffs_treatments; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX base_treatments_diffs_treatments ON temp_schema.base_treatments_diffs USING btree (treatment);


--
-- Name: diff_treatments_diffs_treatment_diffs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX diff_treatments_diffs_treatment_diffs ON temp_schema.diff_treatments_diffs USING btree (treatment_diff);


--
-- Name: diff_treatments_diffs_treatments; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX diff_treatments_diffs_treatments ON temp_schema.diff_treatments_diffs USING btree (treatment);


--
-- Name: effects_group_ind; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX effects_group_ind ON temp_schema.effects USING btree ("group");


--
-- Name: effects_study_ind; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX effects_study_ind ON temp_schema.effects USING btree (study);


--
-- Name: effectsgroups_study_ind; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX effectsgroups_study_ind ON temp_schema.effectsgroups USING btree (study);


--
-- Name: group_pair_diffs_group_pairs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pair_diffs_group_pairs ON temp_schema.group_pair_diffs USING btree (group_pair);


--
-- Name: group_pair_diffs_treatment_diffs; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pair_diffs_treatment_diffs ON temp_schema.group_pair_diffs USING btree (treatment_diff);


--
-- Name: group_pairs_a_groups; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pairs_a_groups ON temp_schema.group_pairs USING btree (group_a);


--
-- Name: group_pairs_b_groups; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE INDEX group_pairs_b_groups ON temp_schema.group_pairs USING btree (group_b);


--
-- Name: ix_conditions_name; Type: INDEX; Schema: temp_schema; Owner: meditreats
--

CREATE UNIQUE INDEX ix_conditions_name ON temp_schema.conditions USING btree (name);


--
-- Name: administrations administrations_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations
    ADD CONSTRAINT administrations_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.groups(id);


--
-- Name: administrations administrations_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations
    ADD CONSTRAINT administrations_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: analytics analytics_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics
    ADD CONSTRAINT analytics_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: analytics analytics_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics
    ADD CONSTRAINT analytics_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: base_treatments_diffs base_treatments_diffs_treatment_diff_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs
    ADD CONSTRAINT base_treatments_diffs_treatment_diff_fkey FOREIGN KEY (treatment_diff) REFERENCES temp_schema.treatment_diffs(id);


--
-- Name: base_treatments_diffs base_treatments_diffs_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs
    ADD CONSTRAINT base_treatments_diffs_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: baselines baselines_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.baselines
    ADD CONSTRAINT baselines_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: comparison comparison_administration_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison
    ADD CONSTRAINT comparison_administration_fkey FOREIGN KEY (administration) REFERENCES temp_schema.administrations(id);


--
-- Name: comparison comparison_analytic_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison
    ADD CONSTRAINT comparison_analytic_fkey FOREIGN KEY (analytic) REFERENCES temp_schema.analytics(id);


--
-- Name: comparison comparison_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison
    ADD CONSTRAINT comparison_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.groups(id);


--
-- Name: conditions conditions_condition_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditions
    ADD CONSTRAINT conditions_condition_group_fkey FOREIGN KEY (condition_group) REFERENCES temp_schema.condition_groups(id);


--
-- Name: conditionscores conditionscores_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT conditionscores_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: conditionscores conditionscores_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT conditionscores_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: criteria criteria_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.criteria
    ADD CONSTRAINT criteria_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: diff_treatments_diffs diff_treatments_diffs_treatment_diff_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs
    ADD CONSTRAINT diff_treatments_diffs_treatment_diff_fkey FOREIGN KEY (treatment_diff) REFERENCES temp_schema.treatment_diffs(id);


--
-- Name: diff_treatments_diffs diff_treatments_diffs_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs
    ADD CONSTRAINT diff_treatments_diffs_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: effects effects_cluster_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_cluster_fkey FOREIGN KEY (cluster) REFERENCES temp_schema.effects_cluster(id);


--
-- Name: effects effects_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.groups(id);


--
-- Name: effects effects_group_fkey1; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_group_fkey1 FOREIGN KEY ("group") REFERENCES temp_schema.effectsgroups(id);


--
-- Name: effects effects_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: effectsadministrations effectsadministrations_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations
    ADD CONSTRAINT effectsadministrations_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.effectsgroups(id);


--
-- Name: effectsadministrations effectsadministrations_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations
    ADD CONSTRAINT effectsadministrations_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: effectsgroups effectsgroups_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsgroups
    ADD CONSTRAINT effectsgroups_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: group_pair_diffs group_pair_diffs_group_pair_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs
    ADD CONSTRAINT group_pair_diffs_group_pair_fkey FOREIGN KEY (group_pair) REFERENCES temp_schema.group_pairs(id);


--
-- Name: group_pair_diffs group_pair_diffs_treatment_diff_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs
    ADD CONSTRAINT group_pair_diffs_treatment_diff_fkey FOREIGN KEY (treatment_diff) REFERENCES temp_schema.treatment_diffs(id);


--
-- Name: group_pairs group_pairs_group_a_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs
    ADD CONSTRAINT group_pairs_group_a_fkey FOREIGN KEY (group_a) REFERENCES temp_schema.groups(id);


--
-- Name: group_pairs group_pairs_group_b_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs
    ADD CONSTRAINT group_pairs_group_b_fkey FOREIGN KEY (group_b) REFERENCES temp_schema.groups(id);


--
-- Name: groups groups_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.groups
    ADD CONSTRAINT groups_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: insights insights_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights
    ADD CONSTRAINT insights_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: insights insights_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights
    ADD CONSTRAINT insights_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: measure_group_measures measure_group_measures_measureGroup_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures
    ADD CONSTRAINT "measure_group_measures_measureGroup_fkey" FOREIGN KEY ("measureGroup") REFERENCES temp_schema.measure_groups(id);


--
-- Name: measure_group_measures measure_group_measures_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures
    ADD CONSTRAINT measure_group_measures_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: measure_groups measure_groups_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_groups
    ADD CONSTRAINT measure_groups_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: measures measures_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measures
    ADD CONSTRAINT measures_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: outcomes outcomes_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.groups(id);


--
-- Name: outcomes outcomes_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: outcomes outcomes_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_conditions study_conditions_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions
    ADD CONSTRAINT study_conditions_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: study_conditions study_conditions_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions
    ADD CONSTRAINT study_conditions_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_treatments study_treatments_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_treatments study_treatments_study_fkey1; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_study_fkey1 FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_treatments study_treatments_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: study_treatments study_treatments_treatment_fkey1; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_treatment_fkey1 FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: treatment_brand_names treatment_brand_names_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_brand_names
    ADD CONSTRAINT treatment_brand_names_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: treatment_diffs treatment_diffs_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_diffs
    ADD CONSTRAINT treatment_diffs_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: treatments treatments_treatmentGroup_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments
    ADD CONSTRAINT "treatments_treatmentGroup_fkey" FOREIGN KEY ("treatmentGroup") REFERENCES temp_schema.treatment_groups(id);


--
-- Name: administrations administrations_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations
    ADD CONSTRAINT administrations_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.groups(id);


--
-- Name: administrations administrations_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.administrations
    ADD CONSTRAINT administrations_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: analytics analytics_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics
    ADD CONSTRAINT analytics_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: analytics analytics_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.analytics
    ADD CONSTRAINT analytics_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: base_treatments_diffs base_treatments_diffs_treatment_diff_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs
    ADD CONSTRAINT base_treatments_diffs_treatment_diff_fkey FOREIGN KEY (treatment_diff) REFERENCES temp_schema.treatment_diffs(id);


--
-- Name: base_treatments_diffs base_treatments_diffs_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.base_treatments_diffs
    ADD CONSTRAINT base_treatments_diffs_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: baselines baselines_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.baselines
    ADD CONSTRAINT baselines_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: comparison comparison_administration_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison
    ADD CONSTRAINT comparison_administration_fkey FOREIGN KEY (administration) REFERENCES temp_schema.administrations(id);


--
-- Name: comparison comparison_analytic_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.comparison
    ADD CONSTRAINT comparison_analytic_fkey FOREIGN KEY (analytic) REFERENCES temp_schema.analytics(id);


--
-- Name: conditions conditions_condition_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditions
    ADD CONSTRAINT conditions_condition_group_fkey FOREIGN KEY (condition_group) REFERENCES temp_schema.condition_groups(id);


--
-- Name: conditionscores conditionscores_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT conditionscores_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: conditionscores conditionscores_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.conditionscores
    ADD CONSTRAINT conditionscores_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: criteria criteria_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.criteria
    ADD CONSTRAINT criteria_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: diff_treatments_diffs diff_treatments_diffs_treatment_diff_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs
    ADD CONSTRAINT diff_treatments_diffs_treatment_diff_fkey FOREIGN KEY (treatment_diff) REFERENCES temp_schema.treatment_diffs(id);


--
-- Name: diff_treatments_diffs diff_treatments_diffs_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.diff_treatments_diffs
    ADD CONSTRAINT diff_treatments_diffs_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: effects effects_cluster_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_cluster_fkey FOREIGN KEY (cluster) REFERENCES temp_schema.effects_cluster(id);


--
-- Name: effects effects_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.groups(id);


--
-- Name: effects effects_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effects
    ADD CONSTRAINT effects_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: effectsadministrations effectsadministrations_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations
    ADD CONSTRAINT effectsadministrations_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.effectsgroups(id);


--
-- Name: effectsadministrations effectsadministrations_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsadministrations
    ADD CONSTRAINT effectsadministrations_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: effectsgroups effectsgroups_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.effectsgroups
    ADD CONSTRAINT effectsgroups_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: group_pair_diffs group_pair_diffs_group_pair_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs
    ADD CONSTRAINT group_pair_diffs_group_pair_fkey FOREIGN KEY (group_pair) REFERENCES temp_schema.group_pairs(id);


--
-- Name: group_pair_diffs group_pair_diffs_treatment_diff_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pair_diffs
    ADD CONSTRAINT group_pair_diffs_treatment_diff_fkey FOREIGN KEY (treatment_diff) REFERENCES temp_schema.treatment_diffs(id);


--
-- Name: group_pairs group_pairs_group_a_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs
    ADD CONSTRAINT group_pairs_group_a_fkey FOREIGN KEY (group_a) REFERENCES temp_schema.groups(id);


--
-- Name: group_pairs group_pairs_group_b_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.group_pairs
    ADD CONSTRAINT group_pairs_group_b_fkey FOREIGN KEY (group_b) REFERENCES temp_schema.groups(id);


--
-- Name: groups groups_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.groups
    ADD CONSTRAINT groups_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: insights insights_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights
    ADD CONSTRAINT insights_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: insights insights_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.insights
    ADD CONSTRAINT insights_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: measure_group_measures measure_group_measures_measureGroup_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures
    ADD CONSTRAINT "measure_group_measures_measureGroup_fkey" FOREIGN KEY ("measureGroup") REFERENCES temp_schema.measure_groups(id);


--
-- Name: measure_group_measures measure_group_measures_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_group_measures
    ADD CONSTRAINT measure_group_measures_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: measure_groups measure_groups_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measure_groups
    ADD CONSTRAINT measure_groups_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: measures measures_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.measures
    ADD CONSTRAINT measures_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: outcomes outcomes_group_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_group_fkey FOREIGN KEY ("group") REFERENCES temp_schema.groups(id);


--
-- Name: outcomes outcomes_measure_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_measure_fkey FOREIGN KEY (measure) REFERENCES temp_schema.measures(id);


--
-- Name: outcomes outcomes_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.outcomes
    ADD CONSTRAINT outcomes_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_conditions study_conditions_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions
    ADD CONSTRAINT study_conditions_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: study_conditions study_conditions_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_conditions
    ADD CONSTRAINT study_conditions_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_treatments study_treatments_study_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_study_fkey FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_treatments study_treatments_study_fkey1; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_study_fkey1 FOREIGN KEY (study) REFERENCES temp_schema.studies(id);


--
-- Name: study_treatments study_treatments_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: study_treatments study_treatments_treatment_fkey1; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.study_treatments
    ADD CONSTRAINT study_treatments_treatment_fkey1 FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: treatment_brand_names treatment_brand_names_treatment_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_brand_names
    ADD CONSTRAINT treatment_brand_names_treatment_fkey FOREIGN KEY (treatment) REFERENCES temp_schema.treatments(id);


--
-- Name: treatment_diffs treatment_diffs_condition_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatment_diffs
    ADD CONSTRAINT treatment_diffs_condition_fkey FOREIGN KEY (condition) REFERENCES temp_schema.conditions(id);


--
-- Name: treatments treatments_treatmentGroup_fkey; Type: FK CONSTRAINT; Schema: temp_schema; Owner: meditreats
--

ALTER TABLE ONLY temp_schema.treatments
    ADD CONSTRAINT "treatments_treatmentGroup_fkey" FOREIGN KEY ("treatmentGroup") REFERENCES temp_schema.treatment_groups(id);


--
-- PostgreSQL database dump complete
--

