# treats
the treatment exploration arm of mediboard

## Deployment

- Build a new image from repo root
```
docker build -t meditreats:latest .
```

- Tag image for remote registry
```
docker tag meditreats:latest public.ecr.aws/t6z3u3k0/docker-treats:latest
```

- Push image
```
docker push public.ecr.aws/t6z3u3k0/docker-treats:latest
```

Now that the image is pushed and tagged as latest, we just need to restart the compute tasks in ECS and it will restart with the lastest image.

- Go to: ECS => default cluster => Service:df-treats-service-4 => tasks
- Select one task and stop it
- Wait for another one to automatically spin up
- Repeat for the second task


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


