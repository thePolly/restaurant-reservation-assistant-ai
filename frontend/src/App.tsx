import React, { useEffect, useState } from 'react';
import './App.css';

// Translations
const translations = {
  de: {
    title: 'Restaurant Admin Panel',
    refresh: 'Aktualisieren',
    loading: 'Nachrichten werden geladen...',
    error: 'Fehler:',
    from: 'Von:',
    date: 'Datum',
    time: 'Zeit',
    people: 'Personen',
    specialRequests: 'Spezielle Anfragen',
    name: 'Name',
    accept: 'Annehmen',
    deny: 'Ablehnen',
    reply: 'Antwort',
    send: 'Senden',
    cancel: 'Abbrechen',
    breakfast: 'Frühstück',
    lunch: 'Mittagessen',
    dinner: 'Abendessen',
    reservation: 'Reservierung',
    general: 'Allgemein',
  },
  en: {
    title: 'Restaurant Admin Panel',
    refresh: 'Refresh',
    loading: 'Loading messages...',
    error: 'Error:',
    from: 'From:',
    date: 'Date',
    time: 'Time',
    people: 'People',
    specialRequests: 'Special Requests',
    name: 'Name',
    accept: 'Accept',
    deny: 'Deny',
    reply: 'Reply',
    send: 'Send',
    cancel: 'Cancel',
    breakfast: 'Breakfast',
    lunch: 'Lunch',
    dinner: 'Dinner',
    reservation: 'Reservation',
    general: 'General',
  },
};

// Types
interface ExtractionData {
  request_type: 'general' | 'reservation';
  date: string | null;
  time_category: 'breakfast' | 'lunch' | 'dinner' | null;
  people_count: number | null;
  special_requests: string[];
  location_preference: 'terrace' | 'saal' | 'taverne' | 'small_room' | null;
  name?: string;
}

interface ProcessedEmail {
  id: number;
  sender: string;
  masked_body: string;
  extracted_data: ExtractionData;
}

interface ModalState {
  isOpen: boolean;
  messageId: number | null;
  action: 'accept' | 'deny' | 'reply' | null;
  responseText: string;
}

// Modal Component
const Modal: React.FC<{
  isOpen: boolean;
  action?: string;
  onClose: () => void;
  onSend: (text: string) => void;
  initialText?: string;
  t: typeof translations.de;
}> = ({ isOpen, action, onClose, onSend, initialText = 'Type your response here...', t }) => {
  const [text, setText] = useState(initialText);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{action === 'reply' ? t.reply : t.send}</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <textarea
          className="modal-textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={initialText}
        />
        <div className="modal-footer">
          <button className="btn-cancel" onClick={onClose}>{t.cancel}</button>
          <button className="btn-send" onClick={() => {
            onSend(text);
            setText(initialText);
            onClose();
          }}>{t.send}</button>
        </div>
      </div>
    </div>
  );
};

// Message Component
const MessageCard: React.FC<{
  email: ProcessedEmail;
  t: typeof translations.de;
  onAction: (messageId: number, action: 'accept' | 'deny' | 'reply') => void;
}> = ({ email, t, onAction }) => {
  const { extracted_data: data } = email;
  const isReservation = data.request_type === 'reservation';

  const getTimeLabel = (category: string | null) => {
    if (!category) return '—';
    const timeMap: Record<string, string> = {
      breakfast: t.breakfast,
      lunch: t.lunch,
      dinner: t.dinner,
    };
    return timeMap[category] || category;
  };

  const isMissingData = !data.date || !data.time_category || !data.people_count;

  return (
    <div className={`message-card ${isReservation ? 'reservation' : 'general'}`}>
      <div className="message-header">
        <div className="sender-info">
          <strong>{t.from} {email.sender}</strong>
          <span className={`badge ${data.request_type}`}>
            {data.request_type === 'reservation' ? t.reservation : t.general}
          </span>
        </div>
      </div>

      {/* Highlighted Reservation Data */}
      <div className={`reservation-data ${isMissingData ? 'has-missing' : ''}`}>
        <div className="data-row">
          <span className="data-label">{t.name}:</span>
          <span className={`data-value ${!data.name ? 'missing' : ''}`}>
            {data.name || '—'}
          </span>
        </div>
        <div className="data-row">
          <span className="data-label">{t.people}:</span>
          <span className={`data-value ${!data.people_count ? 'missing' : ''}`}>
            {data.people_count || '—'}
          </span>
        </div>
        <div className="data-row">
          <span className="data-label">{t.date}:</span>
          <span className={`data-value ${!data.date ? 'missing' : ''}`}>
            {data.date || '—'}
          </span>
        </div>
        <div className="data-row">
          <span className="data-label">{t.time}:</span>
          <span className={`data-value ${!data.time_category ? 'missing' : ''}`}>
            {getTimeLabel(data.time_category)}
          </span>
        </div>
        {data.special_requests.length > 0 && (
          <div className="data-row">
            <span className="data-label">{t.specialRequests}:</span>
            <span className="data-value">
              {data.special_requests.join(', ')}
            </span>
          </div>
        )}
      </div>

      <div className="message-body">
        <p>"{email.masked_body}"</p>
      </div>

      <div className="message-actions">
        {isReservation ? (
          <>
            <button
              className="btn-accept"
              onClick={() => onAction(email.id, 'accept')}
            >
              ✓ {t.accept}
            </button>
            <button
              className="btn-deny"
              onClick={() => onAction(email.id, 'deny')}
            >
              ✕ {t.deny}
            </button>
          </>
        ) : (
          <button
            className="btn-reply"
            onClick={() => onAction(email.id, 'reply')}
          >
            {t.reply}
          </button>
        )}
      </div>
    </div>
  );
};

// Main App Component
const App: React.FC = () => {
  const [emails, setEmails] = useState<ProcessedEmail[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<'de' | 'en'>('de');
  const [modal, setModal] = useState<ModalState>({
    isOpen: false,
    messageId: null,
    action: null,
    responseText: '',
  });

  const t = translations[language];

  const fetchEmails = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/emails/mock');
      if (!response.ok) throw new Error('Server error');
      const data = await response.json();
      setEmails(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
  }, []);

  const handleAction = (messageId: number, action: 'accept' | 'deny' | 'reply') => {
    setModal({
      isOpen: true,
      messageId,
      action,
      responseText: '',
    });
  };

  const handleSendResponse = (text: string) => {
    console.log(`Action: ${modal.action}, Message ID: ${modal.messageId}, Response: ${text}`);
    // Here you would send the response to the backend
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>{t.title}</h1>
        <div className="header-actions">
          <button className="btn-refresh" onClick={fetchEmails}>
            {t.refresh}
          </button>
          <div className="language-toggle">
            <button
              className={`lang-btn ${language === 'de' ? 'active' : ''}`}
              onClick={() => setLanguage('de')}
            >
              DE
            </button>
            <button
              className={`lang-btn ${language === 'en' ? 'active' : ''}`}
              onClick={() => setLanguage('en')}
            >
              EN
            </button>
          </div>
        </div>
      </header>

      {loading && <p className="status-message">{t.loading}</p>}
      {error && <p className="error-message">{t.error} {error}</p>}

      <main className="messages-container">
        {emails.map((email) => (
          <MessageCard
            key={email.id}
            email={email}
            t={t}
            onAction={handleAction}
          />
        ))}
      </main>

      <Modal
        isOpen={modal.isOpen}
        action={modal.action || undefined}
        onClose={() => setModal({ ...modal, isOpen: false })}
        onSend={handleSendResponse}
        t={t}
      />
    </div>
  );
};

export default App;