CREATE TYPE "study_type" AS ENUM (
  'Interventional',
  'Observational',
  'Patient Registry',
  'Expanded Access'
);

CREATE TYPE "purpose" AS ENUM (
  'Treatment',
  'Prevention',
  'Basic Science',
  'Other',
  'Supportive Care',
  'Diagnostic',
  'Health Services Research',
  'Screening',
  'Device Feasibility',
  'NA'
);

CREATE TYPE "gender" AS ENUM (
  'ALL',
  'Female',
  'Male',
  'NA'
);

CREATE TYPE "intervention_type" AS ENUM (
  'Parallel Assignment',
  'Single Group Assignment',
  'Crossover Assignment',
  'Factorial Assignment',
  'Sequential Assignment',
  'NA'
);

CREATE TYPE "measure_type" AS ENUM (
  'Primary',
  'Secondary',
  'Other'
);

CREATE TYPE "group_type" AS ENUM (
  'Experimental',
  'Active Comparator',
  'Placebo Comparator',
  'Sham Comparator',
  'No Intervention',
  'Other'
);

CREATE TYPE "non_inferiority_type" AS ENUM (
  'Superiority or Other',
  'Superiority',
  'Other',
  'Superiority or Other (legacy)',
  'Non-Inferiority or Equivalence',
  'Non-Inferiority',
  'Non-Inferiority or Equivalence (legacy)'
);

CREATE TABLE "studies" (
  "nct_id" varchar PRIMARY KEY,
  "upload_date" date,
  "name" varchar,
  "description" varchar,
  "responsible_party" varchar,
  "type" study_type,
  "purpose" purpose,
  "intervention_type" intervention_type,
  "min_age" int,
  "max_age" int,
  "gender" gender
);

CREATE TABLE "criteria" (
  "id" SERIAL PRIMARY KEY,
  "nct_id" varchar,
  "criteria" varchar,
  "is_inclusion" boolean
);

CREATE TABLE "study_conditions" (
  "id" SERIAL PRIMARY KEY,
  "nct_id" varchar,
  "condition" int
);

CREATE TABLE "conditions" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "measures" (
  "id" SERIAL PRIMARY KEY,
  "nct_id" varchar,
  "title" varchar,
  "description" varchar,
  "type" measure_type
);

CREATE TABLE "companies" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "treatments" (
  "id" SERIAL PRIMARY KEY,
  "company" int,
  "name" varchar
);

CREATE TABLE "administrations" (
  "id" SERIAL PRIMARY KEY,
  "group" int,
  "treatment" int,
  "description" varchar
);

CREATE TABLE "groups" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar,
  "description" varchar,
  "type" group_type,
  "participants" int
);

CREATE TABLE "analytics" (
  "id" SERIAL PRIMARY KEY,
  "nct_id" varchar,
  "measure" int,
  "from_study" bool,
  "method" varchar,
  "p_value" int,
  "param_type" varchar,
  "is_non_inferiority" bool,
  "non_inferiority_type" non_inferiority_type,
  "non_inferiority_comment" varchar,
  "param_value" float8,
  "ci_pct" int,
  "ci_lower" float8,
  "ci_upper" float8
);

CREATE TABLE "comparisons" (
  "id" SERIAL PRIMARY KEY,
  "analytic" int,
  "group" int
);

ALTER TABLE "criteria" ADD FOREIGN KEY ("nct_id") REFERENCES "studies" ("nct_id");

ALTER TABLE "study_conditions" ADD FOREIGN KEY ("condition") REFERENCES "conditions" ("id");

ALTER TABLE "study_conditions" ADD FOREIGN KEY ("nct_id") REFERENCES "studies" ("nct_id");

ALTER TABLE "measures" ADD FOREIGN KEY ("nct_id") REFERENCES "studies" ("nct_id");

ALTER TABLE "treatments" ADD FOREIGN KEY ("company") REFERENCES "companies" ("id");

ALTER TABLE "administrations" ADD FOREIGN KEY ("treatment") REFERENCES "treatments" ("id");

ALTER TABLE "administrations" ADD FOREIGN KEY ("group") REFERENCES "groups" ("id");

ALTER TABLE "analytics" ADD FOREIGN KEY ("measure") REFERENCES "measures" ("id");

ALTER TABLE "comparisons" ADD FOREIGN KEY ("analytic") REFERENCES "analytics" ("id");

ALTER TABLE "comparisons" ADD FOREIGN KEY ("group") REFERENCES "groups" ("id");
