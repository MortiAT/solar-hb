Start with:
```bash
docker compose up --build
```
(--build is good when developing)

Install `postgresql-client` tool to access db from host, then connect with:
```bash
psql -d "postgres://postgres:password@timescale:5432/postgres"
docker exec -it a7  psql -U postgres -d postgres -h timescale
\dx
```

```sql
select * from sensor_data;
```

```
http://192.168.1.151:3000/rpc/get_sensor_data_for_day?day_str=2026-07-10
```

