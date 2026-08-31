export default function RetrievedChunks({ chunks }) {
  return (
    <div className="mt-4">
      <h3 className="text-lg font-semibold">📚 Retrieved Chunks</h3>
      <ul className="list-disc list-inside text-gray-600">
        {chunks.map((chunk, idx) => (
          <li key={idx}>{chunk}</li>
        ))}
      </ul>
    </div>
  );
}
