from sqlalchemy import Column, Float, String, Integer
from models.base import Base


class AircraftData(object):

    id = Column(Integer, primary_key=True, autoincrement=True)
    aircraftsernum_1 = Column(Float)
    phaseoflight_1 = Column(Float)
    amschprsovdrivf_1a = Column(Float)
    amschprsovdrivf_1b = Column(Float)
    amschprsovdrivf_2b = Column(Float)
    amscprsovdrivf_1a = Column(Float)
    amscprsovdrivf_1b = Column(Float)
    amscprsovdrivf_2b = Column(Float)
    basbleedlowpresf_1a = Column(Float)
    basbleedlowpresf_2b = Column(Float)
    basbleedlowtempf_1a = Column(Float)
    basbleedlowtempf_2b = Column(Float)
    basbleedoverpresf_1a = Column(Float)
    basbleedoverpresf_2b = Column(Float)
    basbleedovertempf_1a = Column(Float)
    basbleedovertempf_2b = Column(Float)
    bleedfavtmcmd_1a = Column(Float)
    bleedfavtmcmd_1b = Column(Float)
    bleedfavtmcmd_2a = Column(Float)
    bleedfavtmcmd_2b = Column(Float)
    bleedfavtmfbk_1a = Column(Float)
    bleedfavtmfbk_1b = Column(Float)
    bleedfavtmfbk_2b = Column(Float)
    bleedhprsovcmdstatus_1a = Column(Float)
    bleedhprsovcmdstatus_1b = Column(Float)
    bleedhprsovcmdstatus_2a = Column(Float)
    bleedhprsovcmdstatus_2b = Column(Float)
    bleedhprsovopostatus_1a = Column(Float)
    bleedhprsovopostatus_1b = Column(Float)
    bleedhprsovopostatus_2a = Column(Float)
    bleedhprsovopostatus_2b = Column(Float)
    bleedmonpres_1a = Column(Float)
    bleedmonpres_1b = Column(Float)
    bleedmonpres_2a = Column(Float)
    bleedmonpres_2b = Column(Float)
    bleedonstatus_1a = Column(Float)
    bleedonstatus_1b = Column(Float)
    bleedonstatus_2b = Column(Float)
    bleedoverprescas_2a = Column(Float)
    bleedoverprescas_2b = Column(Float)
    bleedprecoldifpres_1a = Column(Float)
    bleedprecoldifpres_1b = Column(Float)
    bleedprecoldifpres_2a = Column(Float)
    bleedprecoldifpres_2b = Column(Float)
    bleedprsovclpostatus_1a = Column(Float)
    bleedprsovclpostatus_2a = Column(Float)
    date = Column(String)
    duration = Column(Float)
    cumulative_duration = Column(Float)
    time_to_failure = Column(Float)


class MaxData(AircraftData, Base):
    __tablename__ = 'max_data'


class MinData(AircraftData, Base):
    __tablename__ = 'min_data'


class MeanData(AircraftData, Base):
    __tablename__ = 'mean_data'


class ModeData(AircraftData, Base):
    __tablename__ = 'mode_data'


class StdData(AircraftData, Base):
    __tablename__ = 'std_data'


class_handler = {
    "max": MaxData,
    "min": MinData,
    "mean": MeanData,
    "mode": ModeData,
    "std": StdData
}
