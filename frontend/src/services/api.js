// export async function askQuestion(query) {
//   const res = await fetch("http://localhost:8000/query", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ query }),
//   });
//   if (!res.ok) {
//     throw new Error("Failed to fetch answer");
//   }
//   return res.json();
// }
const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "https://sahayak-backend-vz96.onrender.com";


// ============================================================
// GET TOKEN
// ============================================================

function getToken() {
  return localStorage.getItem("access_token");
}


// ============================================================
// HANDLE API RESPONSE
// ============================================================

async function handleResponse(res) {

  const contentType =
    res.headers.get("content-type") || "";

  let data = null;


  // ----------------------------------------------------------
  // JSON RESPONSE
  // ----------------------------------------------------------

  if (
    contentType.includes(
      "application/json"
    )
  ) {

    try {

      data = await res.json();

    } catch {

      data = null;

    }
  }


  // ----------------------------------------------------------
  // SUCCESS
  // ----------------------------------------------------------

  if (res.ok) {

    return data;

  }


  // ----------------------------------------------------------
  // FASTAPI DETAIL
  // ----------------------------------------------------------

  let message =
    "Something went wrong.";


  if (
    data &&
    typeof data.detail === "string"
  ) {

    message = data.detail;

  }


  // ----------------------------------------------------------
  // DETAIL AS OBJECT / ARRAY
  // ----------------------------------------------------------

  else if (
    data &&
    data.detail
  ) {

    message = JSON.stringify(
      data.detail
    );

  }


  // ----------------------------------------------------------
  // FALLBACK MESSAGE
  // ----------------------------------------------------------

  else if (
    data &&
    data.message
  ) {

    message = data.message;

  }


  const error =
    new Error(message);


  error.status =
    res.status;

  error.detail =
    data?.detail || null;


  throw error;
}


// ============================================================
// ASK QUESTION
// ============================================================

export async function askQuestion(
  query,
  language = "English",
  stakeholder = "Researcher"
) {

  const token =
    getToken();


  if (!token) {

    throw new Error(
      "Please login first."
    );
  }


  const res = await fetch(
    `${API_BASE_URL}/query`,
    {

      method: "POST",

      headers: {

        "Content-Type":
          "application/json",

        "Authorization":
          `Bearer ${token}`
      },

      body: JSON.stringify({

        query,

        language,

        stakeholder

      })
    }
  );


  return handleResponse(
    res
  );
}


// ============================================================
// GET ALL CHATS
// ============================================================

export async function getChats() {

  const token =
    getToken();


  if (!token) {

    throw new Error(
      "Please login first."
    );
  }


  const res = await fetch(
    `${API_BASE_URL}/chats`,
    {

      method: "GET",

      headers: {

        "Authorization":
          `Bearer ${token}`
      }
    }
  );


  return handleResponse(
    res
  );
}


// ============================================================
// GET SINGLE CHAT
// ============================================================

export async function getChat(
  chatId
) {

  const token =
    getToken();


  if (!token) {

    throw new Error(
      "Please login first."
    );
  }


  const res = await fetch(
    `${API_BASE_URL}/chats/${chatId}`,
    {

      method: "GET",

      headers: {

        "Authorization":
          `Bearer ${token}`
      }
    }
  );


  return handleResponse(
    res
  );
}


// ============================================================
// SIGNUP
// ============================================================

export async function signup(
  name,
  email,
  password
) {

  const res = await fetch(
    `${API_BASE_URL}/auth/signup`,
    {

      method: "POST",

      headers: {

        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({

        name,

        email,

        password

      })
    }
  );


  return handleResponse(
    res
  );
}


// ============================================================
// LOGIN
// ============================================================

export async function login(
  email,
  password
) {

  const res = await fetch(
    `${API_BASE_URL}/auth/login`,
    {

      method: "POST",

      headers: {

        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({

        email,

        password

      })
    }
  );


  const data =
    await handleResponse(
      res
    );


  // ----------------------------------------------------------
  // SAVE JWT
  // ----------------------------------------------------------

  if (
    data &&
    data.access_token
  ) {

    localStorage.setItem(
      "access_token",
      data.access_token
    );

  }


  // ----------------------------------------------------------
  // SAVE USER
  // ----------------------------------------------------------

  if (
    data &&
    data.user
  ) {

    localStorage.setItem(
      "user",
      JSON.stringify(
        data.user
      )
    );

  }


  return data;
}


// ============================================================
// LOGOUT
// ============================================================

export function logout() {

  localStorage.removeItem(
    "access_token"
  );

  localStorage.removeItem(
    "user"
  );
}


// ============================================================
// GET CURRENT USER
// ============================================================

export async function getCurrentUser() {

  const token =
    getToken();


  if (!token) {

    throw new Error(
      "Please login first."
    );
  }


  const res = await fetch(
    `${API_BASE_URL}/auth/me`,
    {

      method: "GET",

      headers: {

        "Authorization":
          `Bearer ${token}`
      }
    }
  );


  return handleResponse(
    res
  );
}