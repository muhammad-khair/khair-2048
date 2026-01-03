import { fireEvent, render, screen } from '@testing-library/react';
import { Controls } from '../../src/components/Controls';
import { vi } from 'vitest';

describe('Controls Component', () => {
    const onMoveMock = vi.fn();
    const onRecommendMock = vi.fn();

    test('calls onMove with correct direction', () => {
        render(<Controls onMove={onMoveMock} onRecommend={onRecommendMock} isRecommendLoading={false} disabled={false} />);

        fireEvent.click(screen.getByLabelText('Up'));
        expect(onMoveMock).toHaveBeenCalledWith('up');

        fireEvent.click(screen.getByLabelText('Left'));
        expect(onMoveMock).toHaveBeenCalledWith('left');
    });

    test('calls onRecommend when clicked', () => {
        render(<Controls onMove={onMoveMock} onRecommend={onRecommendMock} isRecommendLoading={false} disabled={false} />);

        const recButton = screen.getByText('Recommend');
        fireEvent.click(recButton);
        expect(onRecommendMock).toHaveBeenCalledTimes(1);
    });

    test('disables recommend button when loading or disabled', () => {
        const { rerender } = render(<Controls onMove={onMoveMock} onRecommend={onRecommendMock} isRecommendLoading={true} disabled={false} />);

        expect(screen.getByText('...')).toBeDisabled();

        rerender(<Controls onMove={onMoveMock} onRecommend={onRecommendMock} isRecommendLoading={false} disabled={true} />);
        expect(screen.getByText('Recommend')).toBeDisabled();
    });
});
