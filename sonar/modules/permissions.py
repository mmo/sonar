# -*- coding: utf-8 -*-
#
# Swiss Open Access Repository
# Copyright (C) 2019 RERO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Project permissions management."""

from flask_principal import ActionNeed
from invenio_access import Permission
from invenio_records_rest.utils import check_elasticsearch

superuser_access_permission = Permission(ActionNeed('superuser-access'))
admin_access_permission = Permission(ActionNeed('admin-access'))


def has_admin_access():
    """Check if current user has access to admin panel.

    This function is used in app context and can be called in all templates.
    """
    return admin_access_permission.can()


def admin_permission_factory(admin_view):
    """Admin permission factory."""
    if admin_view.name in ['Home']:
        return admin_access_permission
    return superuser_access_permission


def can_list_record_factory(**kwargs):
    """Factory to check if a ressource can be listed."""
    return type('Allow', (), {'can': lambda self: True})()


def can_read_record_factory(record):
    """Factory to check if a record can be read."""
    return check_elasticsearch(record)


def can_create_record_factory(**kwargs):
    """Factory to check if a record can be created."""
    return admin_access_permission


def can_update_record_factory(**kwargs):
    """Factory to check if a record can be updated."""
    return admin_access_permission


def can_delete_record_factory(**kwargs):
    """Factory to check if a record can be deleted."""
    return admin_access_permission