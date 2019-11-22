#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: inventory source.py
#
# Copyright 2018 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for inventory_script.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import InvalidValue
from .core import (Entity,
                   validate_max_length)

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-03'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''inventory_script'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class InventoryScript(Entity):
    """Models the inventory script entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the inventory script.

        Returns:
            string: The name of the inventory script.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the inventory script.

        Returns:
            None:

        """
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue(('{value} is invalid. Condition max_characters must be '
                                'less or equal to {max_characters}').format(value=value,
                                                                            max_characters=max_characters))

    @property
    def description(self):
        """The description of the inventory script.

        Returns:
            string: The description of the inventory script.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the first name of the inventory script.

        Returns:
            None:

        """
        self._update_values('description', value)

    @property
    def script(self):
        """The script of the inventory script.

        Returns:
            string: The script of the inventory script.

        """
        return self._data.get('script')

    @script.setter
    def script(self, value):
        """Update the script of the inventory script.

        Returns:
            None:

        """
        self._update_values('script', value)

    def create_inventory_script(self, name, description, script, organization):
        """Creates a custom inventory script.

        Args:
            name: Name of the inventory script.
            description: The description of the inventory script.
            script: The script of the inventory script.
            organization: The organization the inventory script is part of.

        Returns:
            Inventory_script: The created inventory script is successful, None otherwise.

        """
        url = '{api}/inventory_scripts/'.format(api=self._tower.api)
        payload = {'name': name,
                   'description': description,
                   'inventory': self.id,
                   'script': script,
                   'organization': organization
                   }
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating host "%s", response was "%s"', name, response.text)
        return response.json() if response.ok else None
