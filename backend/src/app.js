const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");
const axios = require("axios");

const app = express();
const server = http.createServer(app);

/* Mount the whole application under this prefix */
const BASE_PATH = "/apps/llms";

app.use(
  BASE_PATH,
  express.static(path.join(__dirname, "..", "..", "frontend"))
);

/* ── WebSocket setup ─────────────────────────────────────── */
const io = new Server(server, {
  path: `${BASE_PATH}/socket.io`,
});

io.on("connection", (socket) => {
  console.log("Client connected");

  socket.on("analyzeWebsite", async (data) => {
    console.log("Received URL:", data);

    try {
      const response = await axios.post("http://flask:5000/get-data", data); // Replace 'flask' with your Flask container's hostname
      socket.emit("analysisResult", response.data);
    } catch (error) {
      console.error("Request to Flask failed:", error.message);
      socket.emit("analysisResult", { error: "Failed to analyze website" });
    }
  });

  socket.on("disconnect", () => console.log("Client disconnected"));
});

/* ── Start the server ────────────────────────────────────── */
const PORT = process.env.PORT || 3000;
server.listen(PORT, () =>
  console.log(`Server running on port ${PORT} (base path ${BASE_PATH})`)
);
