import * as constants from '../constants/index';

const initialState = {
  list: [],
  showAddList: false,
  name: "",
  description: ""
};
const listReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.SET_LISTS:
      return {
        ...state,
        list: Array.isArray(action.payload) ? action.payload : []
      };
    case constants.SWITCH_SHOW_ADD_LIST_FORM:
      return {
        ...state,
        showAddList: action.payload
      };
    case constants.SET_CREATE_LIST_NAME:
      return {
        ...state,
        name: action.payload
      };
    case constants.SET_CREATE_LIST_DESCRIPTION:
      return {
        ...state,
        description: action.payload
      };
    default:
      return state;
  }
};
export default listReducer;
