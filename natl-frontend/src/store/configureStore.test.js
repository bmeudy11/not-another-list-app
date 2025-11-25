import configureStore from './configureStore';

describe('configureStore', () => {
  it('should create a store', () => {
    const store = configureStore();
    expect(store).toBeDefined();
    expect(store.getState).toBeDefined();
    expect(store.dispatch).toBeDefined();
    expect(store.subscribe).toBeDefined();
  });

  it('should have login state', () => {
    const store = configureStore();
    const state = store.getState();
    expect(state.login).toBeDefined();
  });

  it('should have list state', () => {
    const store = configureStore();
    const state = store.getState();
    expect(state.list).toBeDefined();
  });

  it('should have task state', () => {
    const store = configureStore();
    const state = store.getState();
    expect(state.task).toBeDefined();
  });

  it('should initialize with correct default state', () => {
    const store = configureStore();
    const state = store.getState();
    
    expect(state.login.accessId).toBeUndefined();
    expect(state.list.list).toEqual([]);
    expect(state.list.showAddList).toBe(false);
    expect(state.task.tasks).toEqual([]);
    expect(state.task.showAddTaskForm).toBe(false);
  });

  it('should allow dispatching actions', () => {
    const store = configureStore();
    expect(() => {
      store.dispatch({ type: 'TEST_ACTION' });
    }).not.toThrow();
  });
});
