export function setAccessToken(accessToken: string) {
  localStorage.setItem('accessToken', accessToken);
}

export function getAccessToken(): string | null {
  return localStorage.getItem('accessToken');
}
