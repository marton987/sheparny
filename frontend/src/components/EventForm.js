import React from 'react';
import PropTypes from 'prop-types';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';

import { ServerClient } from '../services/server-client';

const serverClient = new ServerClient();

const EventForm = ({ event, setEvent }) => {
  const { register, handleSubmit, errors, setError, reset } = useForm();

  const resetForm = () => {
    setEvent({});
    reset();
  };

  const onSubmit = (data) => {
    serverClient.createEvent({ ...data, id: event.id }).then((eventData) => {
      if (!eventData.id) {
        Object.keys(eventData).forEach((errorId) =>
          setError(errorId, 'notEqual', 'Field is required')
        );
      } else {
        toast('Event saved');
        setEvent(eventData);
        resetForm();
      }
    });
  };

  const deleteEvent = () => {
    serverClient.deleteEvent(event.id).then(() => {
      toast('Event deleted');
      resetForm();
    });
  };

  return (
    <div className="column is-one-third has-text-left">
      <h1 className="title is-2">
        {event.id ? 'Update event' : 'Create event'}
      </h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="field">
          <label className="label">Title</label>
          <div className="control">
            <input
              className="input is-medium"
              type="text"
              name="title"
              defaultValue={event?.title || ''}
              ref={register({ required: true })}
            />
            {errors?.title && (
              <div className="form-error">Title is required</div>
            )}
          </div>
        </div>

        <div className="field">
          <label className="label">Description</label>
          <div className="control">
            <textarea
              className="textarea"
              name="description"
              defaultValue={event?.description || ''}
              ref={register({ required: true })}
            ></textarea>
            {errors?.description && (
              <div className="form-error">Description is required</div>
            )}
          </div>
        </div>

        <div className="field">
          <label className="label">Date</label>
          <div className="control">
            <input
              className="input is-medium"
              type="date"
              name="date"
              defaultValue={event?.date || ''}
              ref={register({ required: true })}
            />
            {errors?.date && <div className="form-error">Date is required</div>}
          </div>
        </div>

        <div className="control">
          <button
            type="submit"
            className="button is-link is-fullwidth has-text-weight-medium is-medium"
          >
            Save event
          </button>
          {errors?.formError && (
            <div className="form-error">{errors.formError.message}</div>
          )}
        </div>

        <br />
        {serverClient.isAuthenticated() &&
          serverClient.getUser().username === event.created_by && (
            <>
              <div className="control">
                <span
                  className="button is-danger is-light is-link is-fullwidth has-text-weight-medium is-medium"
                  onClick={deleteEvent}
                >
                  Delete
                </span>
              </div>
              <br />
              <div className="control">
                <span
                  className="button is-info is-light is-link is-fullwidth has-text-weight-medium is-medium"
                  onClick={resetForm}
                >
                  Cancel update
                </span>
              </div>
            </>
          )}
      </form>
    </div>
  );
};
EventForm.propTypes = {
  event: PropTypes.object,
  setEvent: PropTypes.func,
};

export default EventForm;
