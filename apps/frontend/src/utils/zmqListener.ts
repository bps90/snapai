
export async function startZmqListener<Data>(callback: (data: Data) => void) {
    console.log("Iniciando ZMQ listener", window);
    if (typeof window !== "undefined") return;

    const zmq = await import("zeromq");

    const sock = new zmq.Pull();
    await sock.bind("tcp://127.0.0.1:5555");
    console.log("ZMQ ouvindo em tcp://127.0.0.1:5555");

    for await (const [msg] of sock) {
        try {
            const data = JSON.parse(msg.toString());
            callback(data);
        } catch (e) {
            console.error("Erro ao parsear JSON:", e);
        }
    }
}