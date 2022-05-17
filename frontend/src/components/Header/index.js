import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import {Link, NavLink} from 'react-router-dom';

const Header = () => {
  return (
    <>
      <Navbar collapseOnSelect expand="md" bg="dark" variant="dark">
        <Container fluid>
          <Navbar.Brand as={Link} to="/">DONATello</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="m-auto">
              <Nav.Link as={NavLink} to="/" exact>Home</Nav.Link>
              <Nav.Link as={NavLink} to="/charities">Charities</Nav.Link>
              <Nav.Link as={NavLink} to="/posts">Posts</Nav.Link>
            </Nav>
            <Button as={Link} to="/auth" variant="outline-light" >Sing In</Button>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}

export default Header;