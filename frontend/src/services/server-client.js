/**
 * ServerClient to connect with the server
 */
export class ServerClient {
  constructor() {
    this.baseUrl =
      process.env.REACT_APP_SERVER_BASE_URL || 'http://localhost:8000/api/v1/';
    this.headers = { 'Content-Type': 'application/json' };
  }

  /**
   * Returns the header with the token if user is authenticated
   */
  setAuthorization() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (user?.token) {
      return {
        ...this.headers,
        Authorization: `Token ${user.token}`,
      };
    }
    return this.headers;
  }

  /**
   * Validates if the user is authenticated with the
   * server
   */
  isAuthenticated() {
    return !!localStorage.getItem('currentUser', null);
  }

  /**
   * Retrieves the user from localStorage
   */
  getUser() {
    return JSON.parse(localStorage.getItem('currentUser', null));
  }

  /**
   * Indicates if the user will attend to the event
   * @param {int} eventId Id of the event to attend
   * @param {bool} attend will attend to the event
   */
  async attendEvent(eventId, attend) {
    const headers = this.setAuthorization();
    const response = await fetch(`${this.baseUrl}events/${eventId}/attend`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        attend,
      }),
    })
      .then((response) => response.json())
      .catch((error) => {
        return error;
      });
    return response;
  }

  /**
   * List all the events from the backend
   * @param {int} page Number of the current page
   * @param {int} offset Number of the current offset
   * @param {int} limit Number of results retrieved
   */
  async listEvents(page = 0, offset = 0, limit = 10) {
    const headers = this.setAuthorization();
    const params = new URLSearchParams({
      page,
      offset,
      limit,
    });
    const response = await fetch(`${this.baseUrl}events?${params}`, {
      method: 'GET',
      headers,
    })
      .then((response) => response.json())
      .then((res) => res.results);
    return response;
  }

  /**
   * Create or update a new event
   * @param {obj} event Instance to be created or updated
   */
  async createEvent(event) {
    const headers = this.setAuthorization();
    const body = JSON.stringify(event);
    const response = await fetch(
      `${this.baseUrl}events${event.id ? '/' + event.id : ''}`,
      {
        method: event.id ? 'PUT' : 'POST',
        headers,
        body,
      }
    )
      .then((response) => response.json())
      .catch((error) => {
        return error;
      });
    return response;
  }

  /**
   * Delete an event
   * @param {int} eventId Id of the event to delete
   */
  async deleteEvent(eventId) {
    const headers = this.setAuthorization();
    const response = await fetch(`${this.baseUrl}events/${eventId}`, {
      method: 'DELETE',
      headers,
    })
      .then((response) => response.json())
      .catch((error) => {
        return error;
      });
    return response;
  }

  /**
   * Authenticate a user
   * @param {obj} credentials email and password of the user to be authenticated
   */
  async login(credentials) {
    const body = JSON.stringify(credentials);
    const headers = this.setAuthorization();
    const response = await fetch(`${this.baseUrl}auth/login`, {
      method: 'POST',
      headers,
      body,
    })
      .then((response) => response.json())
      .then((res) => {
        if (res.token) {
          localStorage.setItem('currentUser', JSON.stringify(res));
        }
        return res;
      })
      .catch((error) => {
        return error;
      });
    return response;
  }

  /**
   * Unauthentiate the current user
   */
  async logout() {
    const headers = this.setAuthorization();
    await fetch(`${this.baseUrl}auth/logout`, {
      method: 'POST',
      headers,
    });
    localStorage.removeItem('currentUser');
    return;
  }

  /**
   * Register a new account
   * @param {obj} credentials Email an pasword of the user to be registered
   */
  async register(credentials) {
    const body = JSON.stringify(credentials);
    const headers = this.setAuthorization();
    const response = await fetch(`${this.baseUrl}accounts`, {
      method: 'POST',
      headers,
      body,
    })
      .then((response) => response.json())
      .then((res) => {
        if (res.token) {
          localStorage.setItem('currentUser', JSON.stringify(res));
        }
        return res;
      })
      .catch((error) => {
        return error;
      });
    return response;
  }
}
