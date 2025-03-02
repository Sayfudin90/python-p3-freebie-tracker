from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    # Relationship to Freebie
    freebies = relationship('Freebie', back_populates='company')
    
    # Relationship to Dev through Freebie (many-to-many)
    devs = relationship(
        'Dev',
        secondary='freebies',
        back_populates='companies',
        viewonly=True
    )
    
    def give_freebie(self, dev, item_name, value):
        """
        Creates a new Freebie instance associated with this company and the given dev.
        
        Args:
            dev: An instance of the Dev class
            item_name: String representing the freebie's name
            value: Integer representing the freebie's value
            
        Returns:
            The newly created Freebie instance
        """
        freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        return freebie
    
    @classmethod
    def oldest_company(cls):
        """
        Returns the Company instance with the earliest founding year.
        
        Returns:
            Company: The company with the earliest founding year
        """
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine
        
        engine = create_engine('sqlite:///freebies.db')
        session = Session(engine)
        
        oldest = session.query(cls).order_by(cls.founding_year).first()
        session.close()
        
        return oldest
    
    def __repr__(self):
        return f'<Company {self.name}>'


class Dev(Base):
    __tablename__ = 'devs'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    # Relationship to Freebie
    freebies = relationship('Freebie', back_populates='dev')
    
    # Relationship to Company through Freebie (many-to-many)
    companies = relationship(
        'Company', 
        secondary='freebies',
        back_populates='devs',
        viewonly=True
    )
    
    def received_one(self, item_name):
        """
        Checks if any of the freebies associated with the dev has the given item_name.
        
        Args:
            item_name: String representing the item name to check for
            
        Returns:
            Bool: True if the dev has a freebie with the given item_name, False otherwise
        """
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False
    
    def give_away(self, dev, freebie):
        """
        Gives a freebie to another dev if the freebie belongs to this dev.
        
        Args:
            dev: An instance of the Dev class who will receive the freebie
            freebie: An instance of the Freebie class to be given away
            
        Returns:
            None
        """
        if freebie in self.freebies:
            freebie.dev = dev
    
    def __repr__(self):
        return f'<Dev {self.name}>'


class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    
    # Foreign keys
    dev_id = Column(Integer(), ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)
    
    # Relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')
    
    def print_details(self):
        """
        Returns a formatted string with details about the freebie.
        
        Returns:
            String: Formatted string with dev name, freebie item_name, and company name
        """
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'