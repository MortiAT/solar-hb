Start with:
```bash
docker compose up --build
```
(--build is good when developing)

Install `postgresql-client` tool to access db from host, then connect with:
```bash
psql -d "postgres://postgres:password@127.0.0.1:5432/postgres"
docker exec -it a7  psql -U postgres -d postgres -h timescale
\dx
```

```sql
select * from sensor_data;
```

