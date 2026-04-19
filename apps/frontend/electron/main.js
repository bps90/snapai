import {app, BrowserWindow, ipcMain} from "electron";
import path from "path";
import zmq from "zeromq";
import fs from "fs";
import {fileURLToPath} from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
console.log(
  "Preload path:",
  path.join(__dirname, "preload.js"),
  fs.existsSync(path.join(__dirname, "preload.js"))
);
function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"), // comunicação segura
    },
  });

  // Em dev, usa o servidor Next local; em produção, o build estático
  const startUrl = process.env.ELECTRON_DEV
    ? "http://localhost:3000"
    : `file://${path.join(__dirname, "../out/index.html")}`;

  win.loadURL(startUrl);

  // setInterval(() => {
  //     const arr = [];
  //     for (let i = 0; i < Math.random() * 100000000; i++) {
  //         arr.push(Math.random() * 10000000);
  //     }
  //     console.log('enviando');
  //     win.webContents.send('electron', { arr, arrS: JSON.stringify(arr), timestamp: Date.now() });
  // }, 10000);

  ipcMain.on("get_add_nodes_form", () => {
    win.webContents.send(
      "get_add_nodes_form_response",
      JSON.parse(fs.readFileSync("add_nodes_form.json", "utf-8"))
    );
  });

  ipcMain.on("add_nodes_form_updated", (_, form) => {
    fs.writeFileSync("add_nodes_form.json", JSON.stringify(form, null, 2));
  });

  console.log("Iniciando ZMQ listener");

  const sock = new zmq.Pull();
  sock.bind("tcp://127.0.0.1:5555").then(async () => {
    console.log("ZMQ ouvindo em tcp://127.0.0.1:5555");
    let canSend = true;
    ipcMain.on("electron", () => {
      canSend = true;
    });
    const rl = new Set();
    const al = new Set();
    ipcMain.on("initialize", () => {
      rl.clear();
      al.clear();
    });
    for await (const [msg] of sock) {
      try {
        const data = JSON.parse(msg.toString());
        const nodes = data.n.map(([id, x, y, , size, color]) => ({
          id: id.toString(),
          x,
          y,
          size,
          color,
          label: id.toString(),
        }));
        // const links = data.l.reduce((acc, link) => {
        //     if (link[2]) {
        //         acc.push({ source: link[0].toString(), target: link[1].toString() });
        //         acc.push({ source: link[1].toString(), target: link[0].toString() });
        //     } else {
        //         acc.push({ source: link[0].toString(), target: link[1].toString() });
        //     }
        //     return acc;
        // }, []);
        for (const addedLink of data.a_l) {
          const [source, target] = addedLink;
          al.add(`${source}-${target}`);
          rl.delete(`${source}-${target}`);
        }
        for (const removedLink of data.r_l) {
          const [source, target] = removedLink;
          al.delete(`${source}-${target}`);
          rl.add(`${source}-${target}`);
        }

        if (!canSend) continue;
        data.r_l = Array.from(rl.values()).map((l) => {
          const [source, target] = l.split("-");
          return [source, target];
        });
        data.a_l = Array.from(al.values()).map((l) => {
          const [source, target] = l.split("-");
          return [source, target];
        });
        win.webContents.send("electron", {data: {...data, n: nodes}, timestamp: Date.now()});
        al.clear();
        rl.clear();
        canSend = false;
      } catch (e) {
        console.error("Erro ao parsear JSON:", e);
      }
    }
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
