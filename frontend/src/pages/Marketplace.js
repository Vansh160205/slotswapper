import React, { useState, useEffect } from 'react';
import { eventsAPI, swapAPI } from '../services/api';
import EventCard from '../components/EventCard';
import Modal from '../components/Modal';
import { format } from 'date-fns';

const Marketplace = () => {
  const [swappableSlots, setSwappableSlots] = useState([]);
  const [mySwappableSlots, setMySwappableSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSlots();
  }, []);

  const fetchSlots = async () => {
    try {
      const [available, mine] = await Promise.all([
        eventsAPI.getSwappableSlots(),
        eventsAPI.getMyEvents(),
      ]);
      setSwappableSlots(available.data);
      setMySwappableSlots(mine.data.filter((e) => e.status === 'SWAPPABLE'));
    } catch (error) {
      console.error('Error fetching slots:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestSwap = (slot) => {
    setSelectedSlot(slot);
    setShowModal(true);
  };

  const handleConfirmSwap = async (mySlotId) => {
    try {
      await swapAPI.createSwapRequest({
        my_slot_id: mySlotId,
        their_slot_id: selectedSlot.id,
      });
      alert('Swap request sent successfully!');
      setShowModal(false);
      fetchSlots();
    } catch (error) {
      alert('Error sending swap request: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  if (loading) {
    return <div className="loading-container"><div className="spinner"></div></div>;
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>🏪 Marketplace</h1>
        <p>Available slots from other users</p>
      </div>

      {swappableSlots.length === 0 ? (
        <div className="empty-state">
          <h3>No swappable slots available</h3>
          <p>Check back later when other users mark their slots as swappable</p>
        </div>
      ) : (
        <div className="events-grid">
          {swappableSlots.map((slot) => (
            <div key={slot.id} className="marketplace-card">
              <EventCard event={slot} showActions={false} />
              <button
                onClick={() => handleRequestSwap(slot)}
                className="btn btn-primary btn-block"
              >
                Request Swap
              </button>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Select Your Slot to Offer">
        {mySwappableSlots.length === 0 ? (
          <div className="empty-state">
            <p>You don't have any swappable slots.</p>
            <p>Go to your calendar and mark a slot as swappable first!</p>
            <button onClick={() => setShowModal(false)} className="btn btn-secondary">
              Close
            </button>
          </div>
        ) : (
          <div className="swap-selection">
            <p className="swap-info">
              You're requesting: <strong>{selectedSlot?.title}</strong>
            </p>
            <p>Select one of your slots to offer in exchange:</p>
            <div className="my-slots-list">
              {mySwappableSlots.map((slot) => (
                <div key={slot.id} className="slot-option">
                  <div className="slot-info">
                    <strong>{slot.title}</strong>
                    <p className="slot-time">
                      {format(new Date(slot.start_time), 'PPp')}
                    </p>
                  </div>
                  <button
                    onClick={() => handleConfirmSwap(slot.id)}
                    className="btn btn-success"
                  >
                    Offer This Slot
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Marketplace;