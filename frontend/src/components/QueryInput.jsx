import { useState } from "react";

export default function QueryInput({ onSubmit }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your legal/regulatory question..."
        className="border rounded p-2 flex-1"
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        Ask
      </button>
    </form>
  );
}
