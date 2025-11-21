import * as constants from '../constants/index';

const initialState = {
  tasks: [],
  showAddTaskForm: false,
  name: "",
  description: "",
  taskListName: "",
  taskListId: ""
};
const taskReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.SET_TASKS:
      return {
        ...state,
        tasks: Array.isArray(action.payload) ? action.payload : []
      };
    case constants.SET_TASKS_LIST_NAME:
      return {
        ...state,
        taskListName: action.payload
      };
    case constants.SET_TASKS_LIST_ID:
      return {
        ...state,
        taskListId: action.payload
      };
    case constants.SWITCH_SHOW_ADD_TASK_FORM:
      return {
        ...state,
        showAddTaskForm: action.payload
      };
    case constants.SWITCH_SET_TASK_IS_DONE:
      return {
        ...state,
        isDone: action.payload
      };
    case constants.SET_CREATE_TASK_NAME:
      return {
        ...state,
        name: action.payload
      };
    case constants.SET_CREATE_TASK_DESCRIPTION:
      return {
        ...state,
        description: action.payload
      };
    default:
      return state;
  }
};
export default taskReducer;
