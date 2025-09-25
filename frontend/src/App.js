import React, { useState } from "react";
import { Input, Button, Card, List, Typography } from "antd";
import axios from "axios";

const { Text } = Typography;

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { role: "user", content: input };
    setMessages([...messages, newMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        question: input,
      });

      const botMessage = {
        role: "bot",
        content: res.data.answer,
        sources: res.data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "20px auto" }}>
      <Card title="🤖 Gemini RAG Chatbot" bordered={false}>
        <List
          dataSource={messages}
          renderItem={(msg, idx) => (
            <List.Item key={idx}>
              <div>
                <Text strong>
                  {msg.role === "user" ? "You: " : "Bot: "}
                </Text>
                <Text>{msg.content}</Text>
                {msg.sources && (
                  <div style={{ marginTop: 5 }}>
                    <Text type="secondary">📚 Sources: {msg.sources.join(", ")}</Text>
                  </div>
                )}
              </div>
            </List.Item>
          )}
        />
        <Input.Group compact style={{ marginTop: 10 }}>
          <Input
            style={{ width: "calc(100% - 100px)" }}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onPressEnter={sendMessage}
            disabled={loading}
          />
          <Button type="primary" onClick={sendMessage} loading={loading}>
            Send
          </Button>
        </Input.Group>
      </Card>
    </div>
  );
}

export default App;