from .standard import StandardTable
from config.rds import Base, metadata

class MaxData(Base, StandardTable):
    __tablename__ = 'max_data'

class MinData(Base, StandardTable):
    __tablename__ = 'min_data'

class MeanData(Base, StandardTable):
    __tablename__ = 'mean_data'

class ModeData(Base, StandardTable):
    __tablename__ = 'mode_data'

class StdData(Base, StandardTable):
    __tablename__ = 'std_data'

class_handler = {
    'max': MaxData,
    'min': MinData,
    'mean': MeanData,
    'mode': ModeData,
    'std': StdData
}
3