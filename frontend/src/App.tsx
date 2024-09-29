import React, { useState, useRef, useEffect } from "react";
import { SendHorizontal } from "lucide-react";
import axios from "axios";

function App() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async () => {
    if (inputMessage.trim()) {
      const userMessage = { type: "user", content: inputMessage };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInputMessage("");
      setIsLoading(true);

      try {
        const response = await axios.post(
          "http://localhost:8000/generate-answer",
          { query: inputMessage }
        );
        const botMessage = {
          type: "bot",
          content: JSON.parse(response.data.response)["answer"],
        };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.log(error);
        const errorMessage = {
          type: "error",
          content: "Sorry, I couldn't process your request.",
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
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
          {/* <ul>
            {messages.length > 0 ? (
              messages.map((msg, index) => (
                <li key={index} className="mb-2 p-2 bg-gray-700 rounded">
                  {msg.content.substring(0, 30)}...
                </li>
              ))
            ) : (
              <li className="text-gray-400">No history yet...</li>
            )}
          </ul> */}
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        <button
          className="md:hidden bg-green-500 text-white py-2 px-4 rounded m-4"
          onClick={toggleDrawer}
        >
          {isDrawerOpen ? "Close History" : "Open History"}
        </button>

        <div className="flex-1 overflow-y-auto p-4">
          <h1 className="text-2xl font-bold mb-4 text-center">
            Sustainability Analytics
          </h1>

          {/* Messages display area */}
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.type === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[70%] p-3 rounded-lg ${
                    msg.type === "user"
                      ? "bg-green-500 text-white"
                      : msg.type === "bot"
                      ? "bg-gray-200 text-black"
                      : "bg-red-500 text-white"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-black max-w-[70%] p-3 rounded-lg">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input area */}
        <div className="p-4 border-t">
          <div className="relative">
            <textarea
              placeholder="Message ChatGreeny"
              className="input-auto-resize  w-full border border-gray-300 rounded-md p-3 pr-12 resize-none"
              value={inputMessage}
              onChange={handleInputChange}
              onKeyPress={(e) =>
                e.key === "Enter" && !e.shiftKey && handleSendMessage()
              }
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              className="absolute right-2 bottom-2 bg-green-500 text-white w-9 h-9 rounded-full flex items-center justify-center"
              disabled={isLoading}
            >
              <SendHorizontal size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
