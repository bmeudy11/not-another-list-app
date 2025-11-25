import loginReducer from './loginReducer';
import * as constants from '../constants/index';

describe('loginReducer', () => {
  const initialState = {
    accessId: undefined
  };

  it('should return initial state', () => {
    expect(loginReducer(undefined, {})).toEqual(initialState);
  });

  it('should handle SET_ACCESS_ID', () => {
    const action = {
      type: constants.SET_ACCESS_ID,
      payload: 'test-access-id-123'
    };
    const newState = loginReducer(initialState, action);
    expect(newState.accessId).toBe('test-access-id-123');
  });

  it('should handle SET_USERNAME', () => {
    const action = {
      type: constants.SET_USERNAME,
      payload: 'testuser'
    };
    const newState = loginReducer(initialState, action);
    expect(newState.username).toBe('testuser');
  });

  it('should handle SET_PASSWORD', () => {
    const action = {
      type: constants.SET_PASSWORD,
      payload: 'testpass'
    };
    const newState = loginReducer(initialState, action);
    expect(newState.password).toBe('testpass');
  });

  it('should handle LOGIN_SUCCESS', () => {
    const action = {
      type: constants.LOGIN_SUCCESS,
      payload: {
        accessId: 'access-123',
        username: 'john'
      }
    };
    const newState = loginReducer(initialState, action);
    expect(newState.accessId).toBe('access-123');
    expect(newState.username).toBe('john');
  });

  it('should preserve existing state for unknown action', () => {
    const existingState = {
      accessId: 'existing-id',
      username: 'existinguser'
    };
    const action = { type: 'UNKNOWN_ACTION' };
    const newState = loginReducer(existingState, action);
    expect(newState).toEqual(existingState);
  });

  it('should maintain other properties when updating one', () => {
    const stateWithUsername = {
      accessId: undefined,
      username: 'user1'
    };
    const action = {
      type: constants.SET_PASSWORD,
      payload: 'newpass'
    };
    const newState = loginReducer(stateWithUsername, action);
    expect(newState.username).toBe('user1');
    expect(newState.password).toBe('newpass');
  });
});
