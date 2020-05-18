import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import EventForm from '../components/EventForm';
import { ServerClient } from '../services/server-client';

const serverClient = new ServerClient();

const HomePage = () => {
  const [events, setEvents] = useState([]);
  const [currentEvent] = useState({});
  // const [currentEvent, setCurrentEvent] = useState({});
  // const [page, setPage] = useState(0);
  // const [offset, setOffset] = useState(0);
  const [page] = useState(0);
  const [offset] = useState(0);

  useEffect(() => {
    serverClient.listEvents(page, offset).then((res) => {
      setEvents(res);
    });
  }, [page, offset]);

  const handleWithdraw = (event) => {
    console.log(event);
  };

  const handleAttend = (event) => {
    console.log(event);
  };

  const EventRow = (event) => {
    return (
      <tr key={event.id}>
        <td>{event.id}</td>
        <td>{event.title}</td>
        <td>@{event.created_by}</td>
        <td>{event.date}</td>
        <td>{event.count_participants}</td>
        {serverClient.isAuthenticated() && (
          <td>
            {event.attends ? (
              <button
                className="button is-danger"
                onClick={() => handleWithdraw(event)}
              >
                Withdraw
              </button>
            ) : (
              <button
                className="button is-success"
                onClick={() => handleAttend(event)}
              >
                Attend
              </button>
            )}
          </td>
        )}
      </tr>
    );
  };

  return (
    <>
      <nav className="navbar">
        <div className="container">
          <div id="navbarMenu" className="navbar-menu">
            <div className="navbar-end">
              <Link className="navbar-item" to="/">
                Home
              </Link>
              {!serverClient.isAuthenticated() ? (
                <Link className="navbar-item" to="/login">
                  Login
                </Link>
              ) : (
                <Link
                  className="navbar-item"
                  onClick={() => serverClient.logout()}
                  to="#"
                >
                  Logout
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>
      <section className="hero is-fullheight">
        <div className="hero-body">
          <div className="container has-text-centered">
            <div className="columns is-8 is-variable ">
              <div className="column is-two-thirds has-text-left">
                <h1 className="title is-1">Events</h1>
                <div className="table-container">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Owner</th>
                        <th>Date</th>
                        <th>Participants</th>
                        {serverClient.isAuthenticated() && <th>I'm in</th>}
                      </tr>
                    </thead>
                    <tbody>{events.map(EventRow)}</tbody>
                  </table>
                </div>
              </div>
              {serverClient.isAuthenticated() && (
                <EventForm event={currentEvent} />
              )}
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default HomePage;
