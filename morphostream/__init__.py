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
MorphoStream QGIS Plugin
------------------------
Plugin untuk analisis morfometri sungai dan DAS.
"""

def classFactory(iface):
    from .morphostream_provider import MorphoStreamProvider
    return MorphoStreamProvider()