import React, { useState, useEffect } from 'react';
import './Projects.css';
import project1 from '../assets/project1.png';
import project2 from '../assets/project2.png';
import project3 from '../assets/project3.png';
import project4 from '../assets/project4.png';
import project5 from '../assets/project5.png';

const projectsData = [
  {
    id: 1,
    title: "MENTAL HEALTH CHATBOT",
    desc: "AI-powered chatbot providing emotional support using NLP, designed with empathy and context-aware dialogue flows.",
    tags: ["PYTHON", "NLP", "REACT"],
    category: "FULL STACK",
    image: project1,
    year: "2024",
    featured: false
  },
  {
    id: 2,
    title: "PHILPALL APP",
    desc: "Social connection platform with rich user profiles, real-time feeds, and secure authentication.",
    tags: ["SPRING BOOT", "NODE.JS", "POSTGRESQL"],
    category: "FULL STACK",
    image: project2,
    year: "2024",
    featured: true
  },
  {
    id: 3,
    title: "FOODKART APPLICATION",
    desc: "Food delivery platform with real-time order tracking, cart management, and seamless checkout.",
    tags: ["REACT", "MONGODB", "EXPRESS"],
    category: "FULL STACK",
    image: project3,
    year: "2024",
    featured: false
  },
  {
    id: 4,
    title: "CINEMATIC BRAND REEL",
    desc: "High-energy promotional video highlighting brand identity with advanced motion graphics, color grading, and dynamic cuts.",
    tags: ["PREMIERE PRO", "AFTER EFFECTS", "COLOR GRADING"],
    category: "VIDEO EDITING",
    image: project4,
    year: "2025",
    featured: true
  },
  {
    id: 5,
    title: "FINTECH DASHBOARD UI",
    desc: "Modern, dark-themed analytics dashboard designed for clarity, data visualization, and seamless user experience.",
    tags: ["FIGMA", "PROTOTYPING", "DESIGN SYSTEM"],
    category: "UI/UX DESIGN",
    image: project5,
    year: "2025",
    featured: false
  }
];

const categories = ["ALL", "FULL STACK", "VIDEO EDITING", "UI/UX DESIGN"];

const Projects = ({ searchQuery }) => {
  const [activeTab, setActiveTab] = useState("ALL");

  // Sync search with tabs: switch to ALL if user is typing a search
  useEffect(() => {
    if (searchQuery && searchQuery.length > 0) {
      setActiveTab("ALL");
    }
  }, [searchQuery]);

  const filteredProjects = projectsData.filter((project) => {
    // 1. Check tab category
    const matchesCategory = activeTab === "ALL" || project.category === activeTab;
    
    // 2. Check search query (search by title or tags)
    const lowerQuery = (searchQuery || "").toLowerCase();
    const matchesSearch = 
      project.title.toLowerCase().includes(lowerQuery) ||
      project.tags.some(tag => tag.toLowerCase().includes(lowerQuery));

    return matchesCategory && matchesSearch;
  });

  return (
    <section id="projects" className="projects scroll-animate fade-up">
      <div className="container">
        <div className="projects-header">
          <div className="projects-title">
            <h4 style={{ justifyContent: 'flex-start' }}>SELECTED WORK</h4>
            <h2>PROJECTS THAT <span>PACK A PUNCH</span></h2>
          </div>
          <div className="projects-desc">
            <p>A curated selection of full-stack builds across healthcare, social, and commerce — blending clean code with cinematic design.</p>
          </div>
        </div>

        <div className="projects-filters">
          {categories.map(cat => (
            <button 
              key={cat} 
              className={`filter-btn ${activeTab === cat ? 'active' : ''}`}
              onClick={() => setActiveTab(cat)}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="projects-grid">
          {filteredProjects.length > 0 ? (
            filteredProjects.map((project, index) => (
              <div 
                key={project.id} 
                className={`project-card scroll-animate fade-up delay-${(index % 3 + 1) * 100}`}
              >
                <div className="project-image-container">
                  <img src={project.image} alt={project.title} className="project-image" />
                  <div className="project-year">{project.year}</div>
                  {project.featured && <div className="project-featured">⭐ FEATURED</div>}
                </div>
                <div className="project-content">
                  <h3>{project.title}</h3>
                  <p>{project.desc}</p>
                  <div className="project-tags">
                    {project.tags.map(tag => (
                      <span key={tag} className="project-tag">
                        <span className="tag-dot"></span> {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="no-results">
              <p>No projects found matching "{searchQuery}"</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default Projects;
