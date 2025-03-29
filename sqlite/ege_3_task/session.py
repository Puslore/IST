from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from models import Base, Shop, Good, Operation


DATABASE_URL = 'sqlite:///database.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)


def create_shop(id: str, region: str, address: str):
    session = Session()

    try:        
        new_shop = Shop(shop_id=id, region=region,
                        address=address)
        session.add(new_shop)
        session.commit()
        session.refresh(new_shop)

    except Exception as err:
        session.rollback()
        print(f'Error while creating shop: {err}')

    finally:
        session.close()
    
    # return new_shop


def create_good(articul: int, group: str,
                            name: str, measure: int,
                            value: int, cost: int):
    session = Session()

    try:        
        new_good = Good(articul=articul,
                                    group=group,
                                    name=name,
                                    measure=measure,
                                    value=value,
                                    cost=cost)
        session.add(new_good)
        session.commit()
        session.refresh(new_good)

    except Exception as err:
        session.rollback()
        print(f'Error while creating good: {err}')

    finally:
        session.close()
    
    # return new_good


def create_operation(operation_id: int, date,
                            shop_id: str, articul: int,
                            amount: int, operation_type: str):
    session = Session()

    try:
        date = str(date).strip()
        new_operation = Operation(operation_id=operation_id,
                                    date=date,
                                    shop_id=shop_id,
                                    articul=articul,
                                    pacs_amount=amount,
                                    operation_type=operation_type)
        session.add(new_operation)
        session.commit()
        session.refresh(new_operation)

    except Exception as err:
        session.rollback()
        print(f'Error while creating operation: {err}')

    finally:
        session.close()
    
    # return new_operation


def get_shop(id: str = None):
    session = Session()
    
    try:
        if id is not None:
            shop = session.query(Shop).where(Shop.shop_id == id).first()
            
            return shop
        
        return session.query(Shop).all()

    
    except Exception as err:
        print(f'Error while getting shop: {str(err)}')
    
    finally:
        session.close()


def get_good(id: int = None):
    session = Session()

    try:
        if id is not None:
            good = session.query(Good).where(Good.articul == id).first()

            return good

        return session.query(Good).all()
    
    except Exception as err:
        print(f'Error while getting good: {str(err)}')
    
    finally:
        session.close()


def get_operation(id: int = None):
    session = Session()

    try:
        if id is not None:
            operation = session.query(Operation).where(Operation.operation_id == id).first()

            return operation
        
        return session.query(Operation).all()

    except Exception as err:
        print(f'Error while getting operation: {str(err)}')
    
    finally:
        session.close()
