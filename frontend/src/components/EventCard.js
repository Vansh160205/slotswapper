import React from 'react';
import { format } from 'date-fns';

const EventCard = ({ event, onStatusChange, onDelete, showActions = true }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'BUSY':
        return '#6c757d';
      case 'SWAPPABLE':
        return '#28a745';
      case 'SWAP_PENDING':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  };

  return (
    <div className="event-card" style={{ borderLeft: `4px solid ${getStatusColor(event.status)}` }}>
      <div className="event-header">
        <h3>{event.title}</h3>
        <span className={`status-badge status-${event.status.toLowerCase()}`}>
          {event.status}
        </span>
      </div>
      <div className="event-time">
        <p>📅 {format(new Date(event.start_time), 'PPP')}</p>
        <p>🕐 {format(new Date(event.start_time), 'p')} - {format(new Date(event.end_time), 'p')}</p>
      </div>
      {showActions && (
        <div className="event-actions">
          {event.status === 'BUSY' && (
            <button
              onClick={() => onStatusChange(event.id, 'SWAPPABLE')}
              className="btn btn-success"
            >
              Make Swappable
            </button>
          )}
          {event.status === 'SWAPPABLE' && (
            <button
              onClick={() => onStatusChange(event.id, 'BUSY')}
              className="btn btn-secondary"
            >
              Make Busy
            </button>
          )}
          {event.status === 'SWAP_PENDING' && (
            <span className="pending-text">⏳ Swap Pending</span>
          )}
          {event.status !== 'SWAP_PENDING' && (
            <button
              onClick={() => onDelete(event.id)}
              className="btn btn-danger"
            >
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default EventCard;