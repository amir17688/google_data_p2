# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.comments`.

"""
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

try:
    import bleach
except ImportError:
    bleach = None

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.modlib.gfks.mixins import Controllable

from lino.api import dd
from lino import mixins
from lino.modlib.users.mixins import ByUser, UserAuthored
from lino.utils.xmlgen.html import E


@dd.python_2_unicode_compatible
class Comment(
        mixins.CreatedModified,
        UserAuthored,
        # mixins.Hierarchical,
        Controllable):
    """A **comment** is a short text which some user writes about some
    other database object.

    .. attribute:: short_text

        A short "abstract" of your comment. This should not be more
        than one paragraph.

    """

    ALLOWED_TAGS = ['a', 'b', 'i', 'em']

    class Meta(object):
        app_label = 'comments'
        abstract = dd.is_abstract_model(__name__, 'Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    short_text = dd.RichTextField(_("Short text"))
    more_text = dd.RichTextField(_("More text"), blank=True)

    def __str__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def as_li(self, ar):
        """Return this comment as a list item. If `bleach
        <http://bleach.readthedocs.org/en/latest/>`_ is installed, all
        tags except some will be removed when

        """
        txt = ar.parse_memo(self.short_text)
        if bleach is None:
            chunks = [txt]
        else:
            chunks = [bleach.clean(
                txt, tags=self.ALLOWED_TAGS, strip=True)]

        by = _("{0} by {1}").format(
            naturaltime(self.created), str(self.user)),
        chunks += [
            " (", E.tostring(ar.obj2html(self, by)), ")"
        ]
        if self.more_text:
            chunks.append(" (...)")

        html = ''.join(chunks)
        return "<li>" + html + "</li>"

dd.update_field(Comment, 'user', editable=False)


from .ui import *
