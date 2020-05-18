import React from 'react';
import { useForm } from 'react-hook-form';
import { useHistory } from 'react-router-dom';

import { ServerClient } from '../services/server-client';

const serverClient = new ServerClient();

const Register = () => {
  const { register, handleSubmit, errors, setError } = useForm();
  const history = useHistory();

  const onSubmit = (data) => {
    if (data.password !== data.repeatPassword) {
      setError('repeatPassword', 'notEqual', 'Password does not match');
    } else {
      serverClient.register(data).then((resData) => {
        if (resData.id) {
          history.push('/');
        }
        if (resData.password) {
          setError('password', 'notEqual', resData.password);
        }
        if (resData.email) {
          setError('email', 'notEqual', resData.email);
        }
      });
    }
  };

  return (
    <>
      <h3 className="title has-text-black">Register</h3>
      <p className="subtitle has-text-black">Please fill the next form.</p>
      <div className="box">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="field">
            <div className="control">
              <input
                className="input is-large"
                type="email"
                name="email"
                placeholder="Your Email"
                ref={register({ required: true })}
              />
            </div>
          </div>

          <div className="field">
            <div className="control">
              <input
                className="input is-large"
                type="password"
                name="password"
                placeholder="Your Password"
                ref={register({ required: true })}
              />
            </div>
            <ul>
              {errors?.password?.message?.map((error) => (
                <li key={error} className="form-error">
                  {error}
                </li>
              ))}
            </ul>
          </div>

          <div className="field">
            <div className="control">
              <input
                className="input is-large"
                type="password"
                name="repeatPassword"
                placeholder="Repeat Password"
                ref={register({ required: true })}
              />
              {errors?.repeatPassword && (
                <div className="form-error">
                  {errors.repeatPassword.message}
                </div>
              )}
            </div>
          </div>
          <button className="button is-block is-info is-large is-fullwidth">
            Register <i className="fa fa-sign-in"></i>
          </button>
        </form>
      </div>
    </>
  );
};
export default Register;
