# -*- coding: utf-8 -*-
#
# Swiss Open Access Repository
# Copyright (C) 2022 RERO+
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

"""DOJSON transformation for SOAP2."""

from dojson import utils

from sonar.modules.documents.dojson.overdo import Overdo

overdo = Overdo()


@overdo.over('abstracts', '^520..')
@utils.for_each_value
@utils.ignore_value
def marc21_to_abstract(self, key, value):
    """Get abstract."""
    abstract = value.get('a')
    language = value.get('9', 'eng')

    if not abstract:
        return None

    if language == 'fr':
        language = 'fre'

    abstracts_data = self.get('abstracts', [])
    abstracts_data.append({'value': abstract, 'language': language})

    self['abstracts'] = abstracts_data

    return None


@overdo.over('identifiedBy', '856')
@utils.ignore_value
def marc21_to_identified_by_from_856(self, key, value):
    """Get identifier from field 856."""
    identified_by = self.get('identifiedBy', [])

    if not value.get('u'):
        return None

    identified_by.append({
        'type': 'bf:Local',
        'source': 'SOAP2',
        'value': value.get('u')
    })

    return identified_by


@overdo.over('language', '^546')
@utils.for_each_value
@utils.ignore_value
def marc21_to_language(self, key, value):
    """Get languages."""
    if not value.get('a'):
        return None

    language = self.get('language', [])

    codes = utils.force_list(value.get('a'))

    for code in codes:
        language.append({'type': 'bf:Language', 'value': code})

    self['language'] = language

    return None


@overdo.over('title', '^245..')
@utils.for_each_value
@utils.ignore_value
def marc21_to_title_245(self, key, value):
    """Get title."""
    main_title = value.get('a', 'No title found')
    language = value.get('9', 'eng')

    title = {
        'type': 'bf:Title',
        'mainTitle': [{
            'value': main_title,
            'language': language
        }]
    }

    return title


@overdo.over('usageAndAccessPolicy', '^540..')
@utils.ignore_value
def marc21_to_usage_and_access_policy(self, key, value):
    """Extract usage and access policy."""
    if not value.get('a'):
        return None

    return {'label': value.get('a'), 'license': 'License undefined'}


@overdo.over('contribution', '^100..')
@utils.ignore_value
def marc21_to_contribution_field_100(self, key, value):
    """Extract contribution from field 100."""
    if not value.get('a'):
        return None

    contribution = self.get('contribution', [])

    data = {
        'agent': {
            'type': 'bf:Person',
            'preferred_name': value.get('a')
        },
        'role': ['cre']
    }

    # Affiliation
    if value.get('u'):
        data['affiliation'] = value.get('u')

    contribution.append(data)
    self['contribution'] = contribution

    return None

@overdo.over('contribution', '^700..')
@utils.for_each_value
@utils.ignore_value
def marc21_to_contribution_field_700(self, key, value):
    """Extract contribution from field 700."""
    if not value.get('a'):
        return None

    contribution = self.get('contribution', [])

    role = overdo.get_contributor_role(value.get('e'))

    if not role:
        raise Exception('No role found for contributor {contribution}'.format(
            contribution=value))

    data = {
        'agent': {
            'type': 'bf:Person',
            'preferred_name': value.get('a')
        },
        'role': [role]
    }

    # Affiliation
    if value.get('u'):
        data['affiliation'] = value.get('u')

    contribution.append(data)
    self['contribution'] = contribution

    return None


@overdo.over('partOf', '^786..')
@utils.for_each_value
@utils.ignore_value
def marc21_to_part_of(self, key, value):
    """Extract related document for record."""

    data = {}
    document = {}

    # Title is found
    if value.get('n'):
        document['title'] = value.get('n')

    if document:
        data['document'] = document

    return data
