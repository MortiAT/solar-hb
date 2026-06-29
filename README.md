Start with:
'''bash
docker compose up
'''

Install 'postgresql-client' tool to access db from host, then connect with:
'''bash
psql -d "postgres://postgres:password@127.0.0.1:5432/postgres"

\dx
'''

