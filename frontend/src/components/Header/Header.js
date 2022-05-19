import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import {Link, NavLink} from 'react-router-dom';
import axiosInstance from "../../axiosApi";

const Header = ({isAuthenticated, setIsAuthenticated}) => {
  const handleLogout = () => {
    axiosInstance.post(
      '/auth/logout',
    )
    .then(response => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_id');
      setIsAuthenticated(false);
      window.location.href = '/';
    })
    .catch(error => {
      console.log(error);
    });
  }

  let profileButton;

  if (isAuthenticated) {
    profileButton = <>
      <Button as={Link} to="/profile" variant="outline-light" className="me-2" >
        Profile
      </Button>
      <Button onClick={handleLogout} variant="outline-light" >
        Logout
      </Button>
    </>;
  } else {
    profileButton = <Button as={Link} to="/auth" variant="outline-light" >Sing In</Button>;
  }

  return (
    <>
      <Navbar collapseOnSelect expand="md" bg="dark" variant="dark">
        <Container fluid>
          <Navbar.Brand as={Link} to="/">DONATello</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="m-auto">
              <Nav.Link as={NavLink} to="/">Home</Nav.Link>
              <Nav.Link as={NavLink} to="/charities">Charities</Nav.Link>
              <Nav.Link as={NavLink} to="/posts">Posts</Nav.Link>
            </Nav>
            {profileButton}
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}

export default Header;
