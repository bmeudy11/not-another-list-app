"""
Backend Unit Tests
Tests for backend API models, CRUD operations, and database functionality
"""

import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import models
import schemas
import crud
from database import Base


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
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
#  Integration Tests    #
#########################

def test_user_list_relationship(db_session):
    """Test relationship between User and List"""
    # Create user
    user = models.User(username="listuser", password="pass", access_id="access")
    db_session.add(user)
    db_session.commit()
    
    # Create multiple lists for the user
    list1 = models.List(user_id=user.id, name="List 1", description="First", is_done=False)
    list2 = models.List(user_id=user.id, name="List 2", description="Second", is_done=True)
    db_session.add_all([list1, list2])
    db_session.commit()
    
    # Query lists by user_id
    lists = db_session.query(models.List).filter(models.List.user_id == user.id).all()
    
    assert len(lists) == 2
    assert lists[0].user_id == user.id
    assert lists[1].user_id == user.id


def test_list_task_relationship(db_session):
    """Test relationship between List and Task"""
    # Create user and list
    user = models.User(username="taskuser", password="pass", access_id="access")
    db_session.add(user)
    db_session.commit()
    
    list_item = models.List(user_id=user.id, name="Task List", description="Desc", is_done=False)
    db_session.add(list_item)
    db_session.commit()
    
    # Create multiple tasks for the list
    task1 = models.Task(list_id=list_item.id, name="Task 1", description="First task", is_done=False)
    task2 = models.Task(list_id=list_item.id, name="Task 2", description="Second task", is_done=True)
    db_session.add_all([task1, task2])
    db_session.commit()
    
    # Query tasks by list_id
    tasks = db_session.query(models.Task).filter(models.Task.list_id == list_item.id).all()
    
    assert len(tasks) == 2
    assert tasks[0].list_id == list_item.id
    assert tasks[1].list_id == list_item.id


def test_cascade_delete_list_tasks(db_session):
    """Test that tasks handle list deletion (SET NULL)"""
    # Create user, list, and task
    user = models.User(username="cascadeuser", password="pass", access_id="access")
    db_session.add(user)
    db_session.commit()
    
    list_item = models.List(user_id=user.id, name="Delete Me", description="Desc", is_done=False)
    db_session.add(list_item)
    db_session.commit()
    
    task = models.Task(list_id=list_item.id, name="Orphan Task", description="Desc", is_done=False)
    db_session.add(task)
    db_session.commit()
    
    task_id = task.id
    
    # Delete the list
    db_session.delete(list_item)
    db_session.commit()
    
    # Task should still exist but with NULL list_id
    orphaned_task = db_session.query(models.Task).filter(models.Task.id == task_id).first()
    assert orphaned_task is not None
    assert orphaned_task.list_id is None


def test_unique_usernames(db_session):
    """Test that duplicate usernames can be created (no unique constraint in schema)"""
    user1 = models.User(username="duplicate", password="pass1", access_id="id1")
    user2 = models.User(username="duplicate", password="pass2", access_id="id2")
    
    db_session.add(user1)
    db_session.commit()
    
    db_session.add(user2)
    db_session.commit()
    
    # Both should exist since there's no unique constraint
    users = db_session.query(models.User).filter(models.User.username == "duplicate").all()
    assert len(users) == 2


#########################
#   Edge Case Tests     #
#########################

def test_empty_optional_fields(db_session):
    """Test creating models with empty optional fields"""
    user = models.User(username="", password="", access_id="")
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.username == ""


def test_null_list_id_in_task(db_session):
    """Test creating task without list_id"""
    task = models.Task(list_id=None, name="Orphan", description="No list", is_done=False)
    db_session.add(task)
    db_session.commit()
    
    assert task.id is not None
    assert task.list_id is None


def test_boolean_task_status(db_session):
    """Test task status toggles correctly"""
    user = models.User(username="statususer", password="pass", access_id="id")
    db_session.add(user)
    db_session.commit()
    
    list_item = models.List(user_id=user.id, name="List", description="D", is_done=False)
    db_session.add(list_item)
    db_session.commit()
    
    task = models.Task(list_id=list_item.id, name="Toggle", description="D", is_done=False)
    db_session.add(task)
    db_session.commit()
    
    assert task.is_done is False
    
    # Toggle status
    task.is_done = True
    db_session.commit()
    
    # Retrieve and verify
    updated_task = db_session.query(models.Task).filter(models.Task.id == task.id).first()
    assert updated_task.is_done is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
