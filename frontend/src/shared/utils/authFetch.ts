export async function authFetch<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("access_token");
  const headers = {
    ...options.headers,
    Authorization: token ? `Bearer ${token}` : "",
    "Content-Type": "application/json",
  };

  const res = await fetch(url, { ...options, headers });
  if (res.status === 401) {
    // handle logout or refresh logic
    throw new Error("Unauthorized");
  }
  return res.json();
}
