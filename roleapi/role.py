from flask import Blueprint, request
from roleapi import extensions

bp = Blueprint('role', __name__, url_prefix='/role')

@bp.route('/<role_name>', methods=['GET'])
@bp.route('/')
def role(role_name=None):
    if role_name is None:
        return list_all_roles_with_grants()
    all_roles = list_roles()
    for role in all_roles:
        if role[0] == role_name:
            return {
                'role': role_name,
                'grants': list_grants_for_role(role_name)
            }
    return 'Role not found'

@bp.route('/', methods=['POST'])
def create_role():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        request_json = request.json
        role_name = request_json.get('role_name')
        if role_name is not None:
            create_role_in_trino(role_name)
            requested_privileges = request_json.get('privileges')
            for privilege in requested_privileges:
                grant_table_privilege_to_role(role_name, privilege['type'], privilege['table'])
            return {
                'role': role_name,
                'grants': list_grants_for_role(role_name)
            }
        return 'No role name provided'
    else:
        return 'Content-Type not supported'


@bp.route('/<role_name>', methods=['PATCH'])
def update_role_privileges(role_name):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        if role_name is not None:
            request_json = request.json
            requested_privileges = request_json.get('privileges')
            for privilege in requested_privileges:
                grant_table_privilege_to_role(role_name, privilege['type'], privilege['table'])
            return {
                'role': role_name,
                'grants': list_grants_for_role(role_name)
            }
        else:
            return 'No role name provided'
    else:
        return 'Content-Type not supported'


@bp.route('/<role_name>', methods=['DELETE'])
def drop_role(role_name):
    if role_name is not None:
        drop_role_in_trino(role_name)
        return '{} dropped'.format(role_name)
    else:
        return 'No role name provided'


def create_role_in_trino(role_name):
    sql = 'CREATE ROLE {}'.format(role_name)
    execute_sql(extensions.trino.get_db(), sql)


def drop_role_in_trino(role_name):
    sql = 'DROP ROLE {}'.format(role_name)
    execute_sql(extensions.trino.get_db(), sql)


def list_all_roles_with_grants():
    all_roles = list_roles()
    all_roles_with_grants = []
    for role in all_roles:
        all_roles_with_grants.append({
            'role': role[0],
            'grants': list_grants_for_role(role[0])
        })
    return all_roles_with_grants
    

def list_roles():
    sql = 'SHOW ROLES'
    return execute_sql(extensions.trino.get_db(), sql)


def list_all_grants():
    return create_cursor(extensions.trino.get_db(), 'SHOW GRANTS')


def list_grants_for_role(role_name, grants_cursor=None):
    if grants_cursor is None:
        grants_cursor = list_all_grants()
    field_map = fields(grants_cursor)
    role_grants = []
    for grant in grants_cursor:
        if grant[field_map['Grantee']] == role_name and grant[field_map['Grantee Type']] == 'ROLE':
            role_grants.append({
                'catalog': grant[field_map['Catalog']],
                'schema': grant[field_map['Schema']],
                'table': grant[field_map['Table']],
                'privilege': grant[field_map['Privilege']]
            })
    return role_grants


def assign_select_table_privilege_to_role(conn, role, tables):
    for table in tables:
        assign_table_privilege_to_role(
            conn,
            role,
            'SELECT',
            table
        )


def grant_table_privilege_to_role(role, privilege, table):
    sql = 'GRANT {} ON {} TO ROLE {}'.format(
        privilege,
        table,
        role
    )
    execute_sql(extensions.trino.get_db(), sql)


def execute_sql(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def create_cursor(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor

def fields(cursor):
    """ Given a DB API 2.0 cursor object that has been executed, returns
    a dictionary that maps each field name to a column index; 0 and up. """
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1

    return results
    