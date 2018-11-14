describe('Index', () => {
  it('users should be able to view the "/" page', () => {
    cy
      .visit('http://localhost/')
      .get('h1').contains('All Users');
  });
});

describe('Go_to_About_page', () => {
  it('users should be able to view the page navigate to About', () => {
    cy
      .visit('http://localhost/')
      .get('.nav-toggle.navbar-burger').first().click()
      .get('a[href="/about"]').first().click();
  });
});

describe('About', () => {
  it('users should be able to view the "/about" page', () => {
    cy
      .visit('http://localhost/about')
      .get('h1').contains('About')
      .get('p').contains('Add something relevant here.');
  });
});
