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
MorphoStream - Parameter DAS
----------------------------
Menghitung parameter morfometri DAS (Form Factor, Circularity Ratio, Elongation Ratio, Compactness Coefficient).
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFileDestination
)
import geopandas as gpd
import numpy as np
import csv


class DasParamsAlgorithm(QgsProcessingAlgorithm):
    INPUT_DAS = 'INPUT_DAS'
    OUTPUT_CSV = 'OUTPUT_CSV'

    def name(self):
        return 'das_parameters'

    def displayName(self):
        return 'Parameter DAS (Ff, Rc, Re, Cc)'

    def group(self):
        return 'MorphoStream'

    def groupId(self):
        return 'morphostream'

    def initAlgorithm(self, config=None):
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
        das = self.parameterAsVectorLayer(parameters, self.INPUT_DAS, context)
        out_csv = self.parameterAsFileOutput(parameters, self.OUTPUT_CSV, context)

        # Konversi ke GeoDataFrame
        gA = gpd.GeoDataFrame.from_features(das.getFeatures(), crs=das.crs().authid())

        # Hitung luas dan keliling
        area_m2 = gA.area.sum()
        perimeter_m = gA.length.sum()

        # Panjang basin (bounding box terpanjang)
        bounds = gA.total_bounds  # minx, miny, maxx, maxy
        Lb_m = max(bounds[2] - bounds[0], bounds[3] - bounds[1])

        # Parameter morfometri
        Ff = (area_m2) / (Lb_m ** 2) if Lb_m > 0 else None
        Rc = (4 * np.pi * area_m2) / (perimeter_m ** 2) if perimeter_m > 0 else None
        Re = np.sqrt(area_m2 / np.pi) / (Lb_m / 2) if Lb_m > 0 else None
        Cc = perimeter_m / (2 * np.sqrt(np.pi * area_m2)) if area_m2 > 0 else None

        # Simpan ke CSV
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow([
                'Area_km2', 'Perimeter_km', 'Lb_km',
                'FormFactor_Ff', 'Circularity_Rc', 'Elongation_Re', 'Compactness_Cc'
            ])
            w.writerow([
                area_m2 / 1e6, perimeter_m / 1000, Lb_m / 1000,
                Ff, Rc, Re, Cc
            ])

        feedback.pushInfo("Parameter DAS selesai dihitung.")
        return {self.OUTPUT_CSV: out_csv}