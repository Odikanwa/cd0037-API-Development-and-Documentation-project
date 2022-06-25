import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './src/components/FormView';
import QuestionView from './src/components/QuestionView';
import Header from './src/components/Header';
import QuizView from './src/components/QuizView';

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header path />
        <Router>
          <Switch>
            <Route path='/' exact component={QuestionView} />
            <Route path='/add' component={FormView} />
            <Route path='/play' component={QuizView} />
            <Route component={QuestionView} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
