
import { useEffect, useState } from "react";

// ============================================================
// BACKEND
// ============================================================

const API_BASE_URL = "https://sahayak-backend-vz96.onrender.com";

// ============================================================
// LANGUAGES
// ============================================================

const languages = [
  { name: "English", code: "en" },
  { name: "हिन्दी", code: "hi" },
  { name: "मराठी", code: "mr" },
  { name: "தமிழ்", code: "ta" },
];

// ============================================================
// STAKEHOLDERS
// ============================================================

const stakeholders = [
  "Researcher",
  "Ayurveda Startup / MSME",
  "IP Professional",
  "Student",
  "Institution",
];

// ============================================================
// SUGGESTED QUESTIONS
// ============================================================

const suggestedQuestions = [
  "Can a traditional Ayurvedic formulation be patented?",
  "What is prior art in patent examination?",
  "How is traditional knowledge treated under Indian patent law?",
  "What IP protection is available for an Ayurveda brand?",
];

// ============================================================
// APP
// ============================================================

function App() {

  // ==========================================================
  // QUERY / ANSWER
  // ==========================================================

  const [query, setQuery] = useState("");
  const [language, setLanguage] = useState("English");
  const [stakeholder, setStakeholder] = useState("Researcher");

  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [confidence, setConfidence] = useState("Low");

  const [loading, setLoading] = useState(false);

  // ==========================================================
  // DARK MODE
  // ==========================================================

  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("sahayak-theme") === "dark";
  });

  // ==========================================================
  // SIDEBAR
  // ==========================================================

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [historySearch, setHistorySearch] = useState("");

  // ==========================================================
  // ACCOUNT
  // ==========================================================

  const [currentUser, setCurrentUser] = useState(null);

  const [accessToken, setAccessToken] = useState(() => {
    return localStorage.getItem("sahayak-access-token") || null;
  });

  const [authMode, setAuthMode] = useState(null);
  const [accountOpen, setAccountOpen] = useState(false);

  // ==========================================================
  // AUTH FORM
  // ==========================================================

  const [authName, setAuthName] = useState("");
  const [authEmail, setAuthEmail] = useState("");
  const [authPassword, setAuthPassword] = useState("");

  // const [authError, setAuthError] = useState("");
  // const [authLoading, setAuthLoading] = useState(false);
  //==============================
  const [authError, setAuthError] = useState("");
  const [authSuccess, setAuthSuccess] = useState("");
  const [authLoading, setAuthLoading] = useState(false);

  // ==========================================================
  // CHAT HISTORY
  // ==========================================================

  const [chatHistory, setChatHistory] = useState([]);

  // ==========================================================
  // AUTHORIZATION HEADER
  // ==========================================================

  const getAuthHeaders = () => {

    const token =
      localStorage.getItem(
        "sahayak-access-token"
      );

    return {
      "Content-Type": "application/json",

      ...(token
        ? {
            Authorization: `Bearer ${token}`,
          }
        : {}),
    };
  };

  // ==========================================================
  // GET CURRENT USER
  // ==========================================================

  const getCurrentUser = async () => {

    const token =
      localStorage.getItem(
        "sahayak-access-token"
      );

    if (!token) {
      setCurrentUser(null);
      return;
    }

    try {

      const response = await fetch(
        `${API_BASE_URL}/auth/me`,
        {
          method: "GET",

          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {

        if (
          response.status === 401 ||
          response.status === 403
        ) {

          localStorage.removeItem(
            "sahayak-access-token"
          );

          setAccessToken(null);
          setCurrentUser(null);

        }

        return;
      }

      const data =
        await response.json();

      console.log(
        "Current user:",
        data
      );

      /*
       * Depending on your backend,
       * /auth/me may return:
       *
       * {
       *   id: "...",
       *   name: "...",
       *   email: "..."
       * }
       *
       * OR:
       *
       * {
       *   user: {
       *      id: "...",
       *      name: "...",
       *      email: "..."
       *   }
       * }
       */

      const user =
        data.user || data;

      setCurrentUser(user);

    } catch (error) {

      console.error(
        "Failed to get current user:",
        error
      );

    }

  };

  // ==========================================================
  // LOAD CHATS FROM MONGODB
  // ==========================================================

  const loadChats = async () => {

    const token =
      localStorage.getItem(
        "sahayak-access-token"
      );

    if (!token) {

      setChatHistory([]);

      return;

    }

    try {

      const response = await fetch(
        `${API_BASE_URL}/chats`,
        {
          method: "GET",

          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {

        if (
          response.status === 401 ||
          response.status === 403
        ) {

          localStorage.removeItem(
            "sahayak-access-token"
          );

          setAccessToken(null);
          setCurrentUser(null);
          setChatHistory([]);

        }

        throw new Error(
          `Failed to load chats: ${response.status}`
        );

      }

      const data =
        await response.json();

      console.log(
        "Chats from backend:",
        data
      );

      setChatHistory(
        data.chats || []
      );

    } catch (error) {

      console.error(
        "Failed to load chat history:",
        error
      );

    }

  };

  // ==========================================================
  // INITIAL AUTH CHECK
  // ==========================================================

  useEffect(() => {

    if (accessToken) {

      getCurrentUser();

      loadChats();

    }

  }, [accessToken]);

  // ==========================================================
  // SAVE DARK MODE
  // ==========================================================

  useEffect(() => {

    localStorage.setItem(
      "sahayak-theme",
      darkMode
        ? "dark"
        : "light"
    );

  }, [darkMode]);
//==============================================================================
// ==========================================================
// LOGIN
// ==========================================================

const handleLogin = async (e) => {
  e?.preventDefault();

  setAuthError("");
  setAuthLoading(true);

  try {
    const response = await fetch(
      `${API_BASE_URL}/auth/login`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify({
          email: authEmail.trim().toLowerCase(),
          password: authPassword,
        }),
      }
    );

    const data = await response.json();

    console.log("Login response:", data);

    if (!response.ok) {
      let errorMessage = "Invalid email or password.";

      if (typeof data.detail === "string") {
        errorMessage = data.detail;
      } else if (Array.isArray(data.detail)) {
        errorMessage = data.detail
          .map((item) => {
            if (typeof item === "string") {
              return item;
            }

            return item?.msg || JSON.stringify(item);
          })
          .join(", ");
      } else if (
        data.detail &&
        typeof data.detail === "object"
      ) {
        errorMessage =
          data.detail.message ||
          data.detail.msg ||
          JSON.stringify(data.detail);
      } else if (typeof data.message === "string") {
        errorMessage = data.message;
      }

      throw new Error(errorMessage);
    }

    // ------------------------------------------------------
    // CHECK TOKEN
    // ------------------------------------------------------

    if (!data.access_token) {
      throw new Error(
        "Login succeeded but no access token was returned."
      );
    }

    // ------------------------------------------------------
    // SAVE TOKEN
    // ------------------------------------------------------

    localStorage.setItem(
      "sahayak-access-token",
      data.access_token
    );

    // Also save for API helper functions
    localStorage.setItem(
      "access_token",
      data.access_token
    );

    setAccessToken(data.access_token);

    // ------------------------------------------------------
    // SAVE USER
    // ------------------------------------------------------

    if (data.user) {
      setCurrentUser(data.user);

      localStorage.setItem(
        "user",
        JSON.stringify(data.user)
      );
    }

    // ------------------------------------------------------
    // CLOSE MODAL
    // ------------------------------------------------------

    closeAuth();

    // ------------------------------------------------------
    // GET CURRENT USER
    // ------------------------------------------------------

    try {
      await getCurrentUser();
    } catch (error) {
      console.warn(
        "Could not refresh current user:",
        error
      );
    }

    // ------------------------------------------------------
    // LOAD CHATS
    // ------------------------------------------------------

    try {
      await loadChats();
    } catch (error) {
      console.warn(
        "Could not load chats:",
        error
      );
    }

  } catch (error) {
    console.error("Login error:", error);

    setAuthError(
      error.message || "Login failed."
    );

  } finally {
    setAuthLoading(false);
  }
};
//==============================================================================

//========================================================================
// ==========================================================
// SIGNUP
// ==========================================================

const handleSignup = async (e) => {
  e?.preventDefault();

  setAuthError("");
  setAuthSuccess("");
  setAuthLoading(true);

  // --------------------------------------------------------
  // VALIDATION
  // --------------------------------------------------------

  if (!authName.trim()) {
    setAuthLoading(false);
    setAuthError("Please enter your name.");
    return;
  }

  if (!authEmail.trim()) {
    setAuthLoading(false);
    setAuthError("Please enter your email.");
    return;
  }

  if (!authPassword.trim()) {
    setAuthLoading(false);
    setAuthError("Please enter a password.");
    return;
  }

  if (authPassword.length < 6) {
    setAuthLoading(false);
    setAuthError(
      "Password must contain at least 6 characters."
    );
    return;
  }

  try {
    // ------------------------------------------------------
    // CREATE ACCOUNT
    // ------------------------------------------------------

    const response = await fetch(
      `${API_BASE_URL}/auth/signup`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },

        body: JSON.stringify({
          name: authName.trim(),
          email: authEmail.trim().toLowerCase(),
          password: authPassword,
        }),
      }
    );

    const data = await response.json();

    console.log("Signup response:", data);

    // ------------------------------------------------------
    // HANDLE SIGNUP ERROR
    // ------------------------------------------------------

    if (!response.ok) {
      let errorMessage = "Unable to create account.";

      if (typeof data.detail === "string") {
        errorMessage = data.detail;

      } else if (Array.isArray(data.detail)) {
        errorMessage = data.detail
          .map((item) => {
            if (typeof item === "string") {
              return item;
            }

            return item?.msg || JSON.stringify(item);
          })
          .join(", ");

      } else if (
        data.detail &&
        typeof data.detail === "object"
      ) {
        errorMessage =
          data.detail.message ||
          data.detail.msg ||
          JSON.stringify(data.detail);

      } else if (typeof data.message === "string") {
        errorMessage = data.message;
      }

      throw new Error(errorMessage);
    }

    // ------------------------------------------------------
    // SUCCESS
    // ------------------------------------------------------

    console.log(
      "Account created successfully:",
      data
    );

    const registeredEmail =
      authEmail.trim().toLowerCase();

    // Switch to login
    setAuthMode("login");

    // Keep email
    setAuthEmail(registeredEmail);

    // Clear password
    setAuthPassword("");

    // SUCCESS MESSAGE — green
    setAuthSuccess(
      "Account created successfully! Please log in."
    );

  } catch (error) {

    console.error(
      "Signup error:",
      error
    );

    setAuthError(
      error.message ||
      "Unable to create account."
    );

  } finally {

    setAuthLoading(false);
  }
};
//========================================================================
//   // ==========================================================
//   // SIGNUP
//   // ==========================================================
// const handleSignup = async () => {
//   setAuthError("");

//   if (!authName.trim()) {
//     setAuthError("Please enter your name.");
//     return;
//   }

//   if (!authEmail.trim()) {
//     setAuthError("Please enter your email.");
//     return;
//   }

//   if (!authPassword.trim()) {
//     setAuthError("Please enter a password.");
//     return;
//   }

//   if (authPassword.length < 6) {
//     setAuthError(
//       "Password must contain at least 6 characters."
//     );
//     return;
//   }

//   try {
//     const res = await fetch(
//       `${API_BASE_URL}/auth/signup`,
//       {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           name: authName.trim(),
//           email: authEmail.trim(),
//           password: authPassword,
//         }),
//       }
//     );

//     const data = await res.json();

//     if (!res.ok) {
//       throw new Error(
//         typeof data.detail === "string"
//           ? data.detail
//           : "Signup failed."
//       );
//     }

//     console.log("Signup successful:", data);

//     // Switch to login after successful registration
//     setAuthMode("login");

//     // Keep email so the user doesn't need to type it again
//     setAuthEmail(authEmail.trim());
//     setAuthPassword("");

//     setAuthError(
//       "Account created successfully. Please log in."
//     );

//   } catch (error) {
//     console.error("Signup error:", error);

//     setAuthError(
//       error.message || "Unable to create account."
//     );
//   }
// };
  

  // ==========================================================
  // LOGOUT
  // ==========================================================

  const handleLogout = () => {

    localStorage.removeItem(
      "sahayak-access-token"
    );

    setAccessToken(null);
    setCurrentUser(null);

    setChatHistory([]);

    setAccountOpen(false);

    setQuery("");
    setAnswer("");
    setSources([]);
    setConfidence("Low");

    setSidebarOpen(false);

  };

  // ==========================================================
  // CLOSE AUTH
  // ==========================================================

  const closeAuth = () => {

    setAuthMode(null);

    setAuthName("");
    setAuthEmail("");
    setAuthPassword("");

    setAuthError("");

  };

  // ==========================================================
  // ASK SAHAYAK
  // ==========================================================

  const askSahayak = async () => {

    if (
      !query.trim() ||
      loading
    ) {

      return;

    }

    /*
     * Login is required because the backend associates
     * the generated chat with the authenticated user.
     */

    const token =
      localStorage.getItem(
        "sahayak-access-token"
      );

    if (!token) {

      setAuthMode("login");

      setAuthError(
        "Please log in before asking Sahayak."
      );

      return;

    }

    const currentQuery =
      query.trim();

    setLoading(true);

    setAnswer("");
    setSources([]);
    setConfidence("Low");

    try {

      const response = await fetch(
        `${API_BASE_URL}/query`,
        {
          method: "POST",

          headers: getAuthHeaders(),

          body: JSON.stringify({

            query:
              currentQuery,

            language:
              language,

            stakeholder:
              stakeholder,

          }),

        }
      );

      const data =
        await response.json();

      console.log(
        "Sahayak response:",
        data
      );
      console.log(
        "FULL Sahayak response:",
        JSON.stringify(data, null, 2)
      );

      console.log("Answer:", data?.answer);
      console.log("Sources:", data?.sources);
      console.log("Evidence:", data?.evidence);
      console.log("Confidence:", data?.confidence);
      console.log("Status:", response.status);

      if (!response.ok) {

        if (
          response.status === 401 ||
          response.status === 403
        ) {

          handleLogout();

          throw new Error(
            "Your session has expired. Please log in again."
          );

        }

        throw new Error(
          data.detail ||
          data.message ||
          `Backend error: ${response.status}`
        );

      }

      const generatedAnswer =
        data.answer ||
        "No answer received from Sahayak.";

      const retrievedSources =
        data.sources || [];

      const retrievedConfidence =
        data.confidence || "Low";

      setAnswer(
        generatedAnswer
      );

      setSources(
        retrievedSources
      );

      setConfidence(
        retrievedConfidence
      );

      /*
       * IMPORTANT:
       *
       * Do NOT generate:
       *
       * id: Date.now()
       *
       * The backend/MongoDB owns the chat ID.
       */

      const backendChatId =
        data.chat_id ||
        data.id;

      /*
       * Refresh history directly from MongoDB.
       *
       * This ensures the sidebar represents backend
       * data rather than frontend-only data.
       */

      await loadChats();

      /*
       * If the backend returns no chat_id, we still show
       * the answer, but log a warning.
       */

      if (!backendChatId) {

        console.warn(
          "Backend did not return chat_id."
        );

      }

    } catch (error) {

      console.error(
        "Sahayak backend error:",
        error
      );

      /*
       * Don't replace a meaningful backend answer
       * if one was already successfully received.
       */

      if (!answer) {

        setAnswer(
          `⚠️ ${error.message || "Could not connect to the Sahayak backend."}`
        );

      }

      setSources([]);

      setConfidence("Low");

    } finally {

      setLoading(false);

    }

  };

  // ==========================================================
  // ENTER KEY
  // ==========================================================

  const handleKeyDown = (e) => {

    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {

      e.preventDefault();

      askSahayak();

    }

  };

  // ==========================================================
  // LOAD COMPLETE CHAT
  // ==========================================================

  const loadChat = async (chatId) => {

    if (!chatId) {

      console.error(
        "Chat ID is missing."
      );

      return;

    }

    const token =
      localStorage.getItem(
        "sahayak-access-token"
      );

    if (!token) {

      setAuthMode("login");

      return;

    }

    try {

      setLoading(true);

      const response = await fetch(
        `${API_BASE_URL}/chats/${chatId}`,
        {
          method: "GET",

          headers: {
            Authorization:
              `Bearer ${token}`,
          },
        }
      );

      const data =
        await response.json();

      console.log(
        "Complete chat:",
        data
      );

      if (!response.ok) {

        if (
          response.status === 401 ||
          response.status === 403
        ) {

          handleLogout();

          throw new Error(
            "Your session has expired."
          );

        }

        throw new Error(
          data.detail ||
          data.message ||
          `Failed to load chat: ${response.status}`
        );

      }

      setQuery(
        data.query || ""
      );

      setAnswer(
        data.answer || ""
      );

      setSources(
        data.sources || []
      );

      setConfidence(
        data.confidence || "Low"
      );

      setLanguage(
        data.language || "English"
      );

      setStakeholder(
        data.stakeholder ||
        "Researcher"
      );

      setSidebarOpen(false);

    } catch (error) {

      console.error(
        "Failed to load chat:",
        error
      );

    } finally {

      setLoading(false);

    }

  };

  // ==========================================================
  // NEW CHAT
  // ==========================================================

  const newChat = () => {

    setQuery("");
    setAnswer("");
    setSources([]);
    setConfidence("Low");

    setLoading(false);

    setSidebarOpen(false);

  };

  // ==========================================================
  // DELETE CHAT
  // ==========================================================

  const deleteChat = (
    id,
    e
  ) => {

    /*
     * Your currently tested backend endpoints do not include
     * DELETE /chats/{chat_id}.
     *
     * Therefore we do NOT pretend to delete it from MongoDB.
     *
     * Once you create a backend delete endpoint, connect it here.
     */

    e.stopPropagation();

    console.warn(
      "Delete is not connected to the backend yet."
    );

  };

  // ==========================================================
  // CLEAR HISTORY
  // ==========================================================

  const clearHistory = () => {

    /*
     * Same situation:
     *
     * MongoDB history should not be cleared only in React.
     *
     * You need a backend DELETE endpoint for this.
     */

    window.alert(
      "Clear history requires a backend delete endpoint. Your MongoDB chats are currently preserved."
    );

  };

  // ==========================================================
  // FILTER HISTORY
  // ==========================================================

  const filteredHistory =
    chatHistory.filter(
      (chat) => {

        const title =
          chat.title ||
          chat.query ||
          "";

        return title
          .toLowerCase()
          .includes(
            historySearch
              .toLowerCase()
          );

      }
    );

  // ==========================================================
  // PLACEHOLDER
  // ==========================================================

  const getPlaceholder = () => {

    switch (language) {

      case "हिन्दी":

        return "अपना प्रश्न पूछें...";

      case "मराठी":

        return "तुमचा प्रश्न विचारा...";

      case "தமிழ்":

        return "உங்கள் கேள்வியை கேளுங்கள்...";

      default:

        return "Example: Can a traditional Ayurvedic formulation be patented?";

    }

  };

  // ==========================================================
  // CONFIDENCE STYLE
  // ==========================================================

  const confidenceClass = () => {

    if (
      confidence === "High"
    ) {

      return "bg-emerald-100 text-emerald-700";

    }

    if (
      confidence === "Medium"
    ) {

      return "bg-amber-100 text-amber-700";

    }

    return "bg-red-100 text-red-700";

  };

  // ==========================================================
  // RETURN UI
  // ==========================================================

  return (

    <div
      className={
        darkMode
          ? "min-h-screen bg-slate-950 text-slate-100"
          : "min-h-screen bg-slate-50 text-slate-900"
      }
    >

      {/* ====================================================
          MOBILE OVERLAY
      ==================================================== */}

      {sidebarOpen && (

        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() =>
            setSidebarOpen(false)
          }
        />

      )}

      {/* ====================================================
          SIDEBAR
      ==================================================== */}

      <aside
        className={`
          fixed left-0 top-0 z-50 h-screen w-80
          border-r
          transition-transform duration-300
          ${
            darkMode
              ? "border-slate-800 bg-slate-900"
              : "border-slate-200 bg-white"
          }
          ${
            sidebarOpen
              ? "translate-x-0"
              : "-translate-x-full"
          }
          lg:translate-x-0
        `}
      >

        {/* Sidebar Header */}

        <div className="flex h-20 items-center justify-between border-b border-inherit px-5">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100 text-xl">
              🌿
            </div>

            <div>

              <h2
                className={`font-bold ${
                  darkMode
                    ? "text-white"
                    : "text-emerald-900"
                }`}
              >
                Sahayak
              </h2>

              <p className="text-xs text-slate-500">
                Chat History
              </p>

            </div>

          </div>

          <button
            onClick={() =>
              setSidebarOpen(false)
            }
            className="text-slate-400 hover:text-slate-700 lg:hidden"
          >
            ✕
          </button>

        </div>

        {/* New Chat */}

        <div className="p-4">

          <button
            onClick={newChat}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-700 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800"
          >

            <span className="text-lg">
              +
            </span>

            New Chat

          </button>

        </div>

        {/* Search */}

        <div className="px-4 pb-4">

          <div
            className={`flex items-center gap-2 rounded-xl border px-3 py-2 ${
              darkMode
                ? "border-slate-700 bg-slate-800"
                : "border-slate-200 bg-slate-50"
            }`}
          >

            <span className="text-slate-400">
              🔍
            </span>

            <input
              value={historySearch}
              onChange={(e) =>
                setHistorySearch(
                  e.target.value
                )
              }
              placeholder="Search chats..."
              className={`w-full bg-transparent text-sm outline-none ${
                darkMode
                  ? "text-white placeholder:text-slate-500"
                  : "text-slate-700 placeholder:text-slate-400"
              }`}
            />

          </div>

        </div>

        {/* History */}

        <div className="h-[calc(100vh-190px)] overflow-y-auto px-3">

          {filteredHistory.length === 0 ? (

            <div className="px-3 py-10 text-center">

              <div className="text-3xl">
                💬
              </div>

              <p
                className={`mt-3 text-sm font-medium ${
                  darkMode
                    ? "text-slate-300"
                    : "text-slate-700"
                }`}
              >
                No conversations yet
              </p>

              <p className="mt-1 text-xs text-slate-500">
                Your questions will appear here.
              </p>

            </div>

          ) : (

            <div className="space-y-2">

              {filteredHistory.map(
                (chat, index) => (

                  <div
                    key={
                      chat.id ||
                      chat.chat_id ||
                      index
                    }
                    onClick={() =>
                      loadChat(
                        chat.id ||
                        chat.chat_id
                      )
                    }
                    className={`group cursor-pointer rounded-xl p-3 transition ${
                      darkMode
                        ? "hover:bg-slate-800"
                        : "hover:bg-slate-100"
                    }`}
                  >

                    <div className="flex items-start gap-3">

                      <span className="mt-1 text-sm">
                        💬
                      </span>

                      <div className="min-w-0 flex-1">

                        <p
                          className={`truncate text-sm font-medium ${
                            darkMode
                              ? "text-slate-200"
                              : "text-slate-700"
                          }`}
                        >

                          {chat.title ||
                            chat.query ||
                            "Untitled chat"}

                        </p>

                        <p className="mt-1 text-[10px] text-slate-500">

                          {chat.created_at ||
                            chat.timestamp ||
                            ""}

                        </p>

                      </div>

                      <button
                        onClick={(e) =>
                          deleteChat(
                            chat.id ||
                            chat.chat_id,
                            e
                          )
                        }
                        className="hidden text-xs text-slate-400 hover:text-red-500 group-hover:block"
                        title="Delete chat"
                      >
                        🗑️
                      </button>

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

        {/* Clear */}

        {chatHistory.length > 0 && (

          <div className="absolute bottom-0 left-0 right-0 border-t border-inherit bg-inherit p-4">

            <button
              onClick={clearHistory}
              className="w-full rounded-lg px-3 py-2 text-xs font-medium text-slate-500 transition hover:bg-red-50 hover:text-red-600"
            >
              🗑️ Clear all history
            </button>

          </div>

        )}

      </aside>

      {/* ====================================================
          MAIN
      ==================================================== */}

      <div className="lg:pl-80">

        {/* ==================================================
            HEADER
        ================================================== */}

        <header
          className={`sticky top-0 z-30 border-b backdrop-blur ${
            darkMode
              ? "border-slate-800 bg-slate-950/90"
              : "border-slate-200 bg-white/90"
          }`}
        >

          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

            {/* LEFT */}

            <div className="flex items-center gap-3">

              <button
                onClick={() =>
                  setSidebarOpen(true)
                }
                className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden"
              >
                ☰
              </button>

              <div className="hidden sm:block">

                <p
                  className={`text-sm font-semibold ${
                    darkMode
                      ? "text-white"
                      : "text-slate-800"
                  }`}
                >
                  Ayurveda IP & Regulation
                </p>

                <p className="text-xs text-slate-500">
                  Evidence-grounded AI assistant
                </p>

              </div>

            </div>

            {/* RIGHT */}

            <div className="flex items-center gap-3">

              {/* AI STATUS */}

              <div className="hidden items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 sm:flex">

                <span className="h-2 w-2 rounded-full bg-emerald-500"></span>

                AI Assistant

              </div>

              {/* LANGUAGE */}

              <select
                value={language}
                onChange={(e) =>
                  setLanguage(
                    e.target.value
                  )
                }
                className={`rounded-lg border px-3 py-2 text-sm font-medium outline-none ${
                  darkMode
                    ? "border-slate-700 bg-slate-900 text-slate-200"
                    : "border-slate-300 bg-white text-slate-700"
                }`}
              >

                {languages.map(
                  (lang) => (

                    <option
                      key={lang.code}
                      value={lang.name}
                    >
                      {lang.name}
                    </option>

                  )
                )}

              </select>

              {/* DARK MODE */}

              <button
                onClick={() =>
                  setDarkMode(
                    !darkMode
                  )
                }
                title={
                  darkMode
                    ? "Switch to light mode"
                    : "Switch to dark mode"
                }
                className={`flex h-10 w-10 items-center justify-center rounded-xl border transition ${
                  darkMode
                    ? "border-slate-700 bg-slate-900 hover:bg-slate-800"
                    : "border-slate-200 bg-white hover:bg-slate-100"
                }`}
              >

                {darkMode
                  ? "☀️"
                  : "🌙"}

              </button>

              {/* =================================================
                  ACCOUNT
              ================================================= */}

              <div className="relative">

                <button
                  onClick={() =>
                    setAccountOpen(
                      !accountOpen
                    )
                  }
                  className={`flex items-center gap-2 rounded-xl border px-3 py-2 text-sm font-medium transition ${
                    darkMode
                      ? "border-slate-700 bg-slate-900 hover:bg-slate-800"
                      : "border-slate-200 bg-white hover:bg-slate-100"
                  }`}
                >

                  <div className="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-100 text-sm">

                    {currentUser
                      ? (
                          currentUser.name ||
                          currentUser.email ||
                          "U"
                        )
                          .charAt(0)
                          .toUpperCase()
                      : "👤"}

                  </div>

                  <span className="hidden md:block">

                    {currentUser
                      ? currentUser.name ||
                        currentUser.email
                      : "Account"}

                  </span>

                  <span className="text-xs">
                    ▾
                  </span>

                </button>

                {/* ACCOUNT MENU */}

                {accountOpen && (

                  <div
                    className={`absolute right-0 mt-2 w-64 overflow-hidden rounded-xl border shadow-xl ${
                      darkMode
                        ? "border-slate-700 bg-slate-900"
                        : "border-slate-200 bg-white"
                    }`}
                  >

                    {currentUser ? (

                      <>

                        <div className="border-b border-inherit p-4">

                          <p
                            className={`font-semibold ${
                              darkMode
                                ? "text-white"
                                : "text-slate-900"
                            }`}
                          >
                            {currentUser.name ||
                              "User"}
                          </p>

                          <p className="mt-1 break-all text-xs text-slate-500">
                            {currentUser.email}
                          </p>

                        </div>

                        <button
                          onClick={
                            handleLogout
                          }
                          className="w-full px-4 py-3 text-left text-sm text-red-600 hover:bg-red-50"
                        >
                          🚪 Log out
                        </button>

                      </>

                    ) : (

                      <>

                        <div className="p-4">

                          <p
                            className={`font-semibold ${
                              darkMode
                                ? "text-white"
                                : "text-slate-900"
                            }`}
                          >
                            Welcome to Sahayak
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            Sign in to save and manage your chats.
                          </p>

                        </div>

                        <div className="border-t border-inherit p-3">

                          <button
                            onClick={() => {

                              setAuthMode(
                                "login"
                              );

                              setAuthError("");

                              setAccountOpen(
                                false
                              );

                            }}
                            className="mb-2 w-full rounded-lg bg-emerald-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-emerald-800"
                          >
                            Log in
                          </button>

                          <button
                            onClick={() => {

                              setAuthMode(
                                "signup"
                              );

                              setAuthError("");

                              setAccountOpen(
                                false
                              );

                            }}
                            className={`w-full rounded-lg border px-4 py-2.5 text-sm font-semibold ${
                              darkMode
                                ? "border-slate-700 text-slate-200 hover:bg-slate-800"
                                : "border-slate-200 text-slate-700 hover:bg-slate-50"
                            }`}
                          >
                            Sign up
                          </button>

                        </div>

                      </>

                    )}

                  </div>

                )}

              </div>

            </div>

          </div>

        </header>

        {/* ==================================================
            MAIN CONTENT
        ================================================== */}

        <main className="mx-auto max-w-6xl px-6 py-12">

          {/* HERO */}

          <section className="mx-auto max-w-4xl text-center">

            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-xs font-semibold text-emerald-700">

              <span>✦</span>

              Multilingual

              <span className="text-emerald-300">
                •
              </span>

              Evidence-Grounded

              <span className="text-emerald-300">
                •
              </span>

              Citation-Backed

            </div>

            <h1
              className={`mt-7 text-4xl font-extrabold tracking-tight sm:text-5xl ${
                darkMode
                  ? "text-white"
                  : "text-slate-900"
              }`}
            >

              Your AI Assistant for

              <span className="block text-emerald-600">
                Ayurveda IP & Regulation
              </span>

            </h1>

            <p
              className={`mx-auto mt-6 max-w-2xl text-base leading-7 sm:text-lg ${
                darkMode
                  ? "text-slate-400"
                  : "text-slate-600"
              }`}
            >
              Ask questions about patents, traditional knowledge,
              regulations and Ayurveda-related intellectual property.

              Sahayak retrieves relevant authoritative sources and
              explains them with traceable citations.
            </p>

          </section>

          {/* ==================================================
              ASK CARD
          ================================================== */}

          <section className="mx-auto mt-10 max-w-4xl">

            <div
              className={`rounded-2xl border p-6 shadow-lg ${
                darkMode
                  ? "border-slate-800 bg-slate-900 shadow-black/20"
                  : "border-slate-200 bg-white shadow-slate-200/40"
              }`}
            >

              <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

                <div>

                  <h2
                    className={`text-lg font-bold ${
                      darkMode
                        ? "text-white"
                        : "text-slate-900"
                    }`}
                  >
                    Ask Sahayak
                  </h2>

                  <p className="mt-1 text-xs text-slate-500">
                    Get an evidence-grounded answer.
                  </p>

                </div>

                {/* STAKEHOLDER */}

                <div className="flex items-center gap-2">

                  <span className="text-xs text-slate-500">
                    I am a
                  </span>

                  <select
                    value={stakeholder}
                    onChange={(e) =>
                      setStakeholder(
                        e.target.value
                      )
                    }
                    className={`rounded-lg border px-3 py-2 text-xs font-medium outline-none ${
                      darkMode
                        ? "border-slate-700 bg-slate-800 text-slate-200"
                        : "border-slate-300 bg-white text-slate-700"
                    }`}
                  >

                    {stakeholders.map(
                      (role) => (

                        <option
                          key={role}
                        >
                          {role}
                        </option>

                      )
                    )}

                  </select>

                </div>

              </div>

              {/* QUERY */}

              <textarea
                value={query}
                onChange={(e) =>
                  setQuery(
                    e.target.value
                  )
                }
                onKeyDown={
                  handleKeyDown
                }
                rows={5}
                placeholder={
                  getPlaceholder()
                }
                className={`w-full resize-none rounded-xl border p-4 text-sm leading-7 outline-none transition ${
                  darkMode
                    ? "border-slate-700 bg-slate-800 text-white placeholder:text-slate-500 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10"
                    : "border-slate-200 bg-slate-50 text-slate-800 placeholder:text-slate-400 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-50"
                }`}
              />

              <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

                <div className="text-xs text-slate-500">

                  🌐 {language}

                  <span className="mx-2">
                    •
                  </span>

                  👤 {stakeholder}

                </div>

                <button
                  onClick={
                    askSahayak
                  }
                  disabled={
                    loading ||
                    !query.trim()
                  }
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-700 px-6 py-3 text-sm font-semibold text-white shadow-md transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-50"
                >

                  {loading ? (

                    <>

                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>

                      Researching...

                    </>

                  ) : (

                    <>

                      Ask Sahayak

                      <span className="text-lg">
                        →
                      </span>

                    </>

                  )}

                </button>

              </div>

            </div>

          </section>

          {/* ==================================================
              LOADING
          ================================================== */}

          {loading && (

            <section className="mx-auto mt-8 max-w-4xl">

              <div
                className={`rounded-2xl border p-6 ${
                  darkMode
                    ? "border-slate-800 bg-slate-900"
                    : "border-slate-200 bg-white"
                }`}
              >

                <div className="flex items-center gap-4">

                  <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-300 border-t-emerald-700"></div>

                  <div>

                    <h3 className="font-semibold">
                      Sahayak is researching...
                    </h3>

                    <p className="mt-1 text-sm text-slate-500">
                      Searching authoritative sources and
                      preparing your response.
                    </p>

                  </div>

                </div>

              </div>

            </section>

          )}

          {/* ==================================================
              ANSWER
          ================================================== */}

          {answer &&
            !loading && (

              <section className="mx-auto mt-8 max-w-4xl">

                <div
                  className={`overflow-hidden rounded-2xl border shadow-lg ${
                    darkMode
                      ? "border-slate-800 bg-slate-900"
                      : "border-slate-200 bg-white"
                  }`}
                >

                  <div
                    className={`flex flex-col gap-4 border-b px-6 py-5 sm:flex-row sm:items-center sm:justify-between ${
                      darkMode
                        ? "border-slate-800 bg-slate-800/50"
                        : "border-slate-100 bg-slate-50/70"
                    }`}
                  >

                    <div className="flex items-center gap-3">

                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100 text-lg text-emerald-700">
                        ✓
                      </div>

                      <div>

                        <h2 className="font-bold">
                          Sahayak's Answer
                        </h2>

                        <p className="text-xs text-slate-500">
                          Generated using retrieved evidence
                        </p>

                      </div>

                    </div>

                    <div className="flex items-center gap-2">

                      <span className="text-xs text-slate-500">
                        Evidence confidence
                      </span>

                      <span
                        className={`rounded-full px-3 py-1 text-xs font-bold ${confidenceClass()}`}
                      >
                        {confidence}
                      </span>

                    </div>

                  </div>

                  <div className="px-6 py-7">

                    <p
                      className={`whitespace-pre-line text-sm leading-8 ${
                        darkMode
                          ? "text-slate-300"
                          : "text-slate-600"
                      }`}
                    >
                      {answer}
                    </p>

                  </div>

                </div>

              </section>

            )}

          {/* ==================================================
              SOURCES
          ================================================== */}

          {sources.length > 0 &&
            !loading && (

              <section className="mx-auto mt-10 max-w-4xl">

                <div className="mb-5 flex items-end justify-between">

                  <div>

                    <h2
                      className={`text-xl font-bold ${
                        darkMode
                          ? "text-white"
                          : "text-slate-900"
                      }`}
                    >
                      Evidence & Sources
                    </h2>

                    <p
                      className={`mt-1 text-sm ${
                        darkMode
                          ? "text-slate-400"
                          : "text-slate-500"
                      }`}
                    >
                      Sources used to ground the response
                    </p>

                  </div>

                  <span
                    className={`rounded-full px-3 py-1 text-xs font-medium ${
                      darkMode
                        ? "bg-slate-800 text-slate-300"
                        : "bg-slate-100 text-slate-600"
                    }`}
                  >
                    {sources.length} source
                    {sources.length !== 1
                      ? "s"
                      : ""}
                  </span>

                </div>

                {/* SOURCE GRID */}

                <div className="grid gap-4 md:grid-cols-3">

                  {sources.map(
                    (source, index) => (

                      <div
                        key={
                          source.id ||
                          index
                        }
                        className={`group flex min-h-[230px] flex-col rounded-xl border p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:border-emerald-300 hover:shadow-md ${
                          darkMode
                            ? "border-slate-800 bg-slate-900"
                            : "border-slate-200 bg-white"
                        }`}
                      >

                        {/* TOP */}

                        <div className="flex items-center justify-between gap-3">

                          <span
                            className={`rounded-lg px-2 py-1 text-xs font-bold ${
                              darkMode
                                ? "bg-slate-800 text-slate-300"
                                : "bg-slate-100 text-slate-500"
                            }`}
                          >
                            [
                            {source.id ||
                              index +
                                1}
                            ]
                          </span>

                          <span className="text-right text-[10px] font-bold uppercase tracking-wide text-emerald-600">
                            {source.type ||
                              "Official Source"}
                          </span>

                        </div>

                        {/* DOCUMENT TITLE */}

                        <h3
                          className={`mt-4 break-words font-bold ${
                            darkMode
                              ? "text-white"
                              : "text-slate-900"
                          }`}
                        >
                          {source.document_title ||
                            source.source_name ||
                            source.title ||
                            "Unknown Source"}
                        </h3>

                        {/* ORGANIZATION */}

                        {source.organization && (

                          <p
                            className={`mt-1 text-xs ${
                              darkMode
                                ? "text-slate-400"
                                : "text-slate-500"
                            }`}
                          >
                            {source.organization}
                          </p>

                        )}

                        {/* DESCRIPTION */}

                        {source.description && (

                          <p
                            className={`mt-3 line-clamp-3 text-sm leading-6 ${
                              darkMode
                                ? "text-slate-400"
                                : "text-slate-500"
                            }`}
                          >
                            {source.description}
                          </p>

                        )}

                        {/* PAGE */}

                        {source.page && (

                          <div
                            className={`mt-4 text-xs ${
                              darkMode
                                ? "text-slate-500"
                                : "text-slate-400"
                            }`}
                          >
                            📄 {source.page}
                          </div>

                        )}

                        {/* URL */}

                        <div className="mt-auto pt-5">

                          {source.source_url ? (

                            <a
                              href={
                                source.source_url
                              }
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-block text-xs font-semibold text-emerald-600 transition hover:text-emerald-800 hover:underline"
                            >
                              View source →
                            </a>

                          ) : (

                            <span
                              className={`inline-block text-xs ${
                                darkMode
                                  ? "text-slate-500"
                                  : "text-slate-400"
                              }`}
                            >
                              Source URL unavailable
                            </span>

                          )}

                        </div>

                      </div>

                    )
                  )}

                </div>

              </section>

            )}

          {/* ==================================================
              SUGGESTED QUESTIONS
          ================================================== */}

          <section className="mx-auto mt-14 max-w-4xl">

            <h2
              className={`text-xl font-bold ${
                darkMode
                  ? "text-white"
                  : "text-slate-900"
              }`}
            >
              Explore Sahayak
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Start with one of these questions
            </p>

            <div className="mt-5 grid gap-3 sm:grid-cols-2">

              {suggestedQuestions.map(
                (
                  question,
                  index
                ) => (

                  <button
                    key={index}
                    onClick={() =>
                      setQuery(
                        question
                      )
                    }
                    className={`group flex items-center gap-3 rounded-xl border p-4 text-left text-sm transition ${
                      darkMode
                        ? "border-slate-800 bg-slate-900 text-slate-300 hover:border-emerald-700 hover:bg-slate-800"
                        : "border-slate-200 bg-white text-slate-600 hover:border-emerald-300 hover:bg-emerald-50"
                    }`}
                  >

                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-100">
                      {
                        [
                          "⚖️",
                          "🔎",
                          "📚",
                          "™️",
                        ][index]
                      }
                    </span>

                    <span className="flex-1">
                      {question}
                    </span>

                    <span className="text-slate-400">
                      →
                    </span>

                  </button>

                )
              )}

            </div>

          </section>

          {/* ==================================================
              HOW IT WORKS
          ================================================== */}

          <section className="mx-auto mt-14 max-w-4xl">

            <div
              className={`rounded-2xl border p-7 ${
                darkMode
                  ? "border-emerald-900/50 bg-emerald-950/20"
                  : "border-emerald-100 bg-emerald-50/60"
              }`}
            >

              <div className="text-center">

                <h2
                  className={`text-xl font-bold ${
                    darkMode
                      ? "text-white"
                      : "text-slate-900"
                  }`}
                >
                  How Sahayak works
                </h2>

                <p className="mt-2 text-sm text-slate-500">
                  From your question to an evidence-backed answer
                </p>

              </div>

              <div className="mt-8 grid gap-8 sm:grid-cols-4">

                <Step
                  number="01"
                  icon="💬"
                  title="Ask"
                  text="Ask your IP or Ayurveda regulation question."
                />

                <Step
                  number="02"
                  icon="🔎"
                  title="Retrieve"
                  text="Relevant information is retrieved from authoritative sources."
                />

                <Step
                  number="03"
                  icon="🧠"
                  title="Reason"
                  text="AI processes the retrieved evidence."
                />

                <Step
                  number="04"
                  icon="📑"
                  title="Cite"
                  text="Supporting sources are shown for verification."
                />

              </div>

            </div>

          </section>

          {/* ==================================================
              DISCLAIMER
          ================================================== */}

          <section className="mx-auto mt-10 max-w-4xl">

            <div className="flex gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4">

              <div>
                ⚠️
              </div>

              <div>

                <p className="text-sm font-semibold text-amber-900">
                  Important
                </p>

                <p className="mt-1 text-xs leading-5 text-amber-800">
                  Sahayak provides information based on available
                  authoritative sources. It is intended for research
                  and informational purposes and does not constitute
                  legal, medical, or professional advice.
                </p>

              </div>

            </div>

          </section>

        </main>

        {/* ==================================================
            FOOTER
        ================================================== */}

        <footer
          className={`border-t ${
            darkMode
              ? "border-slate-800 bg-slate-950"
              : "border-slate-200 bg-white"
          }`}
        >

          <div className="mx-auto flex max-w-6xl flex-col gap-2 px-6 py-6 text-center text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">

            <div className="font-medium text-emerald-600">
              🌿 Sahayak
            </div>

            <div>
              AI Assistant for Ayurveda IP & Regulation
            </div>

            <div>
              © 2026
            </div>

          </div>

        </footer>

      </div>

      {/* ======================================================
          LOGIN / SIGNUP MODAL
      ====================================================== */}

      {authMode && (

        <div
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 px-4"
          onClick={closeAuth}
        >

          <div
            onClick={(e) =>
              e.stopPropagation()
            }
            className={`w-full max-w-md rounded-2xl border p-7 shadow-2xl ${
              darkMode
                ? "border-slate-700 bg-slate-900"
                : "border-slate-200 bg-white"
            }`}
          >

            {/* MODAL HEADER */}

            <div className="flex items-start justify-between">

              <div>

                <div className="flex items-center gap-3">

                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-100 text-xl">
                    🌿
                  </div>

                  <div>

                    <h2
                      className={`text-xl font-bold ${
                        darkMode
                          ? "text-white"
                          : "text-slate-900"
                      }`}
                    >
                      {authMode === "login"
                        ? "Welcome back"
                        : "Create your account"}
                    </h2>

                    <p className="mt-1 text-xs text-slate-500">

                      {authMode === "login"
                        ? "Log in to continue using Sahayak."
                        : "Create an account to save your conversations."}

                    </p>

                  </div>

                </div>

              </div>

              <button
                onClick={closeAuth}
                className="text-slate-400 hover:text-slate-700"
              >
                ✕
              </button>

            </div>

            {/* ERROR */}

            {authError && (
              <div className="mt-5 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-xs text-red-700">
                ⚠️ {authError}
              </div>
            )}

            {authSuccess && (
              <div className="mt-5 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-xs text-emerald-700">
                ✅ {authSuccess}
              </div>
            )}
            {/* {authError && (

              <div className="mt-5 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-xs text-red-700">
                ⚠️ {authError}
              </div>

            )} */}

            {/* NAME */}

            {authMode === "signup" && (

              <div className="mt-5">

                <label className="mb-2 block text-xs font-semibold text-slate-500">
                  Full name
                </label>

                <input
                  type="text"
                  value={authName}
                  onChange={(e) =>
                    setAuthName(
                      e.target.value
                    )
                  }
                  placeholder="Enter your name"
                  className={`w-full rounded-xl border px-4 py-3 text-sm outline-none focus:border-emerald-500 ${
                    darkMode
                      ? "border-slate-700 bg-slate-800 text-white"
                      : "border-slate-200 bg-slate-50 text-slate-800"
                  }`}
                />

              </div>

            )}

            {/* EMAIL */}

            <div className="mt-5">

              <label className="mb-2 block text-xs font-semibold text-slate-500">
                Email
              </label>

              <input
                type="email"
                value={authEmail}
                onChange={(e) =>
                  setAuthEmail(
                    e.target.value
                  )
                }
                placeholder="you@example.com"
                className={`w-full rounded-xl border px-4 py-3 text-sm outline-none focus:border-emerald-500 ${
                  darkMode
                    ? "border-slate-700 bg-slate-800 text-white"
                    : "border-slate-200 bg-slate-50 text-slate-800"
                }`}
              />

            </div>

            {/* PASSWORD */}

            <div className="mt-5">

              <label className="mb-2 block text-xs font-semibold text-slate-500">
                Password
              </label>

              <input
                type="password"
                value={authPassword}
                onChange={(e) =>
                  setAuthPassword(
                    e.target.value
                  )
                }
                onKeyDown={(e) => {

                  if (
                    e.key === "Enter"
                  ) {

                    if (
                      authMode ===
                      "login"
                    ) {

                      handleLogin();

                    } else {

                      handleSignup();

                    }

                  }

                }}
                placeholder="Enter your password"
                className={`w-full rounded-xl border px-4 py-3 text-sm outline-none focus:border-emerald-500 ${
                  darkMode
                    ? "border-slate-700 bg-slate-800 text-white"
                    : "border-slate-200 bg-slate-50 text-slate-800"
                }`}
              />

            </div>

            {/* BUTTON */}

            <button
              onClick={
                authMode ===
                "login"
                  ? handleLogin
                  : handleSignup
              }
              disabled={
                authLoading
              }
              className="mt-6 w-full rounded-xl bg-emerald-700 px-4 py-3 font-semibold text-white shadow-md transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-50"
            >

              {authLoading
                ? "Logging in..."
                : authMode ===
                  "login"
                ? "Log in"
                : "Create account"}

            </button>

            {/* SWITCH */}

            <div className="mt-5 text-center text-xs text-slate-500">

              {authMode ===
              "login"
                ? (
                  <>

                    Don't have an account?{" "}

                    <button
                      onClick={() => {

                        setAuthMode(
                          "signup"
                        );

                        setAuthError("");

                      }}
                      className="font-semibold text-emerald-600 hover:underline"
                    >
                      Sign up
                    </button>

                  </>
                )
                : (
                  <>

                    Already have an account?{" "}

                    <button
                      onClick={() => {

                        setAuthMode(
                          "login"
                        );

                        setAuthError("");

                      }}
                      className="font-semibold text-emerald-600 hover:underline"
                    >
                      Log in
                    </button>

                  </>
                )}

            </div>

          </div>

        </div>

      )}

    </div>

  );

}

// ============================================================
// STEP COMPONENT
// ============================================================

function Step({
  number,
  icon,
  title,
  text,
}) {

  return (

    <div className="text-center">

      <div className="text-[10px] font-bold tracking-widest text-emerald-600">
        {number}
      </div>

      <div className="mt-3 text-2xl">
        {icon}
      </div>

      <h3 className="mt-2 text-sm font-bold text-emerald-700">
        {title}
      </h3>

      <p className="mt-2 text-xs leading-5 text-slate-500">
        {text}
      </p>

    </div>

  );

}

export default App;