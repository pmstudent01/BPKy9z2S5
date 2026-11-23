const http = require("http");
const PORT = process.env.PORT || 4500;
const JSON_HEADER = { "Content-Type": "application/json" };

const server = http.createServer(async (req, res) => {
  const { method, url } = req;

  // Helper to parse request body
  const parseBody = () => new Promise((resolve) => {
    let raw = "";
    req.on("data", (c) => (raw += c));
    req.on("end", () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch { resolve({}); } });
  });

  // @endpoint POST /vehicles
  if (method === "POST" && url === "/vehicles") {
    res.writeHead(201, JSON_HEADER);
    return res.end(JSON.stringify({
      "id": 1,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": "159,864"
    }));
  }

  // @endpoint GET /vehicles/:id
  if (method === "GET" && url.match(/^\/vehicles\/\d+$/)) {
    const id = parseInt(url.split("/")[2]);
    if (id === 0) {
      res.writeHead(404, JSON_HEADER);
      return res.end(JSON.stringify({ "message": "Vehicle with id: 0 not found." }));
    }
    res.writeHead(200, JSON_HEADER);
    return res.end(JSON.stringify({
      "id": 1,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159864
    }));
  }

  // @endpoint PATCH /vehicles/:id
  if (method === "PATCH" && url.match(/^\/vehicles\/\d+$/)) {
    res.writeHead(200, JSON_HEADER);
    return res.end(JSON.stringify({
      "id": 1,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159999
    }));
  }

  // @endpoint DELETE /vehicles/:id
  if (method === "DELETE" && url.match(/^\/vehicles\/\d+$/)) {
    res.writeHead(204);
    return res.end();
  }

  res.writeHead(404, JSON_HEADER);
  res.end(JSON.stringify({
    error: "Endpoint not defined",
    message: `Please add ${url} endpoint to this mock.`
  }));
});

server.listen(PORT, () => console.log(`Mock server on port ${PORT}`));
