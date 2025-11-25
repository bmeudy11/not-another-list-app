import * as constants from './index';

describe('Constants', () => {
  describe('Login Actions', () => {
    it('should export SET_ACCESS_ID constant', () => {
      expect(constants.SET_ACCESS_ID).toBe('SET_ACCESS_ID');
    });

    it('should export SET_USERNAME constant', () => {
      expect(constants.SET_USERNAME).toBe('SET_USERNAME');
    });

    it('should export SET_PASSWORD constant', () => {
      expect(constants.SET_PASSWORD).toBe('SET_PASSWORD');
    });

    it('should export LOGIN_SUCCESS constant', () => {
      expect(constants.LOGIN_SUCCESS).toBe('LOGIN');
    });
  });

  describe('List Actions', () => {
    it('should export SET_LISTS constant', () => {
      expect(constants.SET_LISTS).toBe('SET_LISTS');
    });

    it('should export SWITCH_SHOW_ADD_LIST_FORM constant', () => {
      expect(constants.SWITCH_SHOW_ADD_LIST_FORM).toBe('SWITCH_SHOW_ADD_LIST_FORM');
    });

    it('should export SET_CREATE_LIST_NAME constant', () => {
      expect(constants.SET_CREATE_LIST_NAME).toBe('SET_CREATE_LIST_NAME');
    });

    it('should export SET_CREATE_LIST_DESCRIPTION constant', () => {
      expect(constants.SET_CREATE_LIST_DESCRIPTION).toBe('SET_CREATE_LIST_DESCRIPTION');
    });
  });

  describe('Task Actions', () => {
    it('should export SET_TASKS constant', () => {
      expect(constants.SET_TASKS).toBe('SET_TASKS');
    });

    it('should export SET_TASKS_LIST_NAME constant', () => {
      expect(constants.SET_TASKS_LIST_NAME).toBe('SET_TASKS_LIST_NAME');
    });

    it('should export SET_TASKS_LIST_ID constant', () => {
      expect(constants.SET_TASKS_LIST_ID).toBe('SET_TASKS_LIST_ID');
    });

    it('should export SWITCH_SHOW_ADD_TASK_FORM constant', () => {
      expect(constants.SWITCH_SHOW_ADD_TASK_FORM).toBe('SWITCH_SHOW_ADD_TASK_FORM');
    });

    it('should export SET_CREATE_TASK_NAME constant', () => {
      expect(constants.SET_CREATE_TASK_NAME).toBe('SET_CREATE_TASK_NAME');
    });

    it('should export SET_CREATE_TASK_DESCRIPTION constant', () => {
      expect(constants.SET_CREATE_TASK_DESCRIPTION).toBe('SET_CREATE_TASK_DESCRIPTION');
    });

    it('should export SWITCH_SET_TASK_IS_DONE constant', () => {
      expect(constants.SWITCH_SET_TASK_IS_DONE).toBe('SWITCH_SET_TASK_IS_DONE');
    });
  });

  describe('All constants', () => {
    it('should export all expected constants', () => {
      const expectedConstants = [
        'SET_ACCESS_ID',
        'SET_USERNAME',
        'SET_PASSWORD',
        'LOGIN_SUCCESS',
        'SET_LISTS',
        'SWITCH_SHOW_ADD_LIST_FORM',
        'SET_CREATE_LIST_NAME',
        'SET_CREATE_LIST_DESCRIPTION',
        'SET_TASKS',
        'SET_TASKS_LIST_NAME',
        'SET_TASKS_LIST_ID',
        'SWITCH_SHOW_ADD_TASK_FORM',
        'SET_CREATE_TASK_NAME',
        'SET_CREATE_TASK_DESCRIPTION',
        'SWITCH_SET_TASK_IS_DONE'
      ];

      expectedConstants.forEach(constantName => {
        expect(constants[constantName]).toBeDefined();
      });
    });

    it('should have unique constant values', () => {
      const values = Object.values(constants);
      const uniqueValues = new Set(values);
      expect(uniqueValues.size).toBe(values.length);
    });
  });
});
