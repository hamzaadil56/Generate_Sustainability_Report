import { useState } from "react";
import "./App.css";

function App() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [history, setHistory] = useState<string[]>([]); // Chat history state

  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  const handleSendMessage = (message: string) => {
    if (message.trim()) {
      setHistory((prevHistory) => [...prevHistory, message]);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar (Chat History) */}
      <div
        className={`fixed inset-y-0 left-0 w-64 bg-gray-800 text-white transition-transform transform ${
          isDrawerOpen ? "translate-x-0" : "-translate-x-full"
        } md:relative md:translate-x-0`}
      >
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-4">Chat History</h2>
          <ul>
            {history.length > 0 ? (
              history.map((chat, index) => (
                <li key={index} className="mb-2 p-2 bg-gray-700 rounded">
                  {chat}
                </li>
              ))
            ) : (
              <li className="text-gray-400">No history yet...</li>
            )}
          </ul>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center">
        <button
          className="absolute top-4 left-4 bg-blue-500 text-white py-2 px-4 rounded md:hidden"
          onClick={toggleDrawer}
        >
          {isDrawerOpen ? "Close History" : "Open History"}
        </button>

        <h1 className="text-2xl font-bold mb-6">
          Generate Your Sustainability Report
        </h1>

        <div className="w-full max-w-lg">
          <input
            type="text"
            placeholder="Type your message here..."
            className="w-full p-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSendMessage((e.target as HTMLInputElement).value);
                (e.target as HTMLInputElement).value = "";
              }
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
