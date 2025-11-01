import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) return null;

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand">
          <Link to="/dashboard">🔄 SlotSwapper</Link>
        </div>
        <div className="nav-links">
          <Link to="/dashboard" className={isActive('/dashboard')}>
            📅 My Calendar
          </Link>
          <Link to="/marketplace" className={isActive('/marketplace')}>
            🏪 Marketplace
          </Link>
          <Link to="/requests" className={isActive('/requests')}>
            🔔 Requests
          </Link>
        </div>
        <div className="nav-user">
          <span className="user-name">👤 {user.name}</span>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;