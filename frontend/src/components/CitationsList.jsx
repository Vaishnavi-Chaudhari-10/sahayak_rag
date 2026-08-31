export default function CitationsList({ citations }) {
  return (
    <div className="mt-4">
      <h3 className="text-lg font-semibold">🔗 Citations</h3>
      <ul className="list-disc list-inside text-gray-600">
        {citations.map((c, idx) => (
          <li key={idx}>{c}</li>
        ))}
      </ul>
    </div>
  );
}
