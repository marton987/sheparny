import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import EventForm from '../components/EventForm';
import { ServerClient } from '../services/server-client';

const serverClient = new ServerClient();

const HomePage = () => {
  const [events, setEvents] = useState([]);
  const [currentEvent, setCurrentEvent] = useState({});
  const [page, setPage] = useState(0);

  useEffect(() => {
    serverClient.listEvents(page, page * 10, 10).then((res) => {
      setEvents(res);
    });
  }, [page, currentEvent]);

  const logout = () => {
    serverClient.logout();
    setCurrentEvent({});
  };

  const handleWithdraw = (event) => {
    serverClient.attendEvent(event.id, false).then(() => {
      setCurrentEvent({});
    });
  };

  const handleAttend = (event) => {
    serverClient.attendEvent(event.id, true).then(() => {
      setCurrentEvent({});
    });
  };

  const addPage = (number) => {
    setPage(Math.max(0, page + number));
  };

  const EventRow = (event) => {
    return (
      <tr key={event.id}>
        <td>
          {serverClient.isAuthenticated() &&
            serverClient.getUser().username === event.created_by && (
              <button
                className="button is-small"
                onClick={() => setCurrentEvent(event)}
              >
                Edit
              </button>
            )}
        </td>
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
                <Link className="navbar-item" onClick={logout} to="#">
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
                        <th></th>
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
                  <nav className="pagination" role="navigation">
                    <button
                      className="pagination-previous"
                      onClick={() => addPage(-1)}
                    >
                      Previous
                    </button>
                    <button
                      className="pagination-next"
                      onClick={() => addPage(1)}
                    >
                      Next page
                    </button>
                  </nav>
                </div>
              </div>
              {serverClient.isAuthenticated() && (
                <EventForm event={currentEvent} setEvent={setCurrentEvent} />
              )}
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default HomePage;
