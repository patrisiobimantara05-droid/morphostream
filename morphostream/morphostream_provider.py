# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Morphostream
                                 A QGIS plugin
 Plugin ini menyediakan algoritma analisis morfometri sungai dan DAS.
                              -------------------
        begin                : 2025-12-14
        copyright            : (C) 2025 by Patrisio Bimantara
        email                : patrisiobimantara05@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Patrisio Bimantara'
__date__ = '2025-12-14'
__copyright__ = '(C) 2025 by Patrisio Bimantara'

# -*- coding: utf-8 -*-
"""
MorphoStream Provider
---------------------
Provider ini mendaftarkan algoritma MorphoStream ke dalam Processing Toolbox QGIS.
"""

# -*- coding: utf-8 -*-
"""
MorphoStream Provider
---------------------
Provider ini mendaftarkan algoritma MorphoStream ke dalam Processing Toolbox QGIS.
"""

# -*- coding: utf-8 -*-
"""
MorphoStream Provider
---------------------
Provider ini mendaftarkan algoritma MorphoStream ke dalam Processing Toolbox QGIS.
"""

from qgis.core import QgsProcessingProvider
from .algorithms.morphometry_si import SinuosityAlgorithm
from .algorithms.morphometry_dd_rb import DdRbAlgorithm
from .algorithms.morphometry_das_params import DasParamsAlgorithm
# Kalau kamu pakai script gabungan morphometry.py, bisa aktifkan baris ini:
# from .algorithms.morphometry import MorphometryAlgorithm


class MorphoStreamProvider(QgsProcessingProvider):
    def id(self):
        """ID unik provider (tanpa spasi)"""
        return "morphostream"

    def name(self):
        """Nama provider yang tampil di Processing Toolbox"""
        return "MorphoStream"

    def loadAlgorithms(self):
        """Daftarkan algoritma ke Processing Toolbox"""
        self.addAlgorithm(SinuosityAlgorithm())
        self.addAlgorithm(DdRbAlgorithm())
        self.addAlgorithm(DasParamsAlgorithm())
        # Kalau mau gabungan, tambahkan:
        # self.addAlgorithm(MorphometryAlgorithm())

