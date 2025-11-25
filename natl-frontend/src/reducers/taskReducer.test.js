import taskReducer from './taskReducer';
import * as constants from '../constants/index';

describe('taskReducer', () => {
  const initialState = {
    tasks: [],
    showAddTaskForm: false,
    name: "",
    description: "",
    taskListName: "",
    taskListId: ""
  };

  it('should return initial state', () => {
    expect(taskReducer(undefined, {})).toEqual(initialState);
  });

  it('should handle SET_TASKS with array', () => {
    const tasks = [
      { id: 1, name: 'Task 1', description: 'Desc 1', is_done: false },
      { id: 2, name: 'Task 2', description: 'Desc 2', is_done: true }
    ];
    const action = {
      type: constants.SET_TASKS,
      payload: tasks
    };
    const newState = taskReducer(initialState, action);
    expect(newState.tasks).toEqual(tasks);
    expect(newState.tasks.length).toBe(2);
  });

  it('should handle SET_TASKS with non-array payload as empty array', () => {
    const action = {
      type: constants.SET_TASKS,
      payload: null
    };
    const newState = taskReducer(initialState, action);
    expect(newState.tasks).toEqual([]);
  });

  it('should handle SET_TASKS with object payload as empty array', () => {
    const action = {
      type: constants.SET_TASKS,
      payload: { id: 1, name: 'Task' }
    };
    const newState = taskReducer(initialState, action);
    expect(newState.tasks).toEqual([]);
  });

  it('should handle SET_TASKS_LIST_NAME', () => {
    const action = {
      type: constants.SET_TASKS_LIST_NAME,
      payload: 'My Task List'
    };
    const newState = taskReducer(initialState, action);
    expect(newState.taskListName).toBe('My Task List');
  });

  it('should handle SET_TASKS_LIST_ID', () => {
    const action = {
      type: constants.SET_TASKS_LIST_ID,
      payload: '123'
    };
    const newState = taskReducer(initialState, action);
    expect(newState.taskListId).toBe('123');
  });

  it('should handle SWITCH_SHOW_ADD_TASK_FORM to true', () => {
    const action = {
      type: constants.SWITCH_SHOW_ADD_TASK_FORM,
      payload: true
    };
    const newState = taskReducer(initialState, action);
    expect(newState.showAddTaskForm).toBe(true);
  });

  it('should handle SWITCH_SHOW_ADD_TASK_FORM to false', () => {
    const stateWithFormOpen = { ...initialState, showAddTaskForm: true };
    const action = {
      type: constants.SWITCH_SHOW_ADD_TASK_FORM,
      payload: false
    };
    const newState = taskReducer(stateWithFormOpen, action);
    expect(newState.showAddTaskForm).toBe(false);
  });

  it('should handle SWITCH_SET_TASK_IS_DONE', () => {
    const action = {
      type: constants.SWITCH_SET_TASK_IS_DONE,
      payload: true
    };
    const newState = taskReducer(initialState, action);
    expect(newState.isDone).toBe(true);
  });

  it('should handle SET_CREATE_TASK_NAME', () => {
    const action = {
      type: constants.SET_CREATE_TASK_NAME,
      payload: 'My New Task'
    };
    const newState = taskReducer(initialState, action);
    expect(newState.name).toBe('My New Task');
  });

  it('should handle SET_CREATE_TASK_DESCRIPTION', () => {
    const action = {
      type: constants.SET_CREATE_TASK_DESCRIPTION,
      payload: 'This is a test task'
    };
    const newState = taskReducer(initialState, action);
    expect(newState.description).toBe('This is a test task');
  });

  it('should preserve other properties when updating one', () => {
    const stateWithData = {
      ...initialState,
      name: 'Existing Task',
      description: 'Existing Desc',
      taskListId: '456'
    };
    const action = {
      type: constants.SET_TASKS_LIST_NAME,
      payload: 'New List Name'
    };
    const newState = taskReducer(stateWithData, action);
    expect(newState.name).toBe('Existing Task');
    expect(newState.description).toBe('Existing Desc');
    expect(newState.taskListId).toBe('456');
    expect(newState.taskListName).toBe('New List Name');
  });

  it('should return state for unknown action type', () => {
    const existingState = {
      tasks: [{ id: 1, name: 'Test Task' }],
      showAddTaskForm: true,
      name: "Test",
      description: "Test Desc",
      taskListName: "List",
      taskListId: "789"
    };
    const action = { type: 'UNKNOWN_ACTION' };
    const newState = taskReducer(existingState, action);
    expect(newState).toEqual(existingState);
  });

  it('should handle multiple state updates', () => {
    let state = initialState;
    
    state = taskReducer(state, {
      type: constants.SET_TASKS_LIST_ID,
      payload: '100'
    });
    
    state = taskReducer(state, {
      type: constants.SET_TASKS_LIST_NAME,
      payload: 'Project Tasks'
    });
    
    state = taskReducer(state, {
      type: constants.SET_CREATE_TASK_NAME,
      payload: 'First Task'
    });
    
    expect(state.taskListId).toBe('100');
    expect(state.taskListName).toBe('Project Tasks');
    expect(state.name).toBe('First Task');
  });
});
