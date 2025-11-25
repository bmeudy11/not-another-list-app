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

  it('should have lists state', () => {
    const store = configureStore();
    const state = store.getState();
    expect(state.lists).toBeDefined();
  });

  it('should have tasks state', () => {
    const store = configureStore();
    const state = store.getState();
    expect(state.tasks).toBeDefined();
  });

  it('should initialize with correct default state', () => {
    const store = configureStore();
    const state = store.getState();
    
    expect(state.login.accessId).toBeUndefined();
    expect(state.lists.list).toEqual([]);
    expect(state.lists.showAddList).toBe(false);
    expect(state.tasks.tasks).toEqual([]);
    expect(state.tasks.showAddTaskForm).toBe(false);
  });

  it('should allow dispatching actions', () => {
    const store = configureStore();
    expect(() => {
      store.dispatch({ type: 'TEST_ACTION' });
    }).not.toThrow();
  });
});
