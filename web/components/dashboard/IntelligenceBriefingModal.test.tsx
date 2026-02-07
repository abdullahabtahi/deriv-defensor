
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { IntelligenceBriefingModal } from './IntelligenceBriefingModal';

// Mock localStorage
const localStorageMock = (function () {
    let store: { [key: string]: string } = {};
    return {
        getItem(key: string) {
            return store[key] || null;
        },
        setItem(key: string, value: string) {
            store[key] = value;
        },
        clear() {
            store = {};
        },
        removeItem(key: string) {
            delete store[key];
        },
    };
})();

Object.defineProperty(window, 'localStorage', {
    value: localStorageMock,
});

describe('IntelligenceBriefingModal', () => {
    const mockOnOpenChange = jest.fn();

    beforeEach(() => {
        localStorageMock.clear();
        mockOnOpenChange.mockClear();
        jest.useFakeTimers();
        jest.setSystemTime(new Date('2024-05-20')); // Monday, May 20, 2024
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    it('renders correctly when open', () => {
        render(<IntelligenceBriefingModal open={true} onOpenChange={mockOnOpenChange} />);

        expect(screen.getByText('Daily Intelligence Briefing')).toBeInTheDocument();
        // Check for date format: Monday, May 20, 2024
        expect(screen.getByText(/Monday, May 20, 2024/)).toBeInTheDocument();
        expect(screen.getByText(/Risk Concentration Alert/)).toBeInTheDocument();
    });

    it('does not render when open is false', () => {
        render(<IntelligenceBriefingModal open={false} onOpenChange={mockOnOpenChange} />);

        expect(screen.queryByText('Daily Intelligence Briefing')).not.toBeInTheDocument();
    });

    it('calls onOpenChange(false) and sets localStorage when acknowledged', () => {
        render(<IntelligenceBriefingModal open={true} onOpenChange={mockOnOpenChange} />);

        const acknowledgeButton = screen.getByText('Acknowledge & Close');
        fireEvent.click(acknowledgeButton);

        expect(mockOnOpenChange).toHaveBeenCalledWith(false);
        expect(localStorage.getItem('lastSeenBriefing')).toBe('2024-05-20');
    });
});
