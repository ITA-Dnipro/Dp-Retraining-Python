import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';

const Header = () => {
  return (
    <>
      <Navbar collapseOnSelect expand="md" bg="dark" variant="dark">
        <Container fluid>
          <Navbar.Brand href="/">DONATello</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="m-auto">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="/charities">Charities</Nav.Link>
              <Nav.Link href="/posts">Posts</Nav.Link>
            </Nav>
            <Button href="/auth/login" variant="outline-light" >Sing In</Button>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}

export default Header
