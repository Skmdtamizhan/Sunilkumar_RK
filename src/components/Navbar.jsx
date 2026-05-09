import React, { useState, useEffect, useRef } from 'react';
import { Menu, Search, X } from 'lucide-react';
import './Navbar.css';

const Navbar = ({ searchQuery, setSearchQuery }) => {
  const [scrolled, setScrolled] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const searchInputRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSearchToggle = () => {
    setSearchOpen(!searchOpen);
    if (!searchOpen) {
      setTimeout(() => {
        searchInputRef.current?.focus();
      }, 100);
    } else {
      setSearchQuery(''); // Clear search when closing
    }
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
    // If user starts typing, scroll to projects section
    if (e.target.value.length === 1) {
      const projectsSection = document.getElementById('projects');
      if (projectsSection) {
        projectsSection.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="container nav-container">
        <div className="logo">
          <div className="logo-icon">S</div>
          <span className="logo-text">SKRK</span>
        </div>
        
        <ul className={`nav-links ${searchOpen ? 'hide-on-search' : ''}`}>
          <li><a href="#home">HOME</a></li>
          <li><a href="#projects">PROJECTS</a></li>
          <li><a href="#experience">EXPERIENCE</a></li>
          <li><a href="#contact">CONTACT</a></li>
        </ul>

        <div className="nav-actions">
          <div className={`search-container ${searchOpen ? 'open' : ''}`}>
            <input 
              ref={searchInputRef}
              type="text" 
              placeholder="Search projects..." 
              value={searchQuery}
              onChange={handleSearchChange}
              className="search-input"
            />
          </div>
          <button className="icon-btn" onClick={handleSearchToggle}>
            {searchOpen ? <X size={20} /> : <Search size={20} />}
          </button>
          <button className="icon-btn menu-btn"><Menu size={24} /></button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
