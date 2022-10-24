# records
PERMISSION_RECORDS_ADD_RECORD = "records__add_record"
PERMISSION_RECORDS_ACCESS_ALL_RECORDS = "records__access_all_records"
# files
PERMISSION_FILES_READ_ALL_FOLDERS = "files__read_all_folders"
PERMISSION_FILES_WRITE_ALL_FOLDERS = "files__write_all_folders"
PERMISSION_FILES_MANAGE_PERMISSIONS = "files__manage_permissions"
# collab
PERMISSION_COLLAB_READ_ALL_DOCUMENTS = "collab__read_all_documents"
PERMISSION_COLLAB_WRITE_ALL_DOCUMENTS = "collab__write_all_documents"
PERMISSION_COLLAB_MANAGE_PERMISSIONS = "collab__manage_permissions"
# admin
PERMISSION_ADMIN_MANAGE_GROUPS = "admin__manage_groups"
PERMISSION_ADMIN_MANAGE_USERS = "admin__manage_users"
PERMISSION_ADMIN_MANAGE_PERMISSIONS = "admin__manage_permissions"
PERMISSION_ADMIN_MANAGE_RECORD_TEMPLATES = "admin__manage_record_templates"
PERMISSION_ADMIN_MANAGE_RECORD_QUESTIONNAIRES = "admin__manage_record_questionnaires"
PERMISSION_ADMIN_MANAGE_RECORD_DELETION_REQUESTS = (
    "admin__manage_record_deletion_requests"
)
PERMISSION_ADMIN_MANAGE_RECORD_ACCESS_REQUESTS = "admin__manage_record_access_requests"
# dashboard
PERMISSION_DASHBOARD_MANAGE_NOTES = "dashboard__manage_notes"


def get_all_permission_strings():
    return [
        # records
        PERMISSION_RECORDS_ADD_RECORD,
        PERMISSION_RECORDS_ACCESS_ALL_RECORDS,
        # files
        PERMISSION_FILES_READ_ALL_FOLDERS,
        PERMISSION_FILES_WRITE_ALL_FOLDERS,
        PERMISSION_FILES_MANAGE_PERMISSIONS,
        # collab
        PERMISSION_COLLAB_MANAGE_PERMISSIONS,
        PERMISSION_COLLAB_READ_ALL_DOCUMENTS,
        PERMISSION_COLLAB_WRITE_ALL_DOCUMENTS,
        # admin
        PERMISSION_ADMIN_MANAGE_GROUPS,
        PERMISSION_ADMIN_MANAGE_USERS,
        PERMISSION_ADMIN_MANAGE_PERMISSIONS,
        PERMISSION_ADMIN_MANAGE_RECORD_TEMPLATES,
        PERMISSION_ADMIN_MANAGE_RECORD_QUESTIONNAIRES,
        PERMISSION_ADMIN_MANAGE_RECORD_DELETION_REQUESTS,
        PERMISSION_ADMIN_MANAGE_RECORD_ACCESS_REQUESTS,
        PERMISSION_DASHBOARD_MANAGE_NOTES,
    ]


def get_all_collab_permissions():
    return [
        PERMISSION_COLLAB_MANAGE_PERMISSIONS,
        PERMISSION_COLLAB_WRITE_ALL_DOCUMENTS,
        PERMISSION_COLLAB_READ_ALL_DOCUMENTS,
    ]


def get_all_records_permissions():
    return [
        PERMISSION_RECORDS_ACCESS_ALL_RECORDS,
        PERMISSION_RECORDS_ADD_RECORD,
    ]


def get_all_files_permissions():
    return [
        PERMISSION_FILES_READ_ALL_FOLDERS,
        PERMISSION_FILES_WRITE_ALL_FOLDERS,
        PERMISSION_FILES_MANAGE_PERMISSIONS,
    ]


def get_all_admin_permissions():
    return [
        PERMISSION_ADMIN_MANAGE_GROUPS,
        PERMISSION_ADMIN_MANAGE_USERS,
        PERMISSION_ADMIN_MANAGE_PERMISSIONS,
        PERMISSION_ADMIN_MANAGE_RECORD_TEMPLATES,
        PERMISSION_ADMIN_MANAGE_RECORD_QUESTIONNAIRES,
        PERMISSION_ADMIN_MANAGE_RECORD_DELETION_REQUESTS,
        PERMISSION_ADMIN_MANAGE_RECORD_ACCESS_REQUESTS,
    ]


PERMISSION_READ_DOCUMENT = "read_document"
PERMISSION_WRITE_DOCUMENT = "write_document"


def get_all_collab_permission_strings():
    return [PERMISSION_READ_DOCUMENT, PERMISSION_WRITE_DOCUMENT]


PERMISSION_READ_FOLDER = "read_folder"
PERMISSION_WRITE_FOLDER = "write_folder"


def get_all_files_permission_strings():
    return [PERMISSION_READ_FOLDER, PERMISSION_WRITE_FOLDER]