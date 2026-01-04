import React from 'react';

interface ErrorMessageProps {
    message: string;
    onDismiss: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onDismiss }) => {


    return (
        <div className="error-message-container">
            <div className="error-content">
                <span className="error-icon">⚠️</span>
                <span className="error-text">{message}</span>
            </div>
            <button className="error-dismiss-btn" onClick={onDismiss} aria-label="Dismiss">
                ✕
            </button>
        </div>
    );
};
