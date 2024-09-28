import { useState } from "react";
import "./App.css";
import { SendHorizontal } from "lucide-react";

function App() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [history, setHistory] = useState<string[]>([]); // Chat history state
  const [message, setMessage] = useState(""); // Message input state

  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  const handleSendMessage = () => {
    if (message.trim()) {
      setHistory((prevHistory) => [...prevHistory, message]);
      setMessage(""); // Clear the input after sending
    }
  };

  const handleMessageChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    // Adjust the height of the textarea dynamically based on content
    e.target.style.height = "auto"; // Reset height
    e.target.style.height = `${e.target.scrollHeight}px`; // Set height based on scroll height
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
          className="absolute top-4 left-4 bg-green-500 text-white py-2 px-4 rounded md:hidden"
          onClick={toggleDrawer}
        >
          {isDrawerOpen ? "Close History" : "Open History"}
        </button>
        <div className="flex-1 flex w-full items-center justify-center">
          <h1 className="text-2xl font-bold">
            Generate Your Sustainability Report
          </h1>
        </div>
        <div className="mb-6 w-full max-w-[700px]">
          <div className="w-full   relative">
            {/* Multiline Textarea with dynamic height */}
            <textarea
              placeholder="Message ChatGreeny"
              className="input-auto-resize border-gray-300 border-[1px] p-3 rounded-md"
              value={message}
              onChange={handleMessageChange}
              rows={1} // Initial number of rows
            />
            <button
              onClick={handleSendMessage}
              className="bg-green-500 text-white w-9 h-9 text-center flex justify-center items-center absolute bottom-0 mb-3 mr-2  rounded-full right-0"
            >
              <SendHorizontal />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
