import React from 'react';
import { useForm } from 'react-hook-form';
import { useHistory } from 'react-router-dom';

import { ServerClient } from '../services/server-client';

const Login = () => {
  const serverClient = new ServerClient();
  const { register, handleSubmit, errors, setError } = useForm();
  const history = useHistory();
  const onSubmit = (data) => {
    serverClient.login(data).then((resData) => {
      if (resData.id) {
        history.push('/');
      }
      if (resData.message) {
        setError('formError', 'password', resData.message);
      }
    });
  };

  return (
    <>
      <h3 className="title has-text-black">Login</h3>
      <p className="subtitle has-text-black">Please login to proceed.</p>
      <div className="box">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="field">
            <div className="control">
              <input
                className="input is-large"
                type="email"
                placeholder="Your Email"
                name="email"
                ref={register({ required: true })}
              />
            </div>
          </div>

          <div className="field">
            <div className="control">
              <input
                className="input is-large"
                type="password"
                placeholder="Your Password"
                name="password"
                ref={register({ required: true })}
              />
            </div>
            {errors.formError && (
              <div className="form-error">{errors.formError.message}</div>
            )}
          </div>

          <button className="button is-block is-info is-large is-fullwidth">
            Login <i className="fa fa-sign-in"></i>
          </button>
        </form>
      </div>
    </>
  );
};
export default Login;
