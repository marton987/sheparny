import React from 'react';
import PropTypes from 'prop-types';

import { ServerClient } from '../services/server-client';

const EventForm = ({ event }) => {
  const serverClient = new ServerClient();
  console.log(event);
  console.log(serverClient);
  return (
    <div className="column is-one-third has-text-left">
      <h1 className="title is-2">
        {event.id ? 'Update event' : 'Create event'}
      </h1>
      <div className="field">
        <label className="label">Title</label>
        <div className="control">
          <input className="input is-medium" type="text" />
        </div>
      </div>

      <div className="field">
        <label className="label">Description</label>
        <div className="control">
          <textarea className="textarea"></textarea>
        </div>
      </div>

      <div className="field">
        <label className="label">Date</label>
        <div className="control">
          <input className="input is-medium" type="date" />
        </div>
      </div>

      <div className="control">
        <button
          type="submit"
          className="button is-link is-fullwidth has-text-weight-medium is-medium"
        >
          Save event
        </button>
      </div>
    </div>
  );
};
EventForm.propTypes = {
  event: PropTypes.object,
};

export default EventForm;
