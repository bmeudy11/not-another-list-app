import * as constants from '../constants/index';

export function setAccessId(accessId) {
  return {
    type: constants.SET_ACCESS_ID,
    payload: accessId
  };
}

export function setUsername(username) {
  return {
    type: constants.SET_USERNAME,
    payload: username
  };
}

export function setPassword(password) {
  return {
    type: constants.SET_PASSWORD,
    payload: password
  };
}

export function loginSuccess(username, accessId) {
  return {
    type: constants.LOGIN_SUCCESS,
    payload: {
      username,
      accessId
    }
  };
}

export function loginFailed() {

}
