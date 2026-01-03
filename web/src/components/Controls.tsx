import React from 'react';

interface ControlsProps {
    onMove: (direction: string) => void;
    onRecommend: () => void;
    isRecommendLoading: boolean;
    disabled: boolean;
}

export const Controls: React.FC<ControlsProps> = ({ onMove, onRecommend, isRecommendLoading, disabled }) => {
    return (
        <div className="controls-outer">
            <div className="arrow-keys-grid">
                <div />
                <button className="control-btn" onClick={() => onMove('up')} aria-label="Up">↑</button>
                <div />
                <button className="control-btn" onClick={() => onMove('left')} aria-label="Left">←</button>
                <button className="control-btn" onClick={() => onMove('down')} aria-label="Down">↓</button>
                <button className="control-btn" onClick={() => onMove('right')} aria-label="Right">→</button>
            </div>
            <div className="recommend-control">
                <button
                    className="recommend-btn"
                    onClick={onRecommend}
                    disabled={isRecommendLoading || disabled}
                >
                    {isRecommendLoading ? '...' : 'Recommend'}
                </button>
            </div>
        </div>
    );
};
