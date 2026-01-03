import { render, screen } from '@testing-library/react';
import { Recommendation } from '../../src/components/Recommendation';
import { RecommendationResponse } from '../../src/types';

describe('Recommendation Component', () => {
    const mockReco: RecommendationResponse = {
        suggested_move: 'up',
        rationale: 'Best move',
        predicted_grid: [[2, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]]
    };

    test('renders recommendation details', () => {
        render(<Recommendation recommendation={mockReco} />);

        expect(screen.getByText('Suggested')).toBeInTheDocument();
        expect(screen.getByText('UP')).toBeInTheDocument();
        expect(screen.getByText('"Best move"')).toBeInTheDocument();
        // Check if tiles are rendered in mini-grid
        expect(screen.getByText('2')).toBeInTheDocument();
    });
});
