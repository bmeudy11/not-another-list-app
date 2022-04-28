import { createStore, combineReducers, applyMiddleware } from 'redux';

// API Reducers
import thunk from 'redux-thunk';
import loginReducer from '../reducers/loginReducer';

// Page Reduces

// Component Reducers

// 3rd Parter

const rootReducer = combineReducers(
  {
    login: loginReducer,
  }
);
const configureStore = () => {
  return createStore(rootReducer, applyMiddleware(thunk));
};

export default configureStore;
