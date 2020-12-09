from abc import ABC, abstractmethod
from dataclasses import dataclass
from wnghub.config.config import Config
from wnghub.model.notification import Notification
from wnghub.controller.base import BaseController
from typing import List, Optional, Callable

import click
import os
from prettytable import PrettyTable


@dataclass
class Attribute:
    header: str
    field_name: str
    min_size: Optional[int] = None
    max_size: Optional[int] = None


class BaseNotificationViewController(BaseController, ABC):
    """
    Base class for viewing notifications. Not opinionated about
    stdout nor formatting the table.
    """

    _excluded_for_terminal = False

    _expand_terminal_msg = "*** Expand your terminal for more information ***"

    _no_notifications_msg = "No new matching notifications!"

    _fields_index = 0

    _headers_index = 1

    _default_attributes = [
        Attribute("abbrev_title", "Title"),
        Attribute("html_url", "url"),
        Attribute("repository", "Repo", min_size=114),
        Attribute("type", "Type", min_size=121),
    ]

    def display(
        self,
        notifications: List[Notification],
        attributes: Optional[List[List[str]]] = None,
    ):
        """
        Displays notifications. Optionally pass in your
        own attributes, to override defaults in class.

        :param notifications: list of notifications to display
        :type notifications: List[Notification]
        :param attributes: optionally specify attributes to see
        :type attributes: Optional[List[List[str]]]
        """
        if len(notifications) < 1:
            self._write_stdout(self._no_notifications_msg)
            return
        if attributes is None:
            attributes = self._default_attributes
        attributes = self._remove_attributes_for_terminal_size(attributes)
        headers, fields = self._unpack_attributes(attributes)
        n_table = [[n.get(field) for field in fields] for n in notifications]
        self._display_table(headers, n_table)

    @abstractmethod
    def _display_table(self, headers, notifications_table):
        pass

    @abstractmethod
    def _write_stdout(self, str_to_write: str):
        pass

    def _remove_attributes_for_terminal_size(self, attributes):
        cols = os.get_terminal_size().columns
        result_attr = []
        for attr in attributes:
            if attr.min_size is None or cols >= attr.min_size:
                result_attr.append(attr)
            else:
                self._excluded_for_terminal = True
        return result_attr

    def _unpack_attributes(self, attributes):
        headers, fields = [], []
        for attr in attributes:
            headers.append(attr.field_name)
            fields.append(attr.header)

        return headers, fields


class NotificationViewController(BaseNotificationViewController):
    """
    Class for viewing notifications via CLI. Uses `prettytable`
    to create table with field names and headers.

    By default, the following fields will be displayed:
        - abbreviated title
        - repo name (not including org)
        - type (either pr or issue)
        - html url to what the notification is referencing

    Override the default fields by providing an array with
    the following to `display`:
    [
        [field name in notification (str), header for table (str)],
        ...
    ]

    :param config: the app config
    :type config: Config
    :param write_stdout: function to call with what to display to user
    :type write_stdout: Callable[[str], None]
    """

    def __init__(
        self, config: Config, write_stdout: Callable[[str], None] = click.echo
    ):
        self.stdout = write_stdout
        BaseNotificationViewController.__init__(self, config)

    def _display_table(self, headers, notifications_table):
        table = PrettyTable()
        table.field_names = headers
        table.add_rows(notifications_table)
        self._write_stdout(table.get_string())
        if self._excluded_for_terminal:
            self._write_stdout(self._expand_terminal_msg)

    def _write_stdout(self, str_to_write: str):
        self.stdout(str_to_write)
