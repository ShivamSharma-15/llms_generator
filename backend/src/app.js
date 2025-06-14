const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const { spawn } = require("child_process");
const path = require("path");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Serve frontend
app.use(express.static(path.join(__dirname, "..", "..", "/frontend")));

io.on("connection", (socket) => {
  console.log("Client connected");

  socket.on("analyzeWebsite", (data) => {
    console.log("Received URL:", data);

    const py = spawn("python", ["./src/script.py", JSON.stringify(data)]);
    let result = "";

    py.stdout.on("data", (chunk) => {
      result += chunk.toString();
    });

    py.stderr.on("data", (err) => {
      console.error("Python error:", err.toString());
    });

    py.on("close", () => {
      try {
        const parsed = JSON.parse(result);
        socket.emit("analysisResult", parsed);
      } catch (err) {
        socket.emit("analysisResult", {
          error: "Failed to parse Python output",
        });
      }
    });
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected");
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
