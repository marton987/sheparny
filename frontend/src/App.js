import React from 'react';
import { Route, Switch } from 'react-router-dom';
import 'bulma/css/bulma.css';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import PageNotFound from './pages/PageNotFound';

function App() {
  return (
    <Switch>
      <Route exact path="/" component={HomePage} />
      <Route path="/login" component={LoginPage} />
      <Route component={PageNotFound} />
    </Switch>
  );
}

export default App;
