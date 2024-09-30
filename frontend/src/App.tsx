import React, { useState, useRef, useEffect } from "react";
import { SendHorizontal } from "lucide-react";
import axios from "axios";
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { Bar, Line } from "react-chartjs-2";
import Loader from "./Loader";

Chart.register(CategoryScale);

function App() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: "My First Dataset",
        data: [65, 59, 80, 81, 56, 55, 40],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 159, 64, 0.2)",
          "rgba(255, 205, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(201, 203, 207, 0.2)",
        ],
        borderColor: [
          "rgb(255, 99, 132)",
          "rgb(255, 159, 64)",
          "rgb(255, 205, 86)",
          "rgb(75, 192, 192)",
          "rgb(54, 162, 235)",
          "rgb(153, 102, 255)",
          "rgb(201, 203, 207)",
        ],
        borderWidth: 1,
      },
    ],
  });

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
          chartType: JSON.parse(response.data.response)?.["chart_type"],
          data: JSON.parse(response.data.response)?.["data"],
          dataType: JSON.parse(response.data.response)?.["data_type"],
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

      {/* Main content */}
      <div className="flex-1 flex flex-col max-w-2xl mx-auto">
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
                  <div>
                    {msg?.data && msg?.chartType === "Bar" && (
                      <div>
                        <Bar
                          data={{
                            labels: msg?.data.map((data) => data?.company),
                            datasets: [
                              {
                                label: msg?.dataType,
                                data: msg?.data.map((data) => data.value),
                                borderColor: "black",
                                borderWidth: 2,
                              },
                            ],
                          }}
                        />
                      </div>
                    )}
                  </div>
                  {msg?.data && msg?.chartType === "Line" && (
                    <div className="w-[70%]">
                      <Line
                        data={{
                          labels: msg?.data.map((data) => data?.year),
                          datasets: [
                            {
                              label: msg?.dataType,
                              data: msg?.data.map((data) => data.value),
                              borderColor: "black",
                              borderWidth: 2,
                            },
                          ],
                        }}
                      />
                    </div>
                  )}
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
              className="absolute right-2 bottom-2 bg-green-500 text-white w-9 h-9 mb-[4px] rounded-full flex items-center justify-center"
              disabled={isLoading}
            >
              {isLoading ? <Loader /> : <SendHorizontal size={20} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
