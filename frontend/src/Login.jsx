import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          email: email.trim(),
          password: password,
        }),
      });

      const data = await res.json();

      console.log("LOGIN STATUS:", res.status);
      console.log("LOGIN RESPONSE:", data);

      if (!res.ok) {
        throw new Error(
          data.detail || data.message || "Login failed."
        );
      }

      if (!data.access_token) {
        throw new Error("Login succeeded but no access token was returned.");
      }

      // Save JWT
      localStorage.setItem(
        "access_token",
        data.access_token
      );

      // Save user
      if (data.user) {
        localStorage.setItem(
          "user",
          JSON.stringify(data.user)
        );
      }

      alert("Login successful!");

      navigate("/");

    } catch (error) {
      console.error("LOGIN ERROR:", error);
      setError(error.message);

    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Login</h1>

      {error && (
        <p style={{ color: "red" }}>
          ⚠️ {error}
        </p>
      )}

      <form onSubmit={handleLogin}>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

      </form>

      <p>
        Don't have an account?{" "}

        <button
          onClick={() => navigate("/signup")}
        >
          Sign Up
        </button>
      </p>
    </div>
  );
}

export default Login;