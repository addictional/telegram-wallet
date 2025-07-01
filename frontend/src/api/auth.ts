export async function loginUser(init_data: string) {
  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ init_data }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Login failed");

  localStorage.setItem("access_token", data.access_token); // или sessionStorage
  return data as { access_token: string; [k: string]: unknown };
}
