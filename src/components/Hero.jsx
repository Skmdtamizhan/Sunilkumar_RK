import React from 'react';
import { Download } from 'lucide-react';
import './Hero.css';
import profilePic from '../assets/profile.png';

const Hero = () => {
  return (
    <section id="home" className="hero-section">
      <div className="hero-content-wrapper">
        
        {/* Outline Text Background */}
        <div className="hero-outline-text">
          <span>SUNIL</span>
          <span className="stroke-text">KUMAR</span>
        </div>

        {/* Tall Profile Image & Tags */}
        <div className="hero-image-container animate-fade-in">
          <img src={profilePic} alt="Sunil Kumar" className="hero-profile-img" />
          
          <div className="skills-tags">
            <div className="tag tag-react"><span className="dot"></span>REACT.JS</div>
            <div className="tag tag-python"><span className="dot"></span>PYTHON</div>
            <div className="tag tag-node"><span className="dot"></span>NODE.JS</div>
            <div className="tag tag-mongo"><span className="dot"></span>MONGODB</div>
          </div>
        </div>

        {/* Bottom overlapping text section */}
        <div className="hero-bottom-text">
          <div className="hero-glow-red"></div>
          
          <div className="portfolio-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            <span>PORTFOLIO 2024</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>

          <div className="container bottom-text-container">
            <h1 className="main-title">
              SUNIL <span>KUMAR</span> RK
            </h1>
            <h3 className="main-subtitle">CREATIVE DEVELOPER & DESIGNER</h3>
            <p className="main-desc">
              Full stack developer offering services in web development, video editing,<br/>
              and UI/UX design. Let's build impactful digital experiences.
            </p>
            
            <div className="main-buttons">
              <a href="#projects" className="btn btn-primary hero-btn">
                VIEW PROJECTS
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </a>
              <a href="#contact" className="btn btn-outline hero-btn-outline">
                CONTACT
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
