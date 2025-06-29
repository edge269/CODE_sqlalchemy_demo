from sqlalchemy import create_engine, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pathlib import Path

# declarative base class
class Base(DeclarativeBase):
    pass

class ReactorLocation(Base):
    __tablename__ = 'REACTOR_LOCATIONS'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reactor_location: Mapped[str] = mapped_column(String(32), nullable=False)
    plants: Mapped[list['Plant']] = relationship('Plant', back_populates='reactor_location')

class Epoch(Base):
    __tablename__ = 'EPOCHS'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    epoch: Mapped[str] = mapped_column(String(8), nullable=False)
    fuel_assemblies: Mapped[list['FuelAssembly']] = relationship('FuelAssembly', back_populates='epoch')

class ReactorDesign(Base):
    __tablename__ = 'REACTOR_DESIGN'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reactor_power: Mapped[int] = mapped_column(nullable=False)
    reactor_type: Mapped[str] = mapped_column(String(4), nullable=False)
    fuel_assemblies: Mapped[list['FuelAssembly']] = relationship('FuelAssembly', back_populates='reactor_design')

class Plant(Base):
    __tablename__ = 'PLANTS'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plant_name: Mapped[str] = mapped_column(String(32), nullable=False)
    reactor_location_id: Mapped[int] = mapped_column(ForeignKey('REACTOR_LOCATIONS.id'), nullable=False)
    reactor_location: Mapped['ReactorLocation'] = relationship('ReactorLocation', back_populates='plants')
    fuel_assemblies: Mapped[list['FuelAssembly']] = relationship('FuelAssembly', back_populates='plant')

class FuelAssembly(Base):
    __tablename__ = 'FUEL_ASSEMBLY'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    FA_name: Mapped[str] = mapped_column(String(8), nullable=False)
    FA_mass: Mapped[float] = mapped_column(nullable=False)
    FA_length_ft: Mapped[int] = mapped_column(nullable=False)
    FA_manufacturing_year: Mapped[int] = mapped_column(nullable=False)
    FA_BUp: Mapped[float] = mapped_column(nullable=False)
    reactor_design_id: Mapped[int] = mapped_column(ForeignKey('REACTOR_DESIGN.id'), nullable=False)
    plant_id: Mapped[int] = mapped_column(ForeignKey('PLANTS.id'), nullable=False)
    epoch_id: Mapped[int] = mapped_column(ForeignKey('EPOCHS.id'), nullable=False)
    introduction_year: Mapped[int] = mapped_column(nullable=False)
    reactor_design: Mapped['ReactorDesign'] = relationship('ReactorDesign', back_populates='fuel_assemblies')
    plant: Mapped['Plant'] = relationship('Plant', back_populates='fuel_assemblies')
    epoch: Mapped['Epoch'] = relationship('Epoch', back_populates='fuel_assemblies')

# Ensure the SQLAlchemy_ORM directory exists for the database file
script_dir = Path(__file__).resolve().parent
script_dir.mkdir(parents=True, exist_ok=True)

# Create SQLite database and tables
DB_PATH = script_dir / 'example_orm.db'
engine = create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)
engine.dispose()
print("Tables created successfully.")
