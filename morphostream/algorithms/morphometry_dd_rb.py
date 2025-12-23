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
MorphoStream - Drainage Density & Bifurcation Ratio
---------------------------------------------------
Menghitung Dd dan Rb dari jaringan sungai.
"""

# -*- coding: utf-8 -*-
"""
MorphoStream - Drainage Density & Bifurcation Ratio
---------------------------------------------------
Menghitung Drainage Density (Dd) dan Bifurcation Ratio (Rb) dari jaringan sungai.
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFileDestination
)
import geopandas as gpd
import csv


class DdRbAlgorithm(QgsProcessingAlgorithm):
    INPUT_RIVERS = 'INPUT_RIVERS'
    INPUT_DAS = 'INPUT_DAS'
    OUTPUT_CSV = 'OUTPUT_CSV'

    def name(self):
        return 'dd_rb_analysis'

    def displayName(self):
        return 'Drainage Density & Bifurcation Ratio'

    def group(self):
        return 'MorphoStream'

    def groupId(self):
        return 'morphostream'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT_RIVERS,
            'Layer sungai (dengan kolom order)',
            [QgsProcessing.TypeVectorLine]
        ))
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT_DAS,
            'Layer batas DAS',
            [QgsProcessing.TypeVectorPolygon]
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT_CSV,
            'Output CSV',
            'CSV files (*.csv)'
        ))

    def processAlgorithm(self, parameters, context, feedback):
        rivers = self.parameterAsVectorLayer(parameters, self.INPUT_RIVERS, context)
        das = self.parameterAsVectorLayer(parameters, self.INPUT_DAS, context)
        out_csv = self.parameterAsFileOutput(parameters, self.OUTPUT_CSV, context)

        # Konversi ke GeoDataFrame
        gR = gpd.GeoDataFrame.from_features(rivers.getFeatures(), crs=rivers.crs().authid())
        gA = gpd.GeoDataFrame.from_features(das.getFeatures(), crs=das.crs().authid())

        # Drainage Density (Dd) = total panjang sungai / luas DAS
        total_length_km = gR.length.sum() / 1000
        area_km2 = gA.area.sum() / 1e6
        Dd = total_length_km / area_km2 if area_km2 > 0 else None

        # Bifurcation Ratio (Rb) = jumlah sungai order n / jumlah sungai order n+1
        Rb = None
        if 'order' in gR.columns:
            order_counts = gR['order'].value_counts().sort_index()
            ratios = []
            for i in range(len(order_counts) - 1):
                higher = order_counts.iloc[i]
                lower = order_counts.iloc[i + 1]
                if lower > 0:
                    ratios.append(higher / lower)
            Rb = sum(ratios) / len(ratios) if ratios else None

        # Simpan ke CSV
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['TotalLength_km', 'Area_km2', 'DrainageDensity_Dd', 'BifurcationRatio_Rb'])
            w.writerow([total_length_km, area_km2, Dd, Rb])

        feedback.pushInfo("Drainage Density & Bifurcation Ratio selesai dihitung.")
        return {self.OUTPUT_CSV: out_csv}