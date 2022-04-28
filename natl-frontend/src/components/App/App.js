import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

// Redux
import { connect } from 'react-redux';

// Other Componets
import Dashboard from '../Dashboard/Dashboard';
import Login from '../Login/Login';
import Preferences from '../Preferences/Preferences';

// CSS
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    console.log(this.props);
    if(this.props.login.accessId === undefined){
      return (
          <Login />
      )
    }
    return (
      <div className="wrapper">
        <h1>Application</h1>
        <BrowserRouter>
          <Routes>
            <Route exact path='/dashboard' element={<Dashboard />} />
            <Route exact path='/preferences' element={<Preferences />} />
          </Routes>
        </BrowserRouter>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return { ...state };
};

const mapDispatchToProps = (dispatch) => {
  return {
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
