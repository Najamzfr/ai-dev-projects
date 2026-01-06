import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App Component', () => {
    it('renders without crashing', () => {
        render(<App />);
        // Assuming App has some content, we can check for it.
        // For now, just checking if it renders is enough for a smoke test.
        expect(document.body).toBeDefined();
    });
});
