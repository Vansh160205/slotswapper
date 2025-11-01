import React, { useState, useEffect } from 'react';
import { eventsAPI } from '../services/api';
import EventCard from '../components/EventCard';
import Modal from '../components/Modal';

const Dashboard = () => {
  const [events, setEvents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [newEvent, setNewEvent] = useState({
    title: '',
    start_time: '',
    end_time: '',
  });

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await eventsAPI.getMyEvents();
      setEvents(response.data);
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEvent = async (e) => {
    e.preventDefault();
    try {
      await eventsAPI.createEvent(newEvent);
      setShowModal(false);
      setNewEvent({ title: '', start_time: '', end_time: '' });
      fetchEvents();
    } catch (error) {
      alert('Error creating event: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  const handleStatusChange = async (eventId, newStatus) => {
    try {
      await eventsAPI.updateEvent(eventId, { status: newStatus });
      fetchEvents();
    } catch (error) {
      alert('Error updating event: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  const handleDeleteEvent = async (eventId) => {
    if (window.confirm('Are you sure you want to delete this event?')) {
      try {
        await eventsAPI.deleteEvent(eventId);
        fetchEvents();
      } catch (error) {
        alert('Error deleting event: ' + (error.response?.data?.detail || 'Unknown error'));
      }
    }
  };

  if (loading) {
    return <div className="loading-container"><div className="spinner"></div></div>;
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>📅 My Calendar</h1>
        <button onClick={() => setShowModal(true)} className="btn btn-primary">
          + Add Event
        </button>
      </div>

      {events.length === 0 ? (
        <div className="empty-state">
          <h3>No events yet</h3>
          <p>Create your first event to get started</p>
          <button onClick={() => setShowModal(true)} className="btn btn-primary">
            Create Event
          </button>
        </div>
      ) : (
        <div className="events-grid">
          {events.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              onStatusChange={handleStatusChange}
              onDelete={handleDeleteEvent}
            />
          ))}
        </div>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Create New Event">
        <form onSubmit={handleCreateEvent}>
          <div className="form-group">
            <label>Event Title</label>
            <input
              type="text"
              placeholder="e.g., Team Meeting"
              value={newEvent.title}
              onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Start Time</label>
            <input
              type="datetime-local"
              value={newEvent.start_time}
              onChange={(e) => setNewEvent({ ...newEvent, start_time: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>End Time</label>
            <input
              type="datetime-local"
              value={newEvent.end_time}
              onChange={(e) => setNewEvent({ ...newEvent, end_time: e.target.value })}
              required
            />
          </div>
          <div className="modal-actions">
            <button type="submit" className="btn btn-primary">
              Create Event
            </button>
            <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Dashboard;