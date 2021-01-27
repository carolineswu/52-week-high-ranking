import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
// import logo from './logo.svg';
import './App.css';
import StocksList from './components/StocksList';
// import List from './pages/List';

export default class App extends Component {
  render() {
    const App = () => (
      <div>
        <Switch>
          <Route exact path='/' component={StocksList}/>
        </Switch>
      </div>
    )
    return (
      <Switch>
        <App/>
      </Switch>
    );
  }
}
