import React, { useState } from 'react';

import Login from '../components/Login';
import Register from '../components/Register';

const LoginPage = () => {
  const [displayLogin, setDisplayLogin] = useState(true);

  return (
    <section className="hero is-success is-fullheight">
      <div className="hero-body">
        <div className="container has-text-centered">
          <div className="column is-4 is-offset-4">
            {displayLogin ? <Login /> : <Register />}
            <button
              className="button is-small is-fullwidth"
              onClick={() => setDisplayLogin(!displayLogin)}
            >
              {displayLogin
                ? 'Do you want to register?'
                : 'Do you want to login?'}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LoginPage;
