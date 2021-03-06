# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=invalid-name, too-few-public-methods
# pylint: disable=too-many-instance-attributes

"""pip building block"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import logging # pylint: disable=unused-import

from hpccm.building_blocks.packages import packages
from hpccm.primitives.comment import comment
from hpccm.primitives.shell import shell

class pip(object):
    """The `pip` building block installs Python packages from PyPi.

    # Parameters

    ospackages: List of OS packages to install prior to installing
    PyPi packages.  For Ubuntu, the default values are `python-pip`,
    `python-setuptools`, and `python-wheel` for Python 2.x and
    `python3-pip`, `python3-setuptools`, and `python3-wheel` for
    Python 3.x.  For RHEL-based Linux distributions, the default
    values are `python-pip` for Python 2.x and `python34-pip` for
    Python 3.x.

    packages: List of PyPi packages to install.  The default is
    an empty list.

    pip: The name of the `pip` tool to use. The default is `pip`.

    upgrade: Boolean flag to control whether pip itself should be
    upgraded prior to installing any PyPi packages.  The default is
    False.

    # Examples

    ```python
    pip(packages=['hpccm'])
    ```

    ```python
    pip(packages=['hpccm'], pip='pip3')
    ```

    """

    def __init__(self, **kwargs):
        """Initialize building block"""

        # Trouble getting MRO with kwargs working correctly, so just call
        # the parent class constructors manually for now.
        #super(pip, self).__init__(**kwargs)

        self.__epel = False
        self.__ospackages = kwargs.get('ospackages', None)
        self.__packages = kwargs.get('packages', [])
        self.__pip = kwargs.get('pip', 'pip')
        self.__upgrade = kwargs.get('upgrade', False)

        self.__debs = [] # Filled in below
        self.__rpms = [] # Filled in below

        if self.__ospackages == None:
            if self.__pip.startswith('pip3'):
                self.__epel = True
                self.__debs.extend(['python3-pip', 'python3-setuptools',
                                    'python3-wheel'])
                self.__rpms.append('python34-pip')  # EPEL package
            else:
                self.__epel = True
                self.__debs.extend(['python-pip', 'python-setuptools',
                                    'python-wheel'])
                self.__rpms.append('python-pip')    # EPEL package
        elif self.__ospackages:
            self.__debs = self.__ospackages
            self.__rpms = self.__ospackages

    def __str__(self):
        """String representation of the building block"""
        instructions = []
        instructions.append(comment('pip'))
        if self.__debs or self.__rpms:
            instructions.append(packages(apt=self.__debs, epel=self.__epel,
                                         yum=self.__rpms))

        if self.__pip:
            cmds = []

            if self.__upgrade:
                cmds.append('{0} install --upgrade pip'.format(self.__pip))

            if self.__packages:
                cmds.append('{0} install {1}'.format(self.__pip,
                                                     ' '.join(self.__packages)))
            instructions.append(shell(commands=cmds))
        return '\n'.join([str(x) for x in instructions])
