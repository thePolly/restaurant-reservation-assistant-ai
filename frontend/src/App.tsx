import React, { useEffect, useState } from "react";
import "./App.css";

// Translations
const translations = {
  de: {
    title: "Restaurant Admin Panel",
    refresh: "Aktualisieren",
    loading: "Nachrichten werden geladen...",
    error: "Fehler:",
    from: "Von:",
    date: "Datum",
    time: "Zeit",
    people: "Personen",
    specialRequests: "Spezielle Anfragen",
    name: "Name",
    accept: "Annehmen",
    deny: "Ablehnen",
    reply: "Antwort",
    send: "Senden",
    cancel: "Abbrechen",
    breakfast: "Frühstück",
    lunch: "Mittagessen",
    dinner: "Abendessen",
    reservation: "Reservierung",
    general: "Allgemein",
  },
  en: {
    title: "Restaurant Admin Panel",
    refresh: "Refresh",
    loading: "Loading messages...",
    error: "Error:",
    from: "From:",
    date: "Date",
    time: "Time",
    people: "People",
    specialRequests: "Special Requests",
    name: "Name",
    accept: "Accept",
    deny: "Deny",
    reply: "Reply",
    send: "Send",
    cancel: "Cancel",
    breakfast: "Breakfast",
    lunch: "Lunch",
    dinner: "Dinner",
    reservation: "Reservation",
    general: "General",
  },
};

// Types
interface ExtractionData {
  request_type: "general" | "reservation";
  date: string | null;
  time_category: "breakfast" | "lunch" | "dinner" | null;
  people_count: number | null;
  special_requests: string[];
  location_preference: "terrace" | "saal" | "taverne" | "small_room" | null;
  name?: string;
}

interface ProcessedEmail {
  id: number;
  sender: string;
  sender_email: string;
  masked_body: string;
  extracted_data: ExtractionData;
}

interface ModalState {
  isOpen: boolean;

  messageId: number | null;

  action: "accept" | "deny" | "reply" | null;

  responseText: string;

  initialText: string;
  selectedEmail: ProcessedEmail | null;
}

// Modal Component
const Modal: React.FC<{
  isOpen: boolean;
  action?: string;
  onClose: () => void;
  onSend: (text: string) => void;
  initialText?: string;
  t: typeof translations.de;
}> = ({
  isOpen,
  action,
  onClose,
  onSend,
  initialText = "Type your response here...",
  t,
}) => {
  const [text, setText] = useState(initialText);

  React.useEffect(() => {
    setText(initialText);
  }, [initialText, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{action === "reply" ? t.reply : t.send}</h2>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        <textarea
          className="modal-textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={initialText}
        />
        <div className="modal-footer">
          <button className="btn-cancel" onClick={onClose}>
            {t.cancel}
          </button>
          <button
            className="btn-send"
            onClick={() => {
              onSend(text);
              setText(initialText);
              onClose();
            }}
          >
            {t.send}
          </button>
        </div>
      </div>
    </div>
  );
};

// Message Component
const MessageCard: React.FC<{
  email: ProcessedEmail;
  t: typeof translations.de;
  onAction: (
    messageId: number,
    action: "accept" | "deny" | "reply",
    email: ProcessedEmail,
  ) => void;
}> = ({ email, t, onAction }) => {
  const { extracted_data: data } = email;
  const isReservation = data.request_type === "reservation";

  const getTimeLabel = (category: string | null) => {
    if (!category) return "—";
    const timeMap: Record<string, string> = {
      breakfast: t.breakfast,
      lunch: t.lunch,
      dinner: t.dinner,
    };
    return timeMap[category] || category;
  };

  const isMissingData = !data.date || !data.time_category || !data.people_count;

  return (
    <div
      className={`message-card ${isReservation ? "reservation" : "general"}`}
    >
      <div className="message-header">
        <div className="sender-info">
          <strong>
            {t.from} {email.sender}
          </strong>
          <span className={`badge ${data.request_type}`}>
            {data.request_type === "reservation" ? t.reservation : t.general}
          </span>
        </div>
      </div>

      {/* Highlighted Reservation Data */}
      {isReservation && (
        <div
          className={`reservation-data ${isMissingData ? "has-missing" : ""}`}
        >
          <div className="data-row pill">
            <span className="pill-label">{t.name}</span>
            <span className={`data-value ${!data.name ? "missing" : ""}`}>
              {data.name || "—"}
            </span>
          </div>
          <div className="data-row pill">
            <span className="pill-label">{t.people}</span>
            <span
              className={`data-value ${!data.people_count ? "missing" : ""}`}
            >
              {data.people_count || "—"}
            </span>
          </div>
          <div className="data-row pill">
            <span className="pill-label">{t.date}</span>
            <span className={`data-value ${!data.date ? "missing" : ""}`}>
              {data.date || "—"}
            </span>
          </div>
          <div className="data-row pill">
            <span className="pill-label">{t.time}</span>
            <span
              className={`data-value ${!data.time_category ? "missing" : ""}`}
            >
              {getTimeLabel(data.time_category)}
            </span>
          </div>
          {data.special_requests.length > 0 && (
            <div className="data-row pill">
              <span className="pill-label">{t.specialRequests}</span>
              <span className="data-value">
                {data.special_requests.join(", ")}
              </span>
            </div>
          )}
        </div>
      )}

      <div className="message-body">
        <p>"{email.masked_body}"</p>
      </div>

      <div className="message-actions">
        {isReservation ? (
          <>
            <button
              className="btn-accept"
              onClick={() => onAction(email.id, "accept", email)}
            >
              ✓ {t.accept}
            </button>
            <button
              className="btn-deny"
              onClick={() => onAction(email.id, "deny", email)}
            >
              ✕ {t.deny}
            </button>
          </>
        ) : (
          <button
            className="btn-reply"
            onClick={() => onAction(email.id, "reply", email)}
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
  const [answeredEmails, setAnsweredEmails] = useState<ProcessedEmail[]>([]);
  const [activeTab, setActiveTab] = useState<"incoming" | "answered">(
    "incoming",
  );
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<"de" | "en">("de");
  const [modal, setModal] = useState<ModalState>({
    isOpen: false,
    messageId: null,
    action: null,
    responseText: "",
    initialText: "Type your response here...",
    selectedEmail: null,
  });

  const t = translations[language];
  const visibleEmails = activeTab === "incoming" ? emails : answeredEmails;

 const fetchEmails = async () => {
  setLoading(true);
  try {
    const response = await fetch("http://127.0.0.1:8000/emails/mock");
    if (!response.ok) throw new Error("Server error");

    const data: ProcessedEmail[] = await response.json();

    setEmails(
      data.filter(
        (incomingEmail) =>
          !answeredEmails.some(
            (answeredEmail) => answeredEmail.id === incomingEmail.id,
          ),
      ),
    );
  } catch (err) {
    setError(err instanceof Error ? err.message : "Unknown error");
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    fetchEmails();
  }, []);

  const generateReplyText = async (
    email: ProcessedEmail,
    action: "accept" | "deny",
  ): Promise<string> => {
    try {
      const { extracted_data: data } = email;

      // Simply pass extracted data to backend - no business logic here
      const requestBody = {
        name: data.name,
        date: data.date,
        time_category: data.time_category,
        people_count: data.people_count,
        action: action === "accept" ? "accept" : "alternative",
      };

      console.log("Reply request body:", requestBody);
      const response = await fetch(
        "http://127.0.0.1:8000/replies/generate-from-email",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        },
      );

      if (!response.ok) throw new Error("Failed to generate reply");
      const result = await response.json();

      console.log("Reply generation response:", result);

      if (!result.success) {
        return result.message || "Error generating reply. Please try again.";
      }

      return result.reply_text || "No reply text returned.";
    } catch (error) {
      console.error("Error generating reply:", error);
      return "Error generating reply. Please try again.";
    }
  };

const generateGeneralReplyText = async (
  email: ProcessedEmail,
): Promise<string> => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/replies/generate-general",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          masked_body: email.masked_body,
        }),
      },
    );

    const result = await response.json();

    if (!result.success) {
      return result.message || "Error generating reply.";
    }

    return result.reply_text || "No reply text returned.";
  } catch (error) {
    console.error("Error generating general reply:", error);
    return "Error generating reply. Please try again.";
  }
};


const handleAction = async (
  messageId: number,
  action: "accept" | "deny" | "reply",
  email: ProcessedEmail,
) => {
  setModal({
    isOpen: true,
    messageId,
    action,
    responseText: "",
    initialText: "Loading reply...",
    selectedEmail: email,
  });

  let generatedText = "Type your response here...";

  if (action === "accept" || action === "deny") {
    generatedText = await generateReplyText(email, action);
  }

  if (action === "reply") {
    generatedText = await generateGeneralReplyText(email);
  }

  setModal({
    isOpen: true,
    messageId,
    action,
    responseText: "",
    initialText: generatedText,
    selectedEmail: email,
  });
};

   
  const closeModal = () => {
    setModal((prev) => ({
      ...prev,
      isOpen: false,
      selectedEmail: null,
    }));
  };

  const handleSendResponse = async (text: string) => {
    if (!modal.selectedEmail) {
      console.error("No selected email");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/emails/send-reply", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          to_email: modal.selectedEmail.sender_email,
          subject: `Re: Reservation request`,
          body: text,
        }),
      });

      const result = await response.json();
      if (!result.success) {
        console.error(result.message);
        alert(result.message);
        return;
      }
    } catch (error) {
      console.warn(
        "Reply send endpoint unavailable or failed, moving email locally.",
        error,
      );
    }

    const sentEmail = modal.selectedEmail;
    setAnsweredEmails((prev) => [...prev, sentEmail]);
    setEmails((prev) => prev.filter((email) => email.id !== sentEmail.id));
    closeModal();
    setActiveTab("answered");
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
              className={`lang-btn ${language === "de" ? "active" : ""}`}
              onClick={() => setLanguage("de")}
            >
              DE
            </button>
            <button
              className={`lang-btn ${language === "en" ? "active" : ""}`}
              onClick={() => setLanguage("en")}
            >
              EN
            </button>
          </div>
        </div>
      </header>

      {loading && <p className="status-message">{t.loading}</p>}
      {error && (
        <p className="error-message">
          {t.error} {error}
        </p>
      )}

      <main className="messages-container">
        <div className="tabs">
          <button
            className={`tab-button ${activeTab === "incoming" ? "active" : ""}`}
            onClick={() => setActiveTab("incoming")}
          >
            Incoming Messages
            <span className="tab-badge">{emails.length}</span>
          </button>
          <button
            className={`tab-button ${activeTab === "answered" ? "active" : ""}`}
            onClick={() => setActiveTab("answered")}
          >
            Answered Messages
          </button>
        </div>

        {visibleEmails.length === 0 ? (
          <p className="empty-message">No messages in this tab.</p>
        ) : (
          visibleEmails.map((email) => (
            <MessageCard
              key={email.id}
              email={email}
              t={t}
              onAction={handleAction}
            />
          ))
        )}
      </main>

      <Modal
        isOpen={modal.isOpen}
        action={modal.action || undefined}
        onClose={closeModal}
        onSend={handleSendResponse}
        initialText={modal.initialText}
        t={t}
      />
    </div>
  );
};

export default App;
