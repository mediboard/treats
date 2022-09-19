select title, t.name, g.description, g.id, t.id from analytics
    join comparison c on analytics.id = c.analytic
    join groups g on g.id = c."group"
    join administrations a on g.id = a."group"
    join treatments t on t.id = a.treatment
    where analytics.study='NCT02552303'; --modafinil

update administrations set treatment = 2182 where "group" = 55009;
update administrations set treatment = 156 where "group" = 55008;
update administrations set treatment = 156 where "group" = 55006;
update administrations set treatment = 2182 where "group" = 55007;

select title, t.name, g.description, g.id, t.id from analytics
join comparison c on analytics.id = c.analytic
join groups g on g.id = c."group"
join administrations a on g.id = a."group"
join treatments t on t.id = a.treatment
where analytics.study='NCT01011218'; -- Modafinil

update administrations set treatment = 2182 where "group" =97607;


select title, t.name, g.description, g.id, t.id from analytics
    join comparison c on analytics.id = c.analytic
    join groups g on g.id = c."group"
    join administrations a on g.id = a."group"
    join treatments t on t.id = a.treatment
    where analytics.study='NCT00482612';

select * from treatments where name = 'Mirtazapine';

update administrations set treatment = 546 where treatment = 6188;


select title, t.name, g.description, g.id, t.id from analytics
    join comparison c on analytics.id = c.analytic
    join groups g on g.id = c."group"
    join administrations a on g.id = a."group"
    join treatments t on t.id = a.treatment
    where analytics.study='NCT00869128';

update administrations set treatment =349 where "group"=41572


select title, t.name, g.description, g.id, t.id from analytics
    join comparison c on analytics.id = c.analytic
    join groups g on g.id = c."group"
    join administrations a on g.id = a."group"
    join treatments t on t.id = a.treatment
    where analytics.study='NCT01348542';

select * from treatments where name ='Trazodone'

update administrations set treatment = 870 where treatment=8243

Select title, measures.id from measures join study_conditions sc on measures.study = sc.study where sc.condition=817;

Insert into measure_groups(name, condition) values ('Total Time Asleep', 817);
Insert into measure_groups(name, condition) values ('Time to Fall Asleep', 817);
Insert into measure_groups(name, condition) values ('Overall Severity', 817);
-- Maybe these two can be combined into quality
-- Insert into measure_groups(name, condition) values ('Waking Up After Falling Asleep', 817);
Insert into measure_groups(name, condition) values ('Quality of Sleep', 817);
Insert into measure_groups(name, condition) values ('Daytime Fatigue', 817);


-- TST
INSERT into measure_group_measures(measure, "measureGroup") values (6382, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (10450, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (30224, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (30227, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (30229, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (30230, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (33195, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (35273, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (35321, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (35322, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (35325, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (44344, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (44351, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (83816, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (85773, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (85780, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (85801, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (124650, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (124654, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (141821, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148819, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148820, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148821, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148853, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148854, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148855, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148856, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148857, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148858, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148859, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (148860, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (149055, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (149056, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (149057, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (165369, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (165370, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (203020, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (210407, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (210408, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (210409, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (210410, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (217759, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (222152, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (224904, 1);
INSERT into measure_group_measures(measure, "measureGroup") values (225002, 1);

-- Sleep Latency
INSERT into measure_group_measures(measure, "measureGroup") values (6381, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (10451, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (30219, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (30224, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (30225, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (30227, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (30230, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (35267, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (35317, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (35323, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (44343, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (44352, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (85772, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (85781, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (85802, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (124648, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (124656, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (148822, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (148823, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (148824, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (148861, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (148862, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (148863, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (149053, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (149063, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (160093, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (180746, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (203017, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (210408, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (210410, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (217760, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (222153, 2);
INSERT into measure_group_measures(measure, "measureGroup") values (224906, 2);

-- Quality of Sleep
Select title, measures.id from measures
    join study_conditions sc on measures.study = sc.study
    left outer join measure_group_measures mgm on measures.id = mgm.measure
    where sc.condition=817 and mgm.id is null;


INSERT into measure_group_measures(measure, "measureGroup") values (6380, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (10452, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (10454, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (15016, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (20309, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (30220, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (30221, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (30222, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (30226, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (30228, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (30231, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (33197, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (33199, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (33202, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (35271, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (35272, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (35313, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (35318, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (35320, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (35324, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (35329, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44342, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44345, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44346, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44347, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44348, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44349, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44353, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44354, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44355, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (44356, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (66084, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (66081, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (83817, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85774, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85775, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85776, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85782, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85784, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85803, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85804, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (85805, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (124646, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (124649, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (124651, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (124652, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (124653, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (124655, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (129896, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (141822, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (141823, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (142253, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148825, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148826, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148827, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148828, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148829, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148830, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148831, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148832, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148834, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148835, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148836, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148864, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148865, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148866, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148867, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148868, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (148869, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (149065, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (149066, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (149059, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (149062, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (149064, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (149067, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (153974, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (160094, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (203019, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (203021, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (215991, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (222154, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (222155, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (222156, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (224907, 5);
INSERT into measure_group_measures(measure, "measureGroup") values (225003, 5);

-- Overall Severity
Select title, measures.id from measures
    join study_conditions sc on measures.study = sc.study
    left outer join measure_group_measures mgm on measures.id = mgm.measure
    where sc.condition=817 and mgm.id is null;

INSERT into measure_group_measures(measure, "measureGroup") values (12831, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (30233, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (32655, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (57659, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (111634, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (124657, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (129897, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (142252, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (148879, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (148880, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (148881, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (165368, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (180281, 3);
INSERT into measure_group_measures(measure, "measureGroup") values (225265, 3);
