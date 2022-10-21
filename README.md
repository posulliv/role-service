# start in virtual environment

```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -e .
```

Next, configure the environment variables for the Trino cluster you wish to connect to:

```
$ export TRINO_PORT=443
$ export TRINO_HOST="hostname"
$ export TRINO_USER="username"
$ export TRINO_PASSWORD="password"
$ export TRINO_CATALOG="catalogname"
$ export TRINO_SCHEMA="schemaname"
```

Now we can start `flask`:

```
$ flask --app roleapi --debug run
```

Server now running on `http://localhost:5000`

# create role 

```
$ curl -X POST http://localhost:5000/role/ \
-H 'Content-Type: application/json' \
-d '{"role_name": "role_api_test_3", "privileges": [{"type":"UPDATE", "table":"datalake.manyrolestest.zwrul_3"}, {"type":"SELECT", "table":"datalake.manyrolestest.zwrul_3"}]}'
{
  "grants": [
    {
      "catalog": "datalake",
      "privilege": "SELECT",
      "schema": "manyrolestest",
      "table": "zwrul_3"
    },
    {
      "catalog": "datalake",
      "privilege": "UPDATE",
      "schema": "manyrolestest",
      "table": "zwrul_3"
    }
  ],
  "role": "role_api_test_3"
}
$
```

# get details for single role

```
$ curl http://localhost:5000/role/role_api_test_3
{
  "grants": [
    {
      "catalog": "datalake",
      "privilege": "SELECT",
      "schema": "manyrolestest",
      "table": "zwrul_3"
    },
    {
      "catalog": "datalake",
      "privilege": "UPDATE",
      "schema": "manyrolestest",
      "table": "zwrul_3"
    }
  ],
  "role": "role_api_test_3"
}
$
```

# get details for all roles

```
$ curl http://localhost:5000/role/
[
  {
    "grants": [
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zoefv_0"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zoefv_1"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zoefv_2"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zoefv_3"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zoefv_4"
      }
    ],
    "role": "zoefv_34_role"
  },
  {
    "grants": [
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zwrul_0"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zwrul_1"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zwrul_2"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zwrul_3"
      },
      {
        "catalog": "datalake",
        "privilege": "SELECT",
        "schema": "manyrolestest",
        "table": "zwrul_4"
      }
    ],
    "role": "zwrul_9_role"
  }
]

$
```

# update privileges for role

```
$ curl -X PATCH http://localhost:5000/role/role_api_test_3 \
-H 'Content-Type: application/json' \
-d '{"privileges": [{"type":"DELETE", "table":"datalake.manyrolestest.zwrul_3"}]}'

{
  "grants": [
    {
      "catalog": "datalake",
      "privilege": "DELETE",
      "schema": "manyrolestest",
      "table": "zwrul_3"
    },
    {
      "catalog": "datalake",
      "privilege": "SELECT",
      "schema": "manyrolestest",
      "table": "zwrul_3"
    },
    {
      "catalog": "datalake",
      "privilege": "UPDATE",
      "schema": "manyrolestest",
      "table": "zwrul_3"
    }
  ],
  "role": "role_api_test_3"
}
$
```

# drop role

```
$ curl -X DELETE http://localhost:5000/role/zoefv_34_role
zoefv_34_role dropped%
$
```