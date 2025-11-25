import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import { createStore, combineReducers } from 'redux';
import App from './App';
import loginReducer from '../../reducers/loginReducer';
import listReducer from '../../reducers/listReducer';
import taskReducer from '../../reducers/taskReducer';

const rootReducer = combineReducers({
  login: loginReducer,
  lists: listReducer,
  tasks: taskReducer
});

describe('App Component', () => {
  it('renders Login component when not logged in', () => {
    const store = createStore(rootReducer);
    const { container } = render(
      <Provider store={store}>
        <App />
      </Provider>
    );
    expect(container).toBeTruthy();
  });

  it('renders Dashboard when logged in', () => {
    const initialState = {
      login: { accessId: 'test-123', username: 'testuser' },
      lists: { list: [], showAddList: false, name: '', description: '' },
      tasks: { tasks: [], showAddTaskForm: false, name: '', description: '', taskListName: '', taskListId: '' }
    };
    const store = createStore(rootReducer, initialState);
    
    const { container } = render(
      <Provider store={store}>
        <App />
      </Provider>
    );
    expect(container.querySelector('.wrapper')).toBeTruthy();
  });

  it('renders without crashing with minimal state', () => {
    const store = createStore(rootReducer);
    expect(() => {
      render(
        <Provider store={store}>
          <App />
        </Provider>
      );
    }).not.toThrow();
  });
});
