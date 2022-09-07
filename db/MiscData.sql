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


