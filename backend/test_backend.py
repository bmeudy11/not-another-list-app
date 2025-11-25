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
    
    assert "Access ID is not specified" in exc_info.value.msg


def test_create_list_no_access_id(db_session):
    """Test that creating list without access_id raises exception"""
    from DefaultException import DefaultException
    
    with pytest.raises(DefaultException) as exc_info:
        crud.create_list(db_session, access_id=None, name="Test", description="Desc", is_done=False)
    
    assert "Access ID is not specified" in exc_info.value.msg


def test_delete_list_no_access_id(db_session):
    """Test that deleting list without access_id raises exception"""
    from DefaultException import DefaultException
    
    with pytest.raises(DefaultException) as exc_info:
        crud.delete_list(db_session, access_id=None, id="1", name="Test")
    
    assert "Access ID is not specified" in exc_info.value.msg


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


def test_get_list_by_id_not_found(db_session):
    """Test retrieving non-existent list by ID returns empty list"""
    result = crud.get_list_by_id(db_session, "999999")
    assert len(result) == 0


def test_delete_list_by_id_not_found(db_session):
    """Test deleting non-existent list returns False"""
    user_data = schemas.UserCreate(username="testuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    result = crud.delete_list(db_session, user.access_id, id="999999", name=None)
    assert result is False


def test_delete_list_by_name_not_found(db_session):
    """Test deleting non-existent list by name returns False"""
    user_data = schemas.UserCreate(username="testuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    result = crud.delete_list(db_session, user.access_id, id=None, name="NonExistent")
    assert result is False


def test_get_task_with_zero_list_id(db_session):
    """Test get_task with list_id=0 returns tasks by id instead"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    created_task = crud.create_task(db_session, user.access_id, list_id, "Task", "Desc", False)
    
    # When list_id=0, it should search by task id
    tasks = crud.get_task(db_session, user.access_id, id=created_task.id, list_id=0)
    assert len(tasks) == 1
    assert tasks[0].id == created_task.id


def test_delete_task_not_found(db_session):
    """Test deleting non-existent task returns False"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    result = crud.delete_task(db_session, user.access_id, 999999)
    assert result is False


def test_update_list_is_done_toggle(db_session):
    """Test toggling list is_done status multiple times"""
    user_data = schemas.UserCreate(username="listuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "Toggle", "Desc", False)
    list_id = created_list[0]['id']
    
    # Toggle to True
    crud.update_list_is_done(db_session, user.access_id, list_id, True)
    updated = crud.get_list_by_id(db_session, list_id)
    assert updated[0]['is_done'] is True
    
    # Toggle back to False
    crud.update_list_is_done(db_session, user.access_id, list_id, False)
    updated = crud.get_list_by_id(db_session, list_id)
    assert updated[0]['is_done'] is False


def test_update_task_is_done_toggle(db_session):
    """Test toggling task is_done status multiple times"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    created_task = crud.create_task(db_session, user.access_id, list_id, "Task", "Desc", False)
    
    # Toggle to True
    crud.update_task_is_done(db_session, user.access_id, created_task.id, True)
    updated = crud.get_task_by_id(db_session, created_task.id)
    assert updated.is_done is True
    
    # Toggle back to False
    crud.update_task_is_done(db_session, user.access_id, created_task.id, False)
    updated = crud.get_task_by_id(db_session, created_task.id)
    assert updated.is_done is False


#########################
# Additional Schema Tests
#########################

def test_list_get_schema():
    """Test ListGet schema"""
    list_get = schemas.ListGet(access_id="test123", id="1")
    assert list_get.access_id == "test123"
    assert list_get.id == "1"


def test_list_get_schema_no_id():
    """Test ListGet schema without id"""
    list_get = schemas.ListGet(access_id="test123")
    assert list_get.access_id == "test123"
    assert list_get.id is None


def test_list_create_schema():
    """Test ListCreate schema"""
    list_create = schemas.ListCreate(
        access_id="test123",
        name="My List",
        description="Description",
        is_done=True
    )
    assert list_create.access_id == "test123"
    assert list_create.name == "My List"
    assert list_create.description == "Description"
    assert list_create.is_done is True


def test_list_create_schema_default_is_done():
    """Test ListCreate schema with default is_done"""
    list_create = schemas.ListCreate(
        access_id="test123",
        name="My List",
        description="Description"
    )
    assert list_create.is_done is False


def test_list_delete_schema():
    """Test ListDelete schema"""
    list_delete = schemas.ListDelete(access_id="test123", id="1", name="Test")
    assert list_delete.access_id == "test123"
    assert list_delete.id == "1"
    assert list_delete.name == "Test"


def test_list_return_schema():
    """Test ListReturn schema"""
    list_return = schemas.ListReturn(
        id=1,
        name="Test",
        description="Desc",
        is_done=False
    )
    assert list_return.id == 1
    assert list_return.name == "Test"
    assert list_return.description == "Desc"
    assert list_return.is_done is False


def test_task_get_schema():
    """Test TaskGet schema"""
    task_get = schemas.TaskGet(access_id="test123", id=1, list_id=2)
    assert task_get.access_id == "test123"
    assert task_get.id == 1
    assert task_get.list_id == 2


def test_task_get_schema_defaults():
    """Test TaskGet schema with defaults"""
    task_get = schemas.TaskGet(access_id="test123")
    assert task_get.access_id == "test123"
    assert task_get.id is None
    assert task_get.list_id is None


def test_task_create_schema():
    """Test TaskCreate schema"""
    task_create = schemas.TaskCreate(
        access_id="test123",
        list_id=1,
        name="Task",
        description="Desc",
        is_done=True
    )
    assert task_create.access_id == "test123"
    assert task_create.list_id == 1
    assert task_create.name == "Task"
    assert task_create.description == "Desc"
    assert task_create.is_done is True


def test_task_create_schema_default_is_done():
    """Test TaskCreate schema with default is_done"""
    task_create = schemas.TaskCreate(
        access_id="test123",
        list_id=1,
        name="Task",
        description="Desc"
    )
    assert task_create.is_done is False


def test_task_delete_schema():
    """Test TaskDelete schema"""
    task_delete = schemas.TaskDelete(access_id="test123", id=1)
    assert task_delete.access_id == "test123"
    assert task_delete.id == 1


def test_task_is_done_schema():
    """Test TaskIsDone schema"""
    task_is_done = schemas.TaskIsDone(access_id="test123", id=1, is_done=True)
    assert task_is_done.access_id == "test123"
    assert task_is_done.id == 1
    assert task_is_done.is_done is True


def test_task_is_done_schema_default():
    """Test TaskIsDone schema with default"""
    task_is_done = schemas.TaskIsDone(access_id="test123", id=1)
    assert task_is_done.access_id == "test123"
    assert task_is_done.id == 1
    assert task_is_done.is_done is False


def test_task_return_schema():
    """Test TaskReturn schema"""
    task_return = schemas.TaskReturn(
        id=1,
        list_id=2,
        name="Task",
        description="Desc",
        is_done=True
    )
    assert task_return.id == 1
    assert task_return.list_id == 2
    assert task_return.name == "Task"
    assert task_return.description == "Desc"
    assert task_return.is_done is True


def test_user_schema():
    """Test User schema"""
    user = schemas.User(id=1, username="testuser", access_id="access123")
    assert user.id == 1
    assert user.username == "testuser"
    assert user.access_id == "access123"


def test_logged_in_base_schema():
    """Test LoggedInBase schema"""
    logged_in = schemas.LoggedInBase(access_id="test123")
    assert logged_in.access_id == "test123"


def test_user_base_schema():
    """Test UserBase schema"""
    user_base = schemas.UserBase(username="testuser")
    assert user_base.username == "testuser"


#########################
# More Coverage Tests   #
#########################

def test_multiple_tasks_same_list(db_session):
    """Test creating multiple tasks for the same list"""
    user_data = schemas.UserCreate(username="multitask", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    # Create 10 tasks
    for i in range(10):
        crud.create_task(db_session, user.access_id, list_id, f"Task {i}", f"Desc {i}", i % 2 == 0)
    
    tasks = crud.get_task(db_session, user.access_id, id=None, list_id=list_id)
    assert len(tasks) == 10


def test_get_task_by_id_not_found(db_session):
    """Test get_task_by_id with non-existent id returns None"""
    result = crud.get_task_by_id(db_session, 999999)
    assert result is None


def test_get_user_by_access_id_not_found(db_session):
    """Test get_user_by_access_id with non-existent id returns None"""
    result = crud.get_user_by_access_id(db_session, "nonexistent")
    assert result is None


def test_get_user_by_id_not_found(db_session):
    """Test get_user_by_id with non-existent id returns None"""
    result = crud.get_user_by_id(db_session, "999999")
    assert result is None


def test_create_list_with_is_done_true(db_session):
    """Test creating list with is_done=True"""
    user_data = schemas.UserCreate(username="doneuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    result = crud.create_list(db_session, user.access_id, "Done List", "Already done", True)
    
    assert len(result) == 1
    assert result[0]['is_done'] is True


def test_create_task_with_is_done_true(db_session):
    """Test creating task with is_done=True"""
    user_data = schemas.UserCreate(username="donetask", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    task = crud.create_task(db_session, user.access_id, list_id, "Done Task", "Already done", True)
    
    assert task.is_done is True


def test_format_list_empty(db_session):
    """Test format_list with empty list"""
    formatted = crud.format_list(db_session, [])
    assert len(formatted) == 0


def test_task_with_long_description(db_session):
    """Test creating task with long description"""
    user_data = schemas.UserCreate(username="longdesc", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    long_desc = "A" * 250  # Long but within VARCHAR(255)
    task = crud.create_task(db_session, user.access_id, list_id, "Task", long_desc, False)
    
    assert task.description == long_desc


def test_list_with_long_description(db_session):
    """Test creating list with long description"""
    user_data = schemas.UserCreate(username="longlist", password="pass")
    user = crud.create_user(db_session, user_data)
    
    long_desc = "B" * 250  # Long but within VARCHAR(255)
    result = crud.create_list(db_session, user.access_id, "List", long_desc, False)
    
    assert result[0]['description'] == long_desc


def test_multiple_users_separate_lists(db_session):
    """Test that multiple users have separate lists"""
    user1 = crud.create_user(db_session, schemas.UserCreate(username="user1", password="pass1"))
    user2 = crud.create_user(db_session, schemas.UserCreate(username="user2", password="pass2"))
    
    # User1 creates lists
    crud.create_list(db_session, user1.access_id, "User1 List", "Desc", False)
    
    # User2 creates lists
    crud.create_list(db_session, user2.access_id, "User2 List", "Desc", False)
    
    # Each user should only see their own list
    user1_lists = crud.get_list(db_session, user1.access_id)
    user2_lists = crud.get_list(db_session, user2.access_id)
    
    assert len(user1_lists) == 1
    assert len(user2_lists) == 1
    assert user1_lists[0]['name'] == "User1 List"
    assert user2_lists[0]['name'] == "User2 List"


def test_get_task_none_list_id(db_session):
    """Test get_task with None list_id searches by task id"""
    user_data = schemas.UserCreate(username="taskuser", password="pass")
    user = crud.create_user(db_session, user_data)
    
    created_list = crud.create_list(db_session, user.access_id, "List", "Desc", False)
    list_id = created_list[0]['id']
    
    task1 = crud.create_task(db_session, user.access_id, list_id, "Task1", "Desc", False)
    task2 = crud.create_task(db_session, user.access_id, list_id, "Task2", "Desc", False)
    
    # Get specific task by id with None list_id
    tasks = crud.get_task(db_session, user.access_id, id=task1.id, list_id=None)
    assert len(tasks) == 1
    assert tasks[0].id == task1.id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
