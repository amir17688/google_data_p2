"""
The manager class for the CMS models
"""
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.utils.timezone import now

from fluent_blogs import appsettings
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel


class EntryQuerySet(QuerySet):
    """
    The QuerySet for entry models.
    """

    def parent_site(self, site):
        """
        Filter to the given site.
        """
        return self.filter(parent_site=site)

    def published(self):
        """
        Return only published entries for the current site.
        """
        if appsettings.FLUENT_BLOGS_FILTER_SITE_ID:
            qs = self.parent_site(settings.SITE_ID)
        else:
            qs = self

        return qs \
            .filter(status=self.model.PUBLISHED) \
            .filter(
                Q(publication_date__isnull=True) |
                Q(publication_date__lte=now())
            ).filter(
                Q(publication_end_date__isnull=True) |
                Q(publication_end_date__gte=now())
            )

    def authors(self, *usernames):
        """
        Return the entries written by the given usernames
        When multiple tags are provided, they operate as "OR" query.
        """
        if len(usernames) == 1:
            return self.filter(author__username=usernames[0])
        else:
            return self.filter(author__username__in=usernames)

    def categories(self, *category_slugs):
        """
        Return the entries with the given category slugs.
        When multiple tags are provided, they operate as "OR" query.
        """
        categories_field = getattr(self.model, 'categories', None)
        if categories_field is None:
            raise AttributeError("The {0} does not include CategoriesEntryMixin".format(self.model.__name__))

        if issubclass(categories_field.rel.model, TranslatableModel):
            # Needs a different field, assume slug is translated (e.g django-categories-i18n)
            filters = {
                'categories__translations__slug__in': category_slugs,
            }

            # TODO: should the current language also be used as filter somehow?
            languages = self._get_active_rel_languages()
            if languages:
                if len(languages) == 1:
                    filters['categories__translations__language_code'] = languages[0]
                else:
                    filters['categories__translations__language_code__in'] = languages

            return self.filter(**filters).distinct()
        else:
            return self.filter(categories__slug=category_slugs)

    def tagged(self, *tag_slugs):
        """
        Return the items which are tagged with a specific tag.
        When multiple tags are provided, they operate as "OR" query.
        """
        if getattr(self.model, 'tags', None) is None:
            raise AttributeError("The {0} does not include TagsEntryMixin".format(self.model.__name__))

        if len(tag_slugs) == 1:
            return self.filter(tags__slug=tag_slugs[0])
        else:
            return self.filter(tags__slug__in=tag_slugs).distinct()

    def _get_active_rel_languages(self):
        return ()


class TranslatableEntryQuerySet(TranslatableQuerySet, EntryQuerySet):

    def __init__(self, *args, **kwargs):
        super(TranslatableEntryQuerySet, self).__init__(*args, **kwargs)
        self._rel_language_codes = None

    def _clone(self, *args, **kw):
        c = super(TranslatableQuerySet, self)._clone(*args, **kw)
        c._rel_language_codes = self._rel_language_codes
        return c

    def active_translations(self, language_code=None, **translated_fields):
        # overwritten to honor our settings instead of the django-parler defaults
        language_codes = appsettings.FLUENT_BLOGS_LANGUAGES.get_active_choices(language_code)
        return self.translated(*language_codes, **translated_fields)

    def translated(self, *language_codes, **translated_fields):
        self._rel_language_codes = language_codes
        return super(TranslatableEntryQuerySet, self).translated(*language_codes, **translated_fields)

    def _get_active_rel_languages(self):
        return self._rel_language_codes


class EntryManager(models.Manager):
    """
    Extra methods attached to ``Entry.objects`` .
    """
    queryset_class = EntryQuerySet

    def get_queryset(self):
        return self.queryset_class(self.model, using=self._db)

    def parent_site(self, site):
        """
        Filter to the given site.
        """
        # NOTE: by using .all(), the correct get_queryset() or get_query_set() method is called.
        # Just calling self.get_queryset() will break the RelatedManager.get_query_set() override in Django 1.5
        # This avoids all issues with Django 1.5/1.6/1.7 compatibility.
        return self.all().parent_site(site)

    def published(self):
        """
        Return only published entries for the current site.
        """
        return self.all().published()

    def authors(self, *usernames):
        """
        Return the entries written by the given usernames
        When multiple tags are provided, they operate as "OR" query.
        """
        return self.all().authors(*usernames)

    def categories(self, *category_slugs):
        """
        Return the entries with the given category slugs.
        When multiple tags are provided, they operate as "OR" query.
        """
        return self.all().categories(*category_slugs)

    def tagged(self, *tag_slugs):
        """
        Return the items which are tagged with a specific tag.
        When multiple tags are provided, they operate as "OR" query.
        """
        return self.all().tagged(*tag_slugs)


class TranslatableEntryManager(EntryManager, TranslatableManager):
    """
    Extra methods attached to ``Entry.objects``.
    """
    queryset_class = TranslatableEntryQuerySet
