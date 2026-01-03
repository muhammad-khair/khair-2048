import React from 'react';
import { RecommendationResponse } from '../types';
import { Grid } from './Grid';

interface RecommendationProps {
    recommendation: RecommendationResponse;
}

export const Recommendation: React.FC<RecommendationProps> = ({ recommendation }) => {
    return (
        <div className="recommendation-section">
            <div className="recommendation-header">
                <span className="recommend-badge">Suggested</span>
                <span>{recommendation.suggested_move.toUpperCase()}</span>
            </div>
            <p className="rationale-text">"{recommendation.rationale}"</p>
            <div className="mini-grid-wrapper">
                <Grid
                    grid={recommendation.predicted_grid}
                    id="mini-grid" // Optional, just to avoid duplicates
                    className="grid-container"
                />
            </div>
        </div>
    );
};
