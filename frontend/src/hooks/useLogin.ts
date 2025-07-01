import { useMutation } from "@tanstack/react-query";
import { loginUser } from "@/api/auth";

export function useLogin() {
  const mutation = useMutation({
    mutationKey: ["login"],
    mutationFn: loginUser,
    retry: false, // не повторяем попытку логина автоматически
  });

  const isAuthorized = Boolean(mutation.data?.access_token);

  return {
    status: mutation.status,
    error: mutation.error ?? null,
    isAuthorized,
    login: mutation.mutate,
  };
}
