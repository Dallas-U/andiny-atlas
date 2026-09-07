import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "@tanstack/react-router";

import "./i18n";

import { router } from "./app/router/router";
import {
  AuthProvider,
  useAuth,
} from "./shared/auth/AuthContext";
import { ToastProvider } from "./shared/feedback/ToastContext";

import "./index.css";

function AppRouter() {
  const { isAuthenticated } = useAuth();

  return (
    <RouterProvider
      router={router}
      context={{
        auth: {
          isAuthenticated,
        },
      }}
    />
  );
}

createRoot(
  document.getElementById("root")!,
).render(
  <StrictMode>
    <AuthProvider>
      <ToastProvider>
        <AppRouter />
      </ToastProvider>
    </AuthProvider>
  </StrictMode>,
);