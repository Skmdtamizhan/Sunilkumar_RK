import React from 'react';
import './Experience.css';

const Experience = () => {
  return (
    <section id="experience" className="experience scroll-animate fade-up">
      <div className="container">
        <div className="section-title">
          <h4>EXPERIENCE</h4>
          <h2>NUMBERS THAT <span>TELL THE STORY</span></h2>
          <p className="section-subtitle">
            Combining technical expertise with creative vision to deliver impactful digital experiences
          </p>
        </div>

        <div className="stats-container">
          <div className="stat-card scroll-animate fade-up delay-100">
            <div className="stat-circle">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" className="bg-circle" />
                <circle cx="50" cy="50" r="45" className="progress-circle" style={{ strokeDashoffset: '70' }} />
              </svg>
              <div className="stat-content">
                <h3>03</h3>
                <p>PROJECTS</p>
              </div>
            </div>
          </div>

          <div className="stat-card scroll-animate fade-up delay-200">
            <div className="stat-circle center-stat">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" className="bg-circle" />
                <circle cx="50" cy="50" r="45" className="progress-circle" style={{ strokeDashoffset: '40' }} />
              </svg>
              <div className="stat-content">
                <h3>5+</h3>
                <p>STACKS</p>
              </div>
            </div>
          </div>

          <div className="stat-card scroll-animate fade-up delay-300">
            <div className="stat-circle">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" className="bg-circle" />
                <circle cx="50" cy="50" r="45" className="progress-circle" style={{ strokeDashoffset: '10' }} />
              </svg>
              <div className="stat-content">
                <h3>2024</h3>
                <p>YEAR</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="white-grid-bg"></div>
    </section>
  );
};

export default Experience;
