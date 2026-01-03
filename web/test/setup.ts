import '@testing-library/jest-dom';
import {vi} from 'vitest';

// Mock fetch
globalThis.fetch = vi.fn() as any;
