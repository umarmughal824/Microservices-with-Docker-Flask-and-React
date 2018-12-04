describe('Index', () => {
  it('should display the page correctly if a user is not logged in', () => {
    cy
      .visit('/')
      .get('.navbar-burger').click()
      .get('a').contains('User Status').should('not.be.visible')
      .get('a').contains('Log Out').should('not.be.visible')
      .get('a').contains('Register')
      .get('a').contains('Log In')
      .get('a').contains('Swagger')  // new
      .get('.notification.is-success').should('not.be.visible');
  });
});

describe('Go_to_About_page', () => {
  it('users should be able to view the page navigate to About', () => {
    cy
      .visit('/')
      .get('.nav-toggle.navbar-burger').first().click()
      .get('a[href="/about"]').first().click();
  });
});

describe('About', () => {
  it('users should be able to view the "/about" page', () => {
    cy
      .visit('/about')
      .get('h1').contains('About')
      .get('p').contains('Add something relevant here.');
  });
});
