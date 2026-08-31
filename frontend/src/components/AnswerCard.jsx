export default function AnswerCard({ answer }) {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 mt-4">
      <h2 className="text-xl font-semibold text-gray-800">📖 उत्तर</h2>
      <p className="mt-2 text-gray-700 whitespace-pre-line">{answer}</p>
    </div>
  );
}
