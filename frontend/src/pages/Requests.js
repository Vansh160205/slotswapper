import React, { useState, useEffect } from 'react';
import { swapAPI } from '../services/api';
import { format } from 'date-fns';

const Requests = () => {
  const [incoming, setIncoming] = useState([]);
  const [outgoing, setOutgoing] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const [incomingRes, outgoingRes] = await Promise.all([
        swapAPI.getIncomingRequests(),
        swapAPI.getOutgoingRequests(),
      ]);
      setIncoming(incomingRes.data);
      setOutgoing(outgoingRes.data);
    } catch (error) {
      console.error('Error fetching requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResponse = async (requestId, accept) => {
    try {
      await swapAPI.respondToSwap(requestId, accept);
      alert(accept ? 'Swap accepted!' : 'Swap rejected!');
      fetchRequests();
    } catch (error) {
      alert('Error responding to swap: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  const handleCancel = async (requestId) => {
    if (window.confirm('Are you sure you want to cancel this swap request?')) {
      try {
        await swapAPI.cancelSwapRequest(requestId);
        alert('Swap request cancelled');
        fetchRequests();
      } catch (error) {
        alert('Error cancelling request: ' + (error.response?.data?.detail || 'Unknown error'));
      }
    }
  };

  if (loading) {
    return <div className="loading-container"><div className="spinner"></div></div>;
  }

  return (
    <div className="page-container">
      <h1>🔔 Swap Requests</h1>

      <section className="requests-section">
        <h2>Incoming Requests</h2>
        {incoming.length === 0 ? (
          <div className="empty-state">
            <p>No incoming swap requests</p>
          </div>
        ) : (
          <div className="requests-list">
            {incoming.map((request) => (
              <div key={request.id} className="request-card incoming">
                <div className="request-header">
                  <h3>Swap Request from {request.requester_name}</h3>
                  <span className="request-date">
                    {format(new Date(request.created_at), 'PPp')}
                  </span>
                </div>
                <div className="request-details">
                  <div className="swap-offer">
                    <span className="label">They offer:</span>
                    <strong>{request.requester_slot_title}</strong>
                  </div>
                  <div className="swap-arrow">⇄</div>
                  <div className="swap-request">
                    <span className="label">They want:</span>
                    <strong>{request.requested_slot_title}</strong>
                  </div>
                </div>
                <div className="request-actions">
                  <button
                    onClick={() => handleResponse(request.id, true)}
                    className="btn btn-success"
                  >
                    ✓ Accept
                  </button>
                  <button
                    onClick={() => handleResponse(request.id, false)}
                    className="btn btn-danger"
                  >
                    ✗ Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="requests-section">
        <h2>Outgoing Requests</h2>
        {outgoing.length === 0 ? (
          <div className="empty-state">
            <p>No outgoing swap requests</p>
          </div>
        ) : (
          <div className="requests-list">
            {outgoing.map((request) => (
              <div key={request.id} className="request-card outgoing">
                <div className="request-header">
                  <h3>Swap Request to {request.receiver_name}</h3>
                  <span className={`status-badge status-${request.status.toLowerCase()}`}>
                    {request.status}
                  </span>
                </div>
                <div className="request-details">
                  <div className="swap-offer">
                    <span className="label">You offer:</span>
                    <strong>{request.requester_slot_title}</strong>
                  </div>
                  <div className="swap-arrow">⇄</div>
                  <div className="swap-request">
                    <span className="label">You want:</span>
                    <strong>{request.requested_slot_title}</strong>
                  </div>
                </div>
                <div className="request-footer">
                  <span className="request-date">
                    Sent: {format(new Date(request.created_at), 'PPp')}
                  </span>
                  {request.status === 'PENDING' && (
                    <button
                      onClick={() => handleCancel(request.id)}
                      className="btn btn-secondary btn-sm"
                    >
                      Cancel Request
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export default Requests;