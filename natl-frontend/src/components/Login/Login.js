import React from 'react';
import './Login.css';

// Redux Related Imports
import { connect } from 'react-redux';
import * as actions from '../../actions/loginAction';

// Configuration
import config from '../../config/dev';

class LoginComponent extends React.Component {
    constructor(props) {
        super(props)
        this.login = this.login.bind(this);
        this.register = this.login.register(this);
    }

    async login() {
        const resp = await fetch(`${config.baseUrl}/user/login`, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: this.props.login.username,
                password: this.props.login.password
            })
        });
        const body = await resp.json();
        if (body.access_id !== undefined) {
            this.props.loginUser(this.props.login.username, body.access_id);
        } else {
            alert('Invalid Registration', body.errorMsg, [
                {
                    text: 'Cancel',
                    onPress: () => console.log('Cancel Pressed'),
                    style: 'cancel'
                },
                { text: 'OK', onPress: () => console.log('OK Pressed') }
            ]);
        }
        return body.access_token;
    }

    async register() {
        const resp = await fetch(`${config.baseUrl}/user/register`, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: this.props.login.username,
                password: this.props.login.password
            })
        });
        const body = await resp.json();
        if (body.access_id !== undefined) {
            this.props.loginUser(this.props.login.username, body.access_id);
        } else {
            alert('Invalid Registration', body.errorMsg, [
                {
                    text: 'Cancel',
                    onPress: () => console.log('Cancel Pressed'),
                    style: 'cancel'
                },
                { text: 'OK', onPress: () => console.log('OK Pressed') }
            ]);
        }
        return body.access_token;
    }

    render() {
        return (
            <div className="login-wrapper">
                <h1>Please Log In</h1>
                <form>
                    <label>
                        <p>Username</p>
                        <input type="text" onChange={(username) => this.props.setUsername(username.target.value)} />
                    </label>
                    <label>
                        <p>Password</p>
                        <input type="password" onChange={(password) => this.props.setUsername(password.target.value)} />
                    </label>
                    <div>
                        <button type="submit" onClick={() => this.login()}>Submit</button>
                    </div>
                </form>
            </div>
        )
    }
}
const mapStateToProps = (state) => {
    return { ...state };
};

const mapDispatchToProps = (dispatch) => {
    return {
        loginUser: (username, accessId) => dispatch(actions.loginSuccess(username, accessId)),
        setUsername: (username) => dispatch(actions.setUsername(username)),
        setPassword: (password) => dispatch(actions.setPassword(password)),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(LoginComponent);
