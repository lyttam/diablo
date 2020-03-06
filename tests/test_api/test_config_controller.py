"""
Copyright ©2020. The Regents of the University of California (Regents). All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation
for educational, research, and not-for-profit purposes, without fee and without a
signed licensing agreement, is hereby granted, provided that the above copyright
notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
"AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.
"""

import pytest
from tests.util import override_config


@pytest.fixture()
def admin_session(fake_auth):
    fake_auth.login('2040')


class TestVersion:
    """Config API delivers Diablo version."""

    def test_anonymous_version_request(self, client):
        """Returns a well-formed response."""
        response = client.get('/api/version')
        assert response.status_code == 200
        assert 'version' in response.json
        assert 'build' in response.json


class TestConfigController:
    """Config API."""

    def test_anonymous(self, app, client):
        """Returns a well-formed response to anonymous user."""
        term_id = '2218'
        with override_config(app, 'CURRENT_TERM', term_id):
            response = client.get('/api/config')
            assert response.status_code == 200
            assert 'diabloEnv' in response.json
            data = response.json
            assert data['ebEnvironment'] is None
            assert '@' in data['supportEmailAddress']
            assert data['timezone'] == 'America/Los_Angeles'
            assert data['currentTermId'] == term_id
            assert data['currentTermName'] == 'Fall 2021'
