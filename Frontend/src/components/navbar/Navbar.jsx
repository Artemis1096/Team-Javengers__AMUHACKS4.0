import React, { useState } from 'react';
import { RiMenu3Line, RiCloseLine } from 'react-icons/ri';
import { Link, useNavigate } from 'react-router-dom';
import logo from '../../logo.png';
import './navbar.css';

const Navbar = () => {
  const [toggleMenu, setToggleMenu] = useState(false);
  const navigate = useNavigate();

  const handleLogoClick = () => {
    navigate('/');
  };

  return (
    <div className="gpt3__navbar">
      <div className="gpt3__navbar-links">
        <div className="gpt3__navbar-links_logo">
          <img className="logo" onClick={handleLogoClick} src={logo} alt="logo" />
        </div>
        <div className="gpt3__navbar-links_container">
          <p><Link to="/">Home</Link></p>
          <p><Link to="/smart-city">Smart City Monitoring</Link></p>
          <p><Link to="/WhatDoesItRepresents">What does our data represent</Link></p>
        </div>
      </div>
      <div className="gpt3__navbar-menu">
        {toggleMenu
          ? <RiCloseLine color="#fff" size={27} onClick={() => setToggleMenu(false)} />
          : <RiMenu3Line color="#fff" size={27} onClick={() => setToggleMenu(true)} />}
        {toggleMenu && (
          <div className="gpt3__navbar-menu_container scale-up-center">
            <div className="gpt3__navbar-menu_container-links">
              <p><Link to="/">Home</Link></p>
              <p><Link to="#wgpt3">What is GPT3?</Link></p>
              <p><Link to="#possibility">Open AI</Link></p>
              <p><Link to="#features">Case Studies</Link></p>
              <p><Link to="#blog">Library</Link></p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
