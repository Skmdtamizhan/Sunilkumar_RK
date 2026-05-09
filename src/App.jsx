import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Experience from './components/Experience';
import Projects from './components/Projects';
import Contact from './components/Contact';
import useScrollAnimation from './hooks/useScrollAnimation';
import './App.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  
  // Initialize scroll animations
  useScrollAnimation();

  return (
    <div className="app">
      <Navbar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      <main>
        <Hero />
        <Experience />
        <Projects searchQuery={searchQuery} />
        <Contact />
      </main>
      <footer style={{ background: '#0a0a0a', padding: '2rem 0', textAlign: 'center', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>© 2026 Sunil Kumar RK. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
