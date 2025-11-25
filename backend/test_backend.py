"""
Backend Unit Tests
Tests for backend API models, CRUD operations, and database functionality
"""

import pytest
import sys
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Create a mock config file if it doesn't exist (for testing)
# database.py looks for config/dev.config.json relative to current directory
# So we need to create it in the backend directory, not backend/src
backend_path = os.path.dirname(__file__)
config_dir = os.path.join(backend_path, 'config')
config_file = os.path.join(config_dir, 'dev.config.json')

if not os.path.exists(config_file):
    os.makedirs(config_dir, exist_ok=True)
    mock_config = {
        "databaseName": "test_db",
        "databaseIp": "localhost",
        "databasePort": "3306",
        "databaseUsername": "test",
        "databasePassword": "test"
    }
    with open(config_file, 'w') as f:
        json.dump(mock_config, f)

# Also change to src directory so database.py can find the config
os.chdir(src_path)

import models
import schemas
import crud


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    # Use models.Base which has all the table definitions
    models.Base.metadata.create_all(bind=engine)
    yield engine
    models.Base.metadata.drop_all(bind=engine)
    # Clean up the test database file
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


#########################
#    Model Tests        #
#########################

def test_user_model_creation(db_session):
    """Test User model can be created"""
    user = models.User(
        username="testuser",
        password="testpass",
        access_id="test-access-id"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.password == "testpass"
    assert user.access_id == "test-access-id"


def test_list_model_creation(db_session):
    """Test List model can be created"""
    # Create a user first
    user = models.User(username="testuser", password="testpass", access_id="test-id")
    db_session.add(user)
    db_session.commit()
    
    # Create a list
    list_item = models.List(
        user_id=user.id,
        name="Test List",
        description="Test Description",
        is_done=False
    )
    db_session.add(list_item)
    db_session.commit()
    db_session.refresh(list_item)
    
    assert list_item.id is not None
    assert list_item.user_id == user.id
    assert list_item.name == "Test List"
    assert list_item.description == "Test Description"
    assert list_item.is_done is False


def test_task_model_creation(db_session):
    """Test Task model can be created"""
    # Create a user and list first
    user = models.User(username="testuser", password="testpass", access_id="test-id")
    db_session.add(user)
    db_session.commit()
    
    list_item = models.List(user_id=user.id, name="Test List", description="Desc", is_done=False)
    db_session.add(list_item)
    db_session.commit()
    
    # Create a task
    task = models.Task(
        list_id=list_item.id,
        name="Test Task",
        description="Test Task Description",
        is_done=False
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    assert task.id is not None
    assert task.list_id == list_item.id
    assert task.name == "Test Task"
    assert task.description == "Test Task Description"
    assert task.is_done is False


#########################
#    CRUD Tests         #
#########################

def test_create_user(db_session):
    """Test user creation through CRUD"""
    user_data = schemas.UserCreate(username="newuser", password="newpass")
    user = crud.create_user(db_session, user_data)
    
    assert user.id is not None
    assert user.username == "newuser"
    assert user.password == "newpass"
    assert user.access_id is not None
    assert len(user.access_id) > 0


def test_get_user_by_username(db_session):
    """Test retrieving user by username"""
    user_data = schemas.UserCreate(username="findme", password="mypass")
    created_user = crud.create_user(db_session, user_data)
    
    found_user = crud.get_user_by_username(db_session, "findme")
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.username == "findme"


def test_get_user_by_username_not_found(db_session):
    """Test retrieving non-existent user returns None"""
    found_user = crud.get_user_by_username(db_session, "nonexistent")
    assert found_user is None


def test_get_user_by_username_password(db_session):
    """Test retrieving user by username and password"""
    user_data = schemas.UserCreate(username="authuser", password="authpass")
    created_user = crud.create_user(db_session, user_data)
    
    found_user = crud.get_user_by_username_password(db_session, "authuser", "authpass")
    
    assert found_user is not None
    assert found_user.id == created_user.id


def test_get_user_by_username_password_wrong_password(db_session):
    """Test retrieving user with wrong password returns None"""
    user_data = schemas.UserCreate(username="authuser", password="authpass")
    crud.create_user(db_session, user_data)
    
    found_user = crud.get_user_by_username_password(db_session, "authuser", "wrongpass")
    assert found_user is None


def test_get_user_by_access_id(db_session):
    """Test retrieving user by access_id"""
    user_data = schemas.UserCreate(username="accessuser", password="pass")
    created_user = crud.create_user(db_session, user_data)
    
    found_user = crud.get_user_by_access_id(db_session, created_user.access_id)
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.username == "accessuser"


def test_get_user_by_id(db_session):
    """Test retrieving user by ID"""
    user_data = schemas.UserCreate(username="iduser", password="pass")
    created_user = crud.create_user(db_session, user_data)
    
    found_user = crud.get_user_by_id(db_session, created_user.id)
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.username == "iduser"


def test_delete_user_by_access_id_password(db_session):
    """Test deleting user by access_id and credentials"""
    user_data = schemas.UserCreate(username="deleteuser", password="deletepass")
    created_user = crud.create_user(db_session, user_data)
    
    result = crud.delete_user_by_access_id_password(
        db_session, 
        created_user.access_id, 
        "deleteuser", 
        "deletepass"
    )
    
    assert result is True
    
    # Verify user is deleted
    found_user = crud.get_user_by_id(db_session, created_user.id)
    assert found_user is None


def test_delete_user_wrong_credentials(db_session):
    """Test deleting user with wrong credentials fails"""
    user_data = schemas.UserCreate(username="keepuser", password="keeppass")
    created_user = crud.create_user(db_session, user_data)
    
    result = crud.delete_user_by_access_id_password(
        db_session, 
        created_user.access_id, 
        "keepuser", 
        "wrongpass"
    )
    
    assert result is False
    
    # Verify user still exists
    found_user = crud.get_user_by_id(db_session, created_user.id)
    assert found_user is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
