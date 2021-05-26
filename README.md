# treats
the treatment exploration arm of mediboard

## API Docs

### Treatments

```
GET /treats/summary?<query>
```
The summary endpoint get's a set of treatments and some summary information about those treatments such as the number of studies, power score, side-effect severity, number of people studied etc.

This also includes something like patient criteria in the query as well.

```
GET /treats/analytics?<query>
```
The analytics endpoint gets all the analytics associated with the query.

```
GET /treats/effects?<query>
```
The effects endpoint gets all the effects documented from the treatment

```
GET /treats/demographics?<query>
```
The demographics endpoint gets the demographic distribution of the participants given the treatment.


