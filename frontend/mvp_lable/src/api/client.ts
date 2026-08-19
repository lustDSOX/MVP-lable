/**
 * Thin API layer. Mock until backend URL is set.
 * VITE_API_BASE_URL + VITE_USE_MOCK=false → real fetch.
 */
const BASE = import.meta.env.VITE_API_BASE_URL || ''
export const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false' || !BASE

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message)
  }
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit & { token?: string | null } = {},
): Promise<T> {
  if (USE_MOCK) {
    throw new ApiError('MOCK_MODE: use Pinia stores', 0)
  }
  const headers: Record<string, string> = {
    Accept: 'application/json',
    ...(options.headers as Record<string, string>),
  }
  if (options.token) headers.Authorization = `Bearer ${options.token}`
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }
  const res = await fetch(`${BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const text = await res.text()
    throw new ApiError(text || res.statusText, res.status)
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}
