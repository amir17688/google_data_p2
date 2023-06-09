import os.path

from django_nose.tools import (
    assert_equal,
    assert_false,
    assert_not_equal,
    assert_raises,
    assert_true
)
from mock import ANY, Mock, patch, PropertyMock

from pontoon.base.models import (
    Entity,
    Repository,
    Resource,
    TranslatedResource,
)
from pontoon.base.tests import (
    CONTAINS,
    NOT,
    UserFactory,
)
from pontoon.sync.core import (
    commit_changes,
    entity_key,
    pull_changes,
    update_entities,
    update_resources,
    update_translated_resources,
    update_translations,
)
from pontoon.sync.tests import FAKE_CHECKOUT_PATH, FakeCheckoutTestCase


class UpdateEntityTests(FakeCheckoutTestCase):
    def call_update_entities(self, collected):
        with patch('pontoon.sync.core.collect_entities') as mock_collect_entities:
            mock_collect_entities.return_value = collected
            return update_entities(self.db_project, self.vcs_project, self.changeset)

    def test_none(self):
        """
        If both the db_entity and vcs_entity are None, raise a
        CommandError, as that should never happen.
        """
        with assert_raises(ValueError):
            self.call_update_entities([('key', None, None)])

    def test_obsolete(self):
        """If VCS is missing the entity in question, obsolete it."""
        self.changeset.obsolete_db_entity = Mock()
        self.call_update_entities([('key', self.main_db_entity, None)])
        self.changeset.obsolete_db_entity.assert_called_with(self.main_db_entity)

    def test_create(self):
        """If the DB is missing an entity in VCS, create it."""
        self.changeset.create_db_entity = Mock()
        self.call_update_entities([('key', None, self.main_vcs_entity)])
        self.changeset.create_db_entity.assert_called_with(self.main_vcs_entity)


class UpdateTranslationsTests(FakeCheckoutTestCase):
    def call_update_translations(self, collected):
        with patch('pontoon.sync.core.collect_entities') as mock_collect_entities:
            mock_collect_entities.return_value = collected
            return update_translations(self.db_project, self.vcs_project,
                                       self.translated_locale, self.changeset)

    def test_missing_entities(self):
        """If either of the entities is missing, skip it."""
        self.changeset.update_vcs_entity = Mock()
        self.changeset.update_db_entity = Mock()

        self.call_update_translations([
            ('one', None, self.main_vcs_entity),
            ('other', self.main_db_entity, None),
            ('both', None, None),
        ])
        assert_false(self.changeset.update_vcs_entity.called)
        assert_false(self.changeset.update_db_entity.called)

    def test_no_translation(self):
        """If no translation exists for a specific locale, skip it."""
        self.changeset.update_vcs_entity = Mock()
        self.changeset.update_db_entity = Mock()
        self.main_vcs_entity.has_translation_for = Mock(return_value=False)

        self.call_update_translations([('key', self.main_db_entity, self.main_vcs_entity)])
        assert_false(self.changeset.update_vcs_entity.called)
        assert_false(self.changeset.update_db_entity.called)

    def test_db_changed(self):
        """
        If the DB entity has changed since the last sync, update the
        VCS.
        """
        self.changeset.update_vcs_entity = Mock()
        with patch.object(Entity, 'has_changed', return_value=True):
            self.call_update_translations([('key', self.main_db_entity, self.main_vcs_entity)])

        self.changeset.update_vcs_entity.assert_called_with(
            self.translated_locale, self.main_db_entity, self.main_vcs_entity
        )

    def test_vcs_changed(self):
        """
        If the DB entity has not changed since the last sync, update the DB with
        the latest changes from VCS.
        """
        self.changeset.update_db_entity = Mock()
        with patch.object(Entity, 'has_changed', return_value=False):
            self.call_update_translations([('key', self.main_db_entity, self.main_vcs_entity)])

        self.changeset.update_db_entity.assert_called_with(
            self.translated_locale, self.main_db_entity, self.main_vcs_entity
        )


class UpdateResourcesTests(FakeCheckoutTestCase):
    def test_basic(self):
        # Check for self.main_db_resource to be updated and
        # self.other_db_resource to be created.
        self.main_db_resource.total_strings = 5000
        self.main_db_resource.save()
        self.other_db_resource.delete()

        update_resources(self.db_project, self.vcs_project)
        self.main_db_resource.refresh_from_db()
        assert_equal(self.main_db_resource.total_strings, len(self.main_vcs_resource.entities))

        other_db_resource = Resource.objects.get(path=self.other_vcs_resource.path)
        assert_equal(other_db_resource.total_strings, len(self.other_vcs_resource.entities))


class UpdateTranslatedResourcesTests(FakeCheckoutTestCase):
    def test_basic(self):
        """
        Create/update the TranslatedResource object on all resources
        available in the current locale.
        """
        update_translated_resources(self.db_project, self.vcs_project,
                             self.changeset, self.translated_locale)

        assert_true(TranslatedResource.objects.filter(
            resource=self.main_db_resource, locale=self.translated_locale
        ).exists())

        assert_true(TranslatedResource.objects.filter(
            resource=self.other_db_resource, locale=self.translated_locale
        ).exists())

        assert_false(TranslatedResource.objects.filter(
            resource=self.missing_db_resource, locale=self.translated_locale
        ).exists())

    def test_asymmetric(self):
        """
        Create/update the TranslatedResource object on asymmetric resources
        even if they don't exist in the target locale.
        """
        with patch.object(Resource, 'is_asymmetric', new_callable=PropertyMock) as is_asymmetric:
            is_asymmetric.return_value = True

            update_translated_resources(self.db_project, self.vcs_project,
                                 self.changeset, self.translated_locale)

            assert_true(TranslatedResource.objects.filter(
                resource=self.main_db_resource, locale=self.translated_locale
            ).exists())

            assert_true(TranslatedResource.objects.filter(
                resource=self.other_db_resource, locale=self.translated_locale
            ).exists())

            assert_true(TranslatedResource.objects.filter(
                resource=self.missing_db_resource, locale=self.translated_locale
            ).exists())

    def test_extra_locales(self):
        """
        Only create/update the TranslatedResource object for active locales,
        even if the inactive locale has a resource.
        """
        update_translated_resources(self.db_project, self.vcs_project,
                             self.changeset, self.translated_locale)

        assert_true(TranslatedResource.objects.filter(
            resource=self.main_db_resource, locale=self.translated_locale
        ).exists())

        assert_true(TranslatedResource.objects.filter(
            resource=self.other_db_resource, locale=self.translated_locale
        ).exists())

        assert_false(TranslatedResource.objects.filter(
            resource=self.main_db_resource, locale=self.inactive_locale
        ).exists())

        assert_false(TranslatedResource.objects.filter(
            resource=self.other_db_resource, locale=self.inactive_locale
        ).exists())


class EntityKeyTests(FakeCheckoutTestCase):
    def test_entity_key_common_string(self):
        """
        Entities with the same string from different resources must not get the
        same key from entity_key.
        """
        assert_not_equal(
            entity_key(self.main_vcs_resource.entities['Common String']),
            entity_key(self.other_vcs_resource.entities['Common String'])
        )


class CommitChangesTests(FakeCheckoutTestCase):
    def setUp(self):
        super(CommitChangesTests, self).setUp()
        self.mock_repo_commit = self.patch_object(Repository, 'commit')

    def test_multiple_authors(self):
        """
        Tests if multiple authors are passed to commit message. The
        author with the most occurrances for the locale should be set as
        the commit author.
        """
        first_author, second_author = UserFactory.create_batch(2)
        self.changeset.commit_authors_per_locale = {
            self.translated_locale.code: [first_author, first_author, second_author]
        }
        self.db_project.repository_for_path = Mock(return_value=self.repository)

        commit_changes(self.db_project, self.vcs_project,
                       self.changeset, self.translated_locale)
        self.repository.commit.assert_called_with(
            CONTAINS(first_author.display_name_and_email, second_author.display_name_and_email),
            first_author,
            os.path.join(FAKE_CHECKOUT_PATH, self.translated_locale.code)
        )

    def test_author_with_multiple_contributions(self):
        """
        Tests if author with multiple contributions occurs once in commit message.
        """
        author = UserFactory.create()
        self.changeset.commit_authors_per_locale = {
            self.translated_locale.code: [author, author]
        }
        self.db_project.repository_for_path = Mock(return_value=self.repository)

        commit_changes(self.db_project, self.vcs_project,
                       self.changeset, self.translated_locale)
        self.repository.commit.assert_called_with(
            CONTAINS(author.display_name_and_email),
            author,
            os.path.join(FAKE_CHECKOUT_PATH, self.translated_locale.code)
        )
        commit_message = self.repository.commit.mock_calls[0][1][0]
        assert_equal(commit_message.count(author.display_name_and_email), 1)

    def test_no_authors(self):
        """
        If no authors are found in the changeset, default to a fake
        "Mozilla Pontoon" user.
        """
        self.changeset.commit_authors_per_locale = {
            self.translated_locale.code: []
        }
        self.db_project.repository_for_path = Mock(return_value=self.repository)

        commit_changes(self.db_project, self.vcs_project,
                       self.changeset, self.translated_locale)
        self.repository.commit.assert_called_with(
            NOT(CONTAINS('Authors:')),  # Don't list authors in commit
            ANY,
            os.path.join(FAKE_CHECKOUT_PATH, self.translated_locale.code)
        )
        user = self.mock_repo_commit.call_args[0][1]
        assert_equal(user.first_name, 'Mozilla Pontoon')
        assert_equal(user.email, 'pontoon@mozilla.com')


class PullChangesTests(FakeCheckoutTestCase):
    def setUp(self):
        super(PullChangesTests, self).setUp()
        self.mock_repo_pull = self.patch_object(Repository, 'pull')

    def test_basic(self):
        """
        Pull_changes should call repo.pull for each repo for the
        project, save the return value to repo.last_synced_revisions,
        and return whether any changes happened in VCS.
        """
        self.mock_repo_pull.return_value = {'single_locale': 'asdf'}
        assert_true(pull_changes(self.db_project))
        self.repository.refresh_from_db()
        assert_equal(self.repository.last_synced_revisions, {'single_locale': 'asdf'})

    def test_unsure_changes(self):
        """
        If any of the repos returns None as a revision number, consider
        the VCS as changed even if the revisions match the last sync.
        """
        self.mock_repo_pull.return_value = {'single_locale': None}
        self.repository.last_synced_revisions = {'single_locale': None}
        self.repository.save()

        assert_true(pull_changes(self.db_project))

    def test_unchanged(self):
        """
        If the revisions returned by repo.pull match those from the last
        sync, consider the VCS unchanged and return False.
        """
        self.mock_repo_pull.return_value = {'single_locale': 'asdf'}
        self.repository.last_synced_revisions = {'single_locale': 'asdf'}
        self.repository.save()

        assert_false(pull_changes(self.db_project))
