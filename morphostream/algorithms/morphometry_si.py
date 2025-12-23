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
MorphoStream - Sinuosity Index
------------------------------
Menghitung Sinuosity Index (SI) dari sungai utama.
"""

# -*- coding: utf-8 -*-
"""
MorphoStream - Sinuosity Index
------------------------------
Menghitung Sinuosity Index (SI) dari sungai utama.
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFileDestination
)
import geopandas as gpd
import csv
from shapely.geometry import Point


class SinuosityAlgorithm(QgsProcessingAlgorithm):
    INPUT_RIVERS = 'INPUT_RIVERS'
    OUTPUT_CSV = 'OUTPUT_CSV'

    def name(self):
        return 'sinuosity_index'

    def displayName(self):
        return 'Sinuosity Index'

    def group(self):
        return 'MorphoStream'

    def groupId(self):
        return 'morphostream'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT_RIVERS,
            'Layer sungai utama (LineString)',
            [QgsProcessing.TypeVectorLine]
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT_CSV,
            'Output CSV',
            'CSV files (*.csv)'
        ))

    def processAlgorithm(self, parameters, context, feedback):
        rivers = self.parameterAsVectorLayer(parameters, self.INPUT_RIVERS, context)
        out_csv = self.parameterAsFileOutput(parameters, self.OUTPUT_CSV, context)

        # Konversi ke GeoDataFrame
        gR = gpd.GeoDataFrame.from_features(rivers.getFeatures(), crs=rivers.crs().authid())

        # Gabungkan semua geometri sungai
        main_geom = gR.geometry.unary_union

        # Ambil sungai terpanjang sebagai sungai utama
        if main_geom.geom_type == "MultiLineString":
            main_line = max(main_geom.geoms, key=lambda g: g.length)
        else:
            main_line = main_geom

        # Hitung panjang aktual (Ol) dan panjang lurus (El)
        Ol = main_line.length
        coords = list(main_line.coords)
        El = Point(coords[0]).distance(Point(coords[-1]))

        # Sinuosity Index
        SI = Ol / El if El > 0 else None

        # Simpan ke CSV
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['Ol_m', 'El_m', 'SinuosityIndex_SI'])
            w.writerow([Ol, El, SI])

        feedback.pushInfo("Sinuosity Index selesai dihitung.")
        return {self.OUTPUT_CSV: out_csv}