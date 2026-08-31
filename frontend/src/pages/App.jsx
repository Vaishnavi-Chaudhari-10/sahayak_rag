import { useState } from "react";
import QueryInput from "../components/QueryInput";
import AnswerCard from "../components/AnswerCard";
import CitationsList from "../components/CitationsList";
import RetrievedChunks from "../components/RetrievedChunks";
import { askQuestion } from "../services/api";

export default function App() {
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState([]);
  const [chunks, setChunks] = useState([]);

  const handleQuery = async (query) => {
    try {
      const data = await askQuestion(query);
      setAnswer(data.answer);
      setCitations(data.citations || []);
      setChunks(data.chunks || []);
    } catch (err) {
      setAnswer("⚠️ Error fetching answer. Please try again.");
      setCitations([]);
      setChunks([]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Sahayak Prototype</h1>
      <QueryInput onSubmit={handleQuery} />
      {answer && <AnswerCard answer={answer} />}
      {citations.length > 0 && <CitationsList citations={citations} />}
      {chunks.length > 0 && <RetrievedChunks chunks={chunks} />}
    </div>
  );
}
