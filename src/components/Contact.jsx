import React, { useState } from 'react';
import { Mail, Phone, MapPin, Send, CheckCircle, AlertCircle } from 'lucide-react';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState('idle'); // idle, submitting, success, error
  const [errorMsg, setErrorMsg] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('submitting');
    setErrorMsg('');

    try {
      const response = await fetch('http://localhost:5000/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('success');
        setFormData({ name: '', email: '', message: '' });
        setTimeout(() => setStatus('idle'), 5000);
      } else {
        setStatus('error');
        setErrorMsg(data.error || 'Something went wrong.');
      }
    } catch (err) {
      console.error(err);
      setStatus('error');
      setErrorMsg('Failed to connect to the server. Please try again later.');
    }
  };

  return (
    <section id="contact" className="contact scroll-animate fade-up">
      <div className="container contact-container">
        <div className="contact-info scroll-animate slide-right">
          <div className="contact-header">
            <h4 style={{ justifyContent: 'flex-start' }}>GET IN TOUCH</h4>
            <h2>LET'S <span>COLLABORATE</span></h2>
            <p>Have a project in mind, a wild idea, or just want to say hi?<br/>Drop a message — I reply within 24 hours.</p>
          </div>

          <div className="contact-details">
            <div className="contact-item">
              <div className="contact-icon">
                <Mail size={20} />
              </div>
              <span>skmdtamizhan007@gmail.com</span>
            </div>
            
            <div className="contact-item">
              <div className="contact-icon">
                <Phone size={20} />
              </div>
              <span>+91 9360629570</span>
            </div>
            
            <div className="contact-item">
              <div className="contact-icon">
                <MapPin size={20} />
              </div>
              <span>Bengaluru, India</span>
            </div>
          </div>
        </div>

        <div className="contact-form-wrapper scroll-animate slide-left delay-200">
          <div className="form-accent-square"></div>
          <form className="contact-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>NAME</label>
              <input 
                type="text" 
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Your full name" 
                required 
              />
            </div>
            
            <div className="form-group">
              <label>EMAIL</label>
              <input 
                type="email" 
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="you@domain.com" 
                required 
              />
            </div>
            
            <div className="form-group">
              <label>MESSAGE</label>
              <textarea 
                name="message"
                value={formData.message}
                onChange={handleChange}
                placeholder="Tell me about your project..." 
                rows="4" 
                required
              ></textarea>
            </div>

            {status === 'success' && (
              <div className="status-message success">
                <CheckCircle size={18} /> Message sent successfully!
              </div>
            )}
            {status === 'error' && (
              <div className="status-message error">
                <AlertCircle size={18} /> {errorMsg}
              </div>
            )}

            <button type="submit" className="btn btn-primary submit-btn" disabled={status === 'submitting'}>
              {status === 'submitting' ? 'SENDING...' : 'SEND MESSAGE'} <Send size={16} />
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Contact;
