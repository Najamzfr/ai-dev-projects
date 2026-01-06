import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiClient, ApiError } from '../lib/api-client';

global.fetch = vi.fn();

describe('API Client', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    describe('getLeaderboard', () => {
        it('should fetch leaderboard from the correct URL', async () => {
            const mockResponse = {
                data: [
                    { id: 1, username: 'PLAYER1', score: 250, mode: 'walls', date: '2024-01-15' },
                ],
                meta: { total: 1, limit: 10, offset: 0, has_more: false },
            };

            (fetch as any).mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });

            const result = await apiClient.getLeaderboard();

            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/v1/leaderboard')
            );
            expect(result.data).toEqual(mockResponse.data);
            expect(result.meta).toEqual(mockResponse.meta);
        });

        it('should include query parameters', async () => {
            const mockResponse = {
                data: [],
                meta: { total: 0, limit: 5, offset: 0, has_more: false },
            };

            (fetch as any).mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });

            await apiClient.getLeaderboard(5, 10, 'walls', 'score');

            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('limit=5')
            );
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('offset=10')
            );
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('mode=walls')
            );
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('sort=score')
            );
        });

        it('should throw ApiError on error response', async () => {
            const mockError = {
                error: {
                    code: 'SERVER_ERROR',
                    message: 'Internal server error',
                },
            };

            (fetch as any).mockResolvedValue({
                ok: false,
                status: 500,
                json: async () => mockError,
            });

            await expect(apiClient.getLeaderboard()).rejects.toThrow(ApiError);
        });
    });

    describe('submitScore', () => {
        it('should submit score to the correct URL', async () => {
            const mockResponse = {
                id: 1,
                username: 'PLAYER1',
                score: 250,
                mode: 'walls',
                date: '2024-01-15',
            };

            (fetch as any).mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });

            const result = await apiClient.submitScore({
                username: 'PLAYER1',
                score: 250,
                mode: 'walls',
            });

            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/v1/leaderboard'),
                expect.objectContaining({
                    method: 'POST',
                    body: expect.stringContaining('PLAYER1'),
                })
            );
            expect(result).toEqual(mockResponse);
        });

        it('should throw ApiError on validation error', async () => {
            const mockError = {
                error: {
                    code: 'VALIDATION_ERROR',
                    message: 'Invalid score',
                },
            };

            (fetch as any).mockResolvedValue({
                ok: false,
                status: 400,
                json: async () => mockError,
            });

            await expect(
                apiClient.submitScore({
                    username: 'PLAYER1',
                    score: -1,
                    mode: 'walls',
                })
            ).rejects.toThrow(ApiError);
        });
    });

    describe('getUserScores', () => {
        it('should fetch user scores from the correct URL', async () => {
            const mockResponse = {
                data: [
                    { id: 1, username: 'PLAYER1', score: 250, mode: 'walls', date: '2024-01-15' },
                ],
                meta: { total: 1, limit: 10, offset: 0, has_more: false },
            };

            (fetch as any).mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });

            const result = await apiClient.getUserScores('PLAYER1');

            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/v1/leaderboard/PLAYER1')
            );
            expect(result.data).toEqual(mockResponse.data);
        });
    });

    describe('healthCheck', () => {
        it('should check health endpoint', async () => {
            const mockResponse = {
                status: 'healthy',
                timestamp: '2024-01-15T10:30:00Z',
            };

            (fetch as any).mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });

            const result = await apiClient.healthCheck();

            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('/health')
            );
            expect(result.status).toBe('healthy');
        });
    });
});

