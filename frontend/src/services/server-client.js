export class ServerClient {
  constructor() {
    this.baseUrl =
      process.env.REACT_APP_SERVER_BASE_URL || 'http://localhost:8000/api/v1/';
    this.headers = { 'Content-Type': 'application/json' };
  }

  setAuthorization() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    Object.assign(this.headers, {
      Authorization: `Bearer ${user.token}`,
    });
    return this.headers;
  }

  isAuthenticated() {
    return !!localStorage.getItem('currentUser', null);
  }

  getUser() {
    return localStorage.getItem('currentUser', null);
  }

  async listEvents(page = 0, offset = 0) {
    const response = await fetch(`${this.baseUrl}events`, {
      method: 'GET',
    })
      .then((response) => response.json())
      .then((res) => res.results);
    return response;
  }

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
          localStorage.setItem('currentUser', res);
        }
        return res;
      })
      .catch((error) => {
        return error;
      });
    return response;
  }

  async logout() {
    const headers = this.setAuthorization();
    await fetch(`${this.baseUrl}auth/logout`, {
      method: 'POST',
      headers,
    }).then(() => {
      localStorage.removeItem('currentUser');
    });
    return;
  }

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
          localStorage.setItem('currentUser', res);
        }
        return res;
      })
      .catch((error) => {
        return error;
      });
    return response;
  }
}
