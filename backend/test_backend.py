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


#########################
#    List CRUD Tests    #
#########################

def test_create_list(db_session):
    """Test list creation"""
    user_data = schemas.UserCreate(username="listuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    result = crud.create_list(
        db_session,
        access_id=user.access_id,
        name="My List",
        description="My Description",
        is_done=False
    )
    
    assert len(result) == 1
    assert result[0]['name'] == "My List"
    assert result[0]['description'] == "My Description"
    assert result[0]['is_done'] is False
    assert result[0]['user_id'] == user.id


def test_get_list(db_session):
    """Test retrieving lists for a user"""
    user_data = schemas.UserCreate(username="listuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    # Create multiple lists
    crud.create_list(db_session, user.access_id, "List 1", "Desc 1", False)
    crud.create_list(db_session, user.access_id, "List 2", "Desc 2", True)
    
    lists = crud.get_list(db_session, user.access_id)
    
    assert len(lists) == 2
    assert lists[0]['name'] == "List 1"
    assert lists[1]['name'] == "List 2"


def test_get_list_by_id(db_session):
    """Test retrieving list by ID"""
    user_data = schemas.UserCreate(username="listuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "Test List", "Desc", False)
    list_id = created_list[0]['id']
    
    found_lists = crud.get_list_by_id(db_session, list_id)
    
    assert len(found_lists) == 1
    assert found_lists[0]['id'] == list_id
    assert found_lists[0]['name'] == "Test List"


def test_delete_list_by_id(db_session):
    """Test deleting list by ID"""
    user_data = schemas.UserCreate(username="listuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "Delete Me", "Desc", False)
    list_id = created_list[0]['id']
    
    result = crud.delete_list(db_session, user.access_id, id=list_id, name=None)
    
    assert result is True
    
    # Verify list is deleted
    lists = crud.get_list(db_session, user.access_id)
    assert len(lists) == 0


def test_delete_list_by_name(db_session):
    """Test deleting list by name"""
    user_data = schemas.UserCreate(username="listuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    crud.create_list(db_session, user.access_id, "Delete Me", "Desc", False)
    
    result = crud.delete_list(db_session, user.access_id, id=None, name="Delete Me")
    
    assert result is True
    
    # Verify list is deleted
    lists = crud.get_list(db_session, user.access_id)
    assert len(lists) == 0


def test_update_list_is_done(db_session):
    """Test updating list completion status"""
    user_data = schemas.UserCreate(username="listuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "Todo", "Desc", False)
    list_id = created_list[0]['id']
    
    # Update to done
    crud.update_list_is_done(db_session, user.access_id, list_id, True)
    
    # Verify update
    updated_list = crud.get_list_by_id(db_session, list_id)
    assert updated_list[0]['is_done'] is True


def test_format_list(db_session):
    """Test list formatting function"""
    user = models.User(username="user", password="pass", access_id="id")
    db_session.add(user)
    db_session.commit()
    
    list1 = models.List(user_id=user.id, name="List 1", description="Desc 1", is_done=False)
    list2 = models.List(user_id=user.id, name="List 2", description="Desc 2", is_done=True)
    db_session.add_all([list1, list2])
    db_session.commit()
    
    formatted = crud.format_list(db_session, [list1, list2])
    
    assert len(formatted) == 2
    assert formatted[0]['name'] == "List 1"
    assert formatted[1]['name'] == "List 2"


#########################
#    Task CRUD Tests    #
#########################

def test_create_task(db_session):
    """Test task creation"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    task = crud.create_task(
        db_session,
        access_id=user.access_id,
        list_id=list_id,
        name="My Task",
        description="Task Description",
        is_done=False
    )
    
    assert task.id is not None
    assert task.list_id == list_id
    assert task.name == "My Task"
    assert task.description == "Task Description"
    assert task.is_done is False


def test_get_task_by_id(db_session):
    """Test retrieving task by ID"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    created_task = crud.create_task(db_session, user.access_id, list_id, "Task", "Desc", False)
    
    found_task = crud.get_task_by_id(db_session, created_task.id)
    
    assert found_task is not None
    assert found_task.id == created_task.id
    assert found_task.name == "Task"


def test_get_task_by_list_id(db_session):
    """Test retrieving tasks by list ID"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    # Create multiple tasks
    crud.create_task(db_session, user.access_id, list_id, "Task 1", "Desc 1", False)
    crud.create_task(db_session, user.access_id, list_id, "Task 2", "Desc 2", True)
    
    tasks = crud.get_task(db_session, user.access_id, id=None, list_id=list_id)
    
    assert len(tasks) == 2
    assert tasks[0].name == "Task 1"
    assert tasks[1].name == "Task 2"


def test_get_task_by_task_id(db_session):
    """Test retrieving tasks by task ID using get_task"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    created_task = crud.create_task(db_session, user.access_id, list_id, "Task", "Desc", False)
    
    tasks = crud.get_task(db_session, user.access_id, id=created_task.id, list_id=0)
    
    assert len(tasks) == 1
    assert tasks[0].id == created_task.id


def test_update_task_is_done(db_session):
    """Test updating task completion status"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    created_task = crud.create_task(db_session, user.access_id, list_id, "Task", "Desc", False)
    
    # Update to done
    crud.update_task_is_done(db_session, user.access_id, created_task.id, True)
    
    # Verify update
    updated_task = crud.get_task_by_id(db_session, created_task.id)
    assert updated_task.is_done is True


def test_delete_task(db_session):
    """Test deleting task"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    created_task = crud.create_task(db_session, user.access_id, list_id, "Delete Me", "Desc", False)
    
    result = crud.delete_task(db_session, user.access_id, created_task.id)
    
    assert result is True
    
    # Verify task is deleted
    deleted_task = crud.get_task_by_id(db_session, created_task.id)
    assert deleted_task is None


#########################
#   Schema Tests        #
#########################

def test_user_create_schema():
    """Test UserCreate schema"""
    user = schemas.UserCreate(username="testuser", password="testpass")
    assert user.username == "testuser"
    assert user.password == "testpass"


def test_user_login_schema():
    """Test UserLogin schema"""
    login = schemas.UserLogin(username="testuser", password="testpass")
    assert login.username == "testuser"
    assert login.password == "testpass"


def test_user_delete_schema():
    """Test UserDelete schema"""
    delete = schemas.UserDelete(username="testuser", access_id="access123", password="pass")
    assert delete.username == "testuser"
    assert delete.access_id == "access123"
    assert delete.password == "pass"


#########################
#  Exception Tests      #
#########################

def test_get_list_no_access_id(db_session):
    """Test that getting list without access_id raises exception"""
    from DefaultException import DefaultException
    
    with pytest.raises(DefaultException) as exc_info:
        crud.get_list(db_session, access_id=None)
    
    assert "Access ID is not specified" in str(exc_info.value)


def test_create_list_no_access_id(db_session):
    """Test that creating list without access_id raises exception"""
    from DefaultException import DefaultException
    
    with pytest.raises(DefaultException) as exc_info:
        crud.create_list(db_session, access_id=None, name="Test", description="Desc", is_done=False)
    
    assert "Access ID is not specified" in str(exc_info.value)


def test_delete_list_no_access_id(db_session):
    """Test that deleting list without access_id raises exception"""
    from DefaultException import DefaultException
    
    with pytest.raises(DefaultException) as exc_info:
        crud.delete_list(db_session, access_id=None, id="1", name="Test")
    
    assert "Access ID is not specified" in str(exc_info.value)


#########################
#  Additional Coverage  #
#########################

def test_multiple_lists_same_user(db_session):
    """Test creating multiple lists for the same user"""
    user_data = schemas.UserCreate(username="multilist", password="pass")
    user = crud.create_user(db_session, user_data)
    
    for i in range(5):
        crud.create_list(db_session, user.access_id, f"List {i}", f"Desc {i}", i % 2 == 0)
    
    lists = crud.get_list(db_session, user.access_id)
    assert len(lists) == 5


def test_tasks_without_list(db_session):
    """Test creating task without list_id (orphaned task)"""
    user_data = schemas.UserCreate(username="orphan", password="pass")
    user = crud.create_user(db_session, user_data)
    
    task = crud.create_task(db_session, user.access_id, None, "Orphan", "No list", False)
    
    assert task.id is not None
    assert task.list_id is None


def test_empty_list_query(db_session):
    """Test querying lists when user has no lists"""
    user_data = schemas.UserCreate(username="nolist", password="pass")
    user = crud.create_user(db_session, user_data)
    
    lists = crud.get_list(db_session, user.access_id)
    assert len(lists) == 0


def test_user_with_special_characters(db_session):
    """Test creating user with special characters"""
    user_data = schemas.UserCreate(username="user@email.com", password="p@ss!w0rd#123")
    user = crud.create_user(db_session, user_data)
    
    assert user.username == "user@email.com"
    assert user.password == "p@ss!w0rd#123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
