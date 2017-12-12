#!/usr/bin/env python3

"""snippet.py: Snippet management."""

from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.migrate.migrate import Migrate
from snippy.content.content import Content


class Snippet(object):
    """Snippet management."""

    def __init__(self, storage, content_type=Const.CONTENT_TYPE_TEXT):
        self.logger = Logger(__name__).get()
        self.storage = storage
        self.content_type = content_type

    def create(self):
        """Create new snippet."""

        self.logger.debug('creating new snippet')
        snippet = Config.get_content(Content())
        if not snippet.has_data():
            Cause.push(Cause.HTTP_BAD_REQUEST, 'mandatory snippet data not defined')
        else:
            self.storage.create(snippet)

    def search(self):
        """Search snippets."""

        self.logger.info('searching snippets')
        snippets = self.storage.search(Const.SNIPPET,
                                       sall=Config.get_search_all(),
                                       stag=Config.get_search_tag(),
                                       sgrp=Config.get_search_grp(),
                                       digest=Config.get_content_digest(),
                                       data=Config.get_content_data())
        snippets = Migrate.content(snippets, self.content_type)

        return snippets

    def update(self):
        """Update snippet."""

        snippets = self.storage.search(Const.SNIPPET,
                                       sall=Config.get_search_all(),
                                       stag=Config.get_search_tag(),
                                       sgrp=Config.get_search_grp(),
                                       digest=Config.get_content_digest(),
                                       data=Config.get_content_data())
        if len(snippets) == 1:
            self.logger.debug('updating snippet with digest %.16s', snippets[0].get_digest())
            snippet = Config.get_content(content=snippets[0], use_editor=True)
            self.storage.update(snippet)
        else:
            Config.validate_search_context(snippets, 'update')

    def delete(self):
        """Delete snippet."""

        snippets = self.storage.search(Const.SNIPPET,
                                       sall=Config.get_search_all(),
                                       stag=Config.get_search_tag(),
                                       sgrp=Config.get_search_grp(),
                                       digest=Config.get_content_digest(),
                                       data=Config.get_content_data())
        if len(snippets) == 1:
            self.logger.debug('deleting snippet with digest %.16s', snippets[0].get_digest())
            self.storage.delete(snippets[0].get_digest())
        else:
            Config.validate_search_context(snippets, 'delete')

    def export_all(self):
        """Export snippets."""

        filename = Config.get_operation_file()
        if Config.is_migrate_template():
            self.logger.debug('exporting snippet template %s', Config.get_operation_file())
            Migrate.dump_template(Content())
        elif Config.is_search_criteria():
            self.logger.debug('exporting snippets based on search criteria')
            snippets = self.storage.search(Const.SNIPPET,
                                           sall=Config.get_search_all(),
                                           stag=Config.get_search_tag(),
                                           sgrp=Config.get_search_grp(),
                                           digest=Config.get_content_digest(),
                                           data=Config.get_content_data())
            if len(snippets) == 1:
                filename = Config.get_operation_file(content_filename=snippets[0].get_filename())
            elif not snippets:
                Config.validate_search_context(snippets, 'export')
            Migrate.dump(snippets, filename)
        else:
            self.logger.debug('exporting all snippets %s', filename)
            snippets = self.storage.export_content(Const.SNIPPET)
            Migrate.dump(snippets, filename)

    def import_all(self):
        """Import snippets."""

        content_digest = Config.get_content_valid_digest()
        if content_digest:
            snippets = self.storage.search(Const.SNIPPET, digest=content_digest)
            if len(snippets) == 1:
                dictionary = Migrate.load(Config.get_operation_file(), Content())
                contents = Content.load(dictionary)
                snippets[0].migrate_edited(contents)
                self.storage.update(snippets[0])
            elif not snippets:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find snippet identified with digest {:.16}'.format(content_digest))
            else:
                Cause.push(Cause.HTTP_CONFLICT, 'cannot import multiple snippets with same digest {:.16}'.format(content_digest))
        else:
            self.logger.debug('importing snippets %s', Config.get_operation_file())
            dictionary = Migrate.load(Config.get_operation_file(), Content())
            snippets = Content.load(dictionary)
            self.storage.import_content(snippets)

    def run(self):
        """Run the snippet management operation."""

        snippets = Const.EMPTY

        self.logger.info('managing snippet')
        Config.set_category(Const.SNIPPET)
        if Config.is_operation_create():
            self.create()
        elif Config.is_operation_search():
            snippets = self.search()
        elif Config.is_operation_update():
            self.update()
        elif Config.is_operation_delete():
            self.delete()
        elif Config.is_operation_export():
            self.export_all()
        elif Config.is_operation_import():
            self.import_all()
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'unknown operation for snippet')

        return snippets
