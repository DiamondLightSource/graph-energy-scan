from datetime import datetime
from typing import Optional

import strawberry
from sqlalchemy import select

from graph_energy_scan import models
from graph_energy_scan.database import current_session


@strawberry.type
class EnergyScan:
    id: int
    flourecenceDetector: Optional[str]
    scanFile: Optional[str]
    choochJpeg: Optional[str]
    element: Optional[str]
    startEnergy: Optional[float]
    endEnergy: Optional[float]
    transmissionFactor: Optional[float]
    exposureTime: Optional[float]
    synchrotronCurrent: Optional[float]
    temperature: Optional[float]
    peakEnergy: Optional[float]
    peakFPrime: Optional[float]
    peakFDoublePrime: Optional[float]
    inflectionEnergy: Optional[float]
    inflectionFPrime: Optional[float]
    inflectionFDoublePrime: Optional[float]
    xrayDose: Optional[float]
    startTime: Optional[datetime]
    endTime: Optional[datetime]
    edgeEnergy: Optional[str]
    beamSizeVertical: Optional[float]
    beamSizeHorizontal: Optional[float]

    @staticmethod
    def from_model(model: models.EnergyScan) -> "EnergyScan":
        return EnergyScan(
            id=model.energyScanId,
            flourecenceDetector=model.fluorescenceDetector,
            scanFile=f"file://{model.scanFileFullPath}"
            if model.scanFileFullPath is not None
            else None,
            choochJpeg=f"file://{model.jpegChoochFileFullPath}"
            if model.jpegChoochFileFullPath is not None
            else None,
            element=model.element,
            startEnergy=model.startEnergy,
            endEnergy=model.endEnergy,
            transmissionFactor=model.transmissionFactor,
            exposureTime=model.exposureTime,
            synchrotronCurrent=model.synchrotronCurrent,
            temperature=model.temperature,
            peakEnergy=model.peakEnergy,
            peakFPrime=model.peakFPrime,
            peakFDoublePrime=model.peakFDoublePrime,
            inflectionEnergy=model.inflectionEnergy,
            inflectionFPrime=model.inflectionFPrime,
            inflectionFDoublePrime=model.inflectionFDoublePrime,
            xrayDose=model.xrayDose,
            startTime=model.startTime,
            endTime=model.endTime,
            edgeEnergy=model.edgeEnergy,
            beamSizeHorizontal=model.beamSizeHorizontal,
            beamSizeVertical=model.beamSizeVertical,
        )


@strawberry.federation.type(keys=["id"])
class Session:
    id: int

    @strawberry.field
    async def energy_scans(self) -> list[EnergyScan]:
        async with current_session() as session:
            stmt = select(models.EnergyScan).where(
                models.EnergyScan.sessionId == self.id
            )
            return [EnergyScan.from_model(model) for model in session.scalars(stmt)]
