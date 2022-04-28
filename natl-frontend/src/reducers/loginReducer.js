import * as constants from '../constants/index';

const initialState = {
  accessId: undefined
};
const loginReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.SET_ACCESS_ID:
      return {
        ...state,
        accessId: action.payload
      };
    case constants.SET_USERNAME:
      return {
        ...state,
        username: action.payload
      };
    case constants.SET_PASSWORD:
      return {
        ...state,
        password: action.payload
      };
    case constants.LOGIN_SUCCESS:
      return {
        ...state,
        accessId: action.payload.accessId,
        username: action.payload.username
      };
    default:
      return state;
  }
};
export default loginReducer;
