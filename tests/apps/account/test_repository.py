import os
import pytest
import json
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import select


# Mock data
EMAIL = "test@naver.com"
PASSWORD = "test1234"
GENDER = "male"
AGE = "20대"

# DB connection
account_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
apps_path = os.path.abspath(os.path.join(account_path, os.path.pardir))
conf_path = os.path.abspath(os.path.join(apps_path, "conf"))
conf_file = os.path.abspath(os.path.join(conf_path, "conf.json"))
with open(conf_file, "rt") as f:
    conf = json.load(f)
POSTGRE_CONNECTION = conf["postgre"]


# db_manager.py
class PostgreManager:
    def __init__(self) -> None:
        user: str = POSTGRE_CONNECTION["user"]
        password: str = POSTGRE_CONNECTION["password"]
        host: str = POSTGRE_CONNECTION["host"]
        port: str = POSTGRE_CONNECTION["port"]
        db: str = POSTGRE_CONNECTION["db"]
        DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{db}'
        self.engine = create_engine(
            DATABASE_URL, pool_size=5, pool_recycle=100, max_overflow=10
        )

    def get_session(self):
        return Session(self.engine)


# model.py
class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = 'user_account'

    seq = Column(Integer, primary_key=True)
    email = Column(String(500), nullable=False)
    password = Column(String(500), nullable=False)
    gender = Column(String(20), nullable=False)
    age = Column(String(200), nullable=False)
    generate_count = Column(Integer, nullable=False)


@pytest.fixture
def mockup():
    yield {
        "email": EMAIL,
        "password": PASSWORD,
        "gender": GENDER,
        "age": AGE
    }


@pytest.fixture
def session():
    yield PostgreManager().get_session()


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_account_repository_can_insert_user_account(mockup, session):
    # given : 유효한 유저 정보
    obj = Account(
        email=mockup["email"],
        password=mockup["password"],
        gender=mockup["gender"],
        age=mockup["age"],
        generate_count=0
    )

    # when : DB에 데이터 입력 요청
    with session:
        session.add(obj)
        session.commit()

    # then : 입력완료되면 email 반환

    # then : 데이터 정상적으로 입력 되었는지 확인
    with session:
        sql = select(Account).filter(Account.email == EMAIL)
        obj = session.execute(sql).scalar_one()
        result = {
            "email": obj.email,
            "password": obj.password,
            "gender": obj.gender,
            "age": obj.age,
            "generate_count": obj.generate_count
        }

    assert result["email"] == EMAIL
    assert result["password"] == PASSWORD
    assert result["gender"] == GENDER
    assert result["age"] == AGE
    assert result["generate_count"] == 0


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_account_repository_cannot_get_user_account(session):
    # given : DB에 없는 조회할 유저 ID
    WRONG_EMAIL = "wrong_email"
    # then : NoRsultFound error
    with pytest.raises(NoResultFound):
        with session:
            # when : DB에 데이터 조회 요청
            sql = select(Account).filter(Account.email == WRONG_EMAIL)
            session.execute(sql).scalar_one()


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_account_repository_can_update_user_account():
    # given : 변경할 유저 정보(ID제외)

    # when : DB에 데이터 변경 요청

    # then : 변경된 데이터 확인
    pass


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_account_respository_can_get_all_user_account():
    # given :

    # when : DB에 데이터 전체 조회 요청

    # then : 조회된 데이터 확인
    pass


@pytest.mark.asyncio(3)
async def test_account_repository_cannot_get_all_user_account():
    # given : 테이블에 아무 데이터도 없을 때

    # when : DB 데이터 조회 요청

    # then : 빈 리스트 출력
    pass
