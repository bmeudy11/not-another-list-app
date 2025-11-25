import listReducer from './listReducer';
import * as constants from '../constants/index';

describe('listReducer', () => {
  const initialState = {
    list: [],
    showAddList: false,
    name: "",
    description: ""
  };

  it('should return initial state', () => {
    expect(listReducer(undefined, {})).toEqual(initialState);
  });

  it('should handle SET_LISTS with array', () => {
    const lists = [
      { id: 1, name: 'List 1', description: 'Desc 1', is_done: false },
      { id: 2, name: 'List 2', description: 'Desc 2', is_done: true }
    ];
    const action = {
      type: constants.SET_LISTS,
      payload: lists
    };
    const newState = listReducer(initialState, action);
    expect(newState.list).toEqual(lists);
    expect(newState.list.length).toBe(2);
  });

  it('should handle SET_LISTS with non-array payload as empty array', () => {
    const action = {
      type: constants.SET_LISTS,
      payload: null
    };
    const newState = listReducer(initialState, action);
    expect(newState.list).toEqual([]);
  });

  it('should handle SET_LISTS with object payload as empty array', () => {
    const action = {
      type: constants.SET_LISTS,
      payload: { id: 1, name: 'List' }
    };
    const newState = listReducer(initialState, action);
    expect(newState.list).toEqual([]);
  });

  it('should handle SWITCH_SHOW_ADD_LIST_FORM to true', () => {
    const action = {
      type: constants.SWITCH_SHOW_ADD_LIST_FORM,
      payload: true
    };
    const newState = listReducer(initialState, action);
    expect(newState.showAddList).toBe(true);
  });

  it('should handle SWITCH_SHOW_ADD_LIST_FORM to false', () => {
    const stateWithFormOpen = { ...initialState, showAddList: true };
    const action = {
      type: constants.SWITCH_SHOW_ADD_LIST_FORM,
      payload: false
    };
    const newState = listReducer(stateWithFormOpen, action);
    expect(newState.showAddList).toBe(false);
  });

  it('should handle SET_CREATE_LIST_NAME', () => {
    const action = {
      type: constants.SET_CREATE_LIST_NAME,
      payload: 'My New List'
    };
    const newState = listReducer(initialState, action);
    expect(newState.name).toBe('My New List');
  });

  it('should handle SET_CREATE_LIST_DESCRIPTION', () => {
    const action = {
      type: constants.SET_CREATE_LIST_DESCRIPTION,
      payload: 'This is a test list'
    };
    const newState = listReducer(initialState, action);
    expect(newState.description).toBe('This is a test list');
  });

  it('should preserve other properties when updating one', () => {
    const stateWithData = {
      ...initialState,
      name: 'Existing List',
      description: 'Existing Desc'
    };
    const action = {
      type: constants.SWITCH_SHOW_ADD_LIST_FORM,
      payload: true
    };
    const newState = listReducer(stateWithData, action);
    expect(newState.name).toBe('Existing List');
    expect(newState.description).toBe('Existing Desc');
    expect(newState.showAddList).toBe(true);
  });

  it('should return state for unknown action type', () => {
    const existingState = {
      list: [{ id: 1, name: 'Test' }],
      showAddList: true,
      name: "Test List",
      description: "Test Desc"
    };
    const action = { type: 'UNKNOWN_ACTION' };
    const newState = listReducer(existingState, action);
    expect(newState).toEqual(existingState);
  });
});
