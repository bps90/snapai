let running = false;
let interval_update = null;
let arrows = false;
let showIds = false;
let node2vecIds = false;
let nodes = [];
let links = [];
let showLogs = true;
let logs = [];
let highlightedLinks = [];
let node2vecData = {
    words: [],
    vectors: []
}

async function renderGraph() {
    running = true;

    // Cria os dados para o scatter plot (nós)
    const nodeScatter = {
        x: nodes.map((node) => node.x),
        y: nodes.map((node) => node.y),
        text: nodes.map((node) => node.id),
        mode: showIds ? "markers+text" : "markers",
        marker: { size: nodes.map((node) => 5 * node.size), color: nodes.map((node) => node.color), symbol: "circle" },
        type: "scatter",
        textposition: "top center",
    };

    // Obtém os limites do retângulo
    const dimX = Number(document.querySelector("#dimX").value);
    const dimY = Number(document.querySelector("#dimY").value);

    // Cria as bordas do retângulo
    const boundaryShapes = [
        {
            type: "line",
            x0: 0,
            y0: 0,
            x1: dimX,
            y1: 0,
            line: { color: "black", width: 1 },
        },
        {
            type: "line",
            x0: dimX,
            y0: 0,
            x1: dimX,
            y1: dimY,
            line: { color: "black", width: 1 },
        },
        {
            type: "line",
            x0: dimX,
            y0: dimY,
            x1: 0,
            y1: dimY,
            line: { color: "black", width: 1 },
        },
        {
            type: "line",
            x0: 0,
            y0: dimY,
            x1: 0,
            y1: 0,
            line: { color: "black", width: 1 },
        },
    ];

    // Obtém o estado atual do gráfico (eixos)
    const currentGraph = document.getElementById("graph");
    const currentLayout = currentGraph.layout ?? {
        xaxis: {
            range: [dimX * -0.1, dimX * 1.1],
            zeroline: false,
        },
        yaxis: {
            range: [dimY * -0.1, dimY * 1.1],
            zeroline: false,
        },
    };

    // Configurações do layout
    const layout = {
        xaxis: {
            range: currentLayout.xaxis.range,
            zeroline: false,
        },
        yaxis: {
            range: currentLayout.yaxis.range,
            zeroline: false,
        },
        shapes: [
            ...createEdgeShapes(
                nodes,
                links,
                numberOfMessagesInThisRound,
                currentLayout
            ),
            ...boundaryShapes,
        ], // Adiciona bordas e arestas
        showlegend: false,
    };

    const graph = document.getElementById("graph");

    // Renderiza o gráfico
    Plotly.react(graph, [nodeScatter], layout);


    running = false;
}

// Função para criar as arestas como shapes (linhas com setas)
function createEdgeShapes(
    nodes,
    links,
    numberOfMessagesInThisRound,
    currentLayout
) {
    const shapes = [];
    const arrowDegrees = Math.PI / 24;
    if (!currentLayout) return shapes;

    links.forEach((link, index) => {
        const filteredNodes = nodes.filter(
            (node) => node.id === link.source || node.id === link.target
        );
        const sourceNode = filteredNodes.find((node) => node.id === link.source);
        const targetNode = filteredNodes.find((node) => node.id === link.target);
        let highlightedInOpositeDirection;

        const highlighted = highlightedLinks.find(
            (highlightedLink) => {
                if (highlightedLink.source === link.target &&
                    highlightedLink.target === link.source) {
                    highlightedInOpositeDirection = true;
                    return true;
                }
                if (highlightedLink.source === link.source &&
                    highlightedLink.target === link.target) {
                    highlightedInOpositeDirection = false;
                    return true;
                }
            }
        );

        if (sourceNode && targetNode) {
            shapes.push({
                type: "line",
                id: `link-${link.source}-${link.target}`,
                x0: sourceNode.x,
                y0: sourceNode.y,
                x1: targetNode.x,
                y1: targetNode.y,
                line: {
                    color: highlighted ? "#ff0000" : "#0000003a",
                    width: highlighted ? 5 : 2,
                },
            });

            // Adiciona uma seta
            if (arrows || highlighted) {
                const arrowSize =
                    Math.min(
                        Math.abs(
                            currentLayout.xaxis.range[1] - currentLayout.xaxis.range[0]
                        ),
                        Math.abs(
                            currentLayout.yaxis.range[1] - currentLayout.yaxis.range[0]
                        ),
                        Math.abs(
                            Math.sqrt(
                                Math.pow(targetNode.x - sourceNode.x, 2) +
                                Math.pow(targetNode.y - sourceNode.y, 2)
                            )
                        ) * 10
                    ) * 0.02;

                let angle = Math.atan2(
                    targetNode.y - sourceNode.y,
                    targetNode.x - sourceNode.x
                );
                if (arrows || highlightedInOpositeDirection === false) {
                    shapes.push({
                        type: "path",
                        path: `M ${targetNode.x - arrowSize * Math.cos(angle - arrowDegrees)
                            } ${targetNode.y - arrowSize * Math.sin(angle - arrowDegrees)}
              L ${targetNode.x - arrowSize * Math.cos(angle + arrowDegrees)} ${targetNode.y - arrowSize * Math.sin(angle + arrowDegrees)
                            }
              L ${targetNode.x} ${targetNode.y}
              Z`,
                        fillcolor: (highlightedInOpositeDirection === false) ? "#ff0000" : "#813131",
                        line: {
                            color: (highlightedInOpositeDirection === false) ? "#ff0000" : "#813131",
                        },
                    });
                }
                if ((arrows && link.bidirectional) || highlightedInOpositeDirection) {
                    angle = angle + Math.PI;
                    shapes.push({
                        type: "path",
                        path: `M ${sourceNode.x - arrowSize * Math.cos(angle - arrowDegrees)
                            } ${sourceNode.y - arrowSize * Math.sin(angle - arrowDegrees)}
              L ${sourceNode.x} ${sourceNode.y}
              L ${sourceNode.x - arrowSize * Math.cos(angle + arrowDegrees)} ${sourceNode.y - arrowSize * Math.sin(angle + arrowDegrees)
                            }
              Z`,
                        fillcolor: highlightedInOpositeDirection ? "#ff0000" : "#813131",
                        line: {
                            color: highlightedInOpositeDirection ? "#ff0000" : "#813131",
                        },
                    });
                }
            }
        }
    });

    return shapes;
}

/*async function renderGraph(nodes, links, round, numberOfMessagesInThisRound,
  numberOfMessagesOverAll) {
  const svgns = "http://www.w3.org/2000/svg";
  const graph_svg = document.getElementById("graph_svg");

  const nodes_circles = nodes.map((node) => {
    const node_circle =
      graph_svg.getElementById("node-" + node.id) ||
      document.createElementNS(svgns, "circle");

    node_circle.setAttributeNS(null, "id", "node-" + node.id);
    node_circle.setAttributeNS(null, "class", "node");
    node_circle.setAttributeNS(null, "cx", node.x);
    node_circle.setAttributeNS(null, "cy", node.y);
    node_circle.setAttributeNS(null, "r", 20);
    node_circle.setAttributeNS(null, "fill", "blue");
    graph_svg.getElementById("node-" + node.id) ||
      graph_svg.append(node_circle);

    return node_circle;
  });

  old_drawed_link_lines = graph_svg.getElementsByClassName("link");

  for (const link_line of old_drawed_link_lines) {
    graph_svg.removeChild(link_line);
  }

  const link_lines = links.map((link) => {
    const link_line =
      graph_svg.getElementById("link-" + link.source + "-" + link.target) ||
      document.createElementNS(svgns, "line");

    source_node = nodes.find((node) => node.id === link.source);
    target_node = nodes.find((node) => node.id === link.target);

    link_line.setAttributeNS(
      null,
      "id",
      "link-" + link.source + "-" + link.target
    );
    link_line.setAttributeNS(null, "class", "link");
    link_line.setAttributeNS(null, "x1", source_node.x);
    link_line.setAttributeNS(null, "x2", target_node.x);
    link_line.setAttributeNS(null, "y1", source_node.y);
    link_line.setAttributeNS(null, "y2", target_node.y);
    link_line.setAttributeNS(null, "stroke-width", "10");
    link_line.setAttributeNS(null, "stroke", "black");

    graph_svg.getElementById("link-" + link.source + "-" + link.target) ||
      graph_svg.append(link_line);

    return link_line;
  });

  document.getElementById("time").innerText = round;
  document.getElementById("numberOfMessagesInThisRound").innerText =
    numberOfMessagesInThisRound;
  document.getElementById("numberOfMessagesOverAll").innerText =
    numberOfMessagesOverAll;
}*/

function updateGUIInfo(round, numberOfMessagesInThisRound, numberOfMessagesOverAll) {
    document.getElementById("time").innerText = round;
    document.getElementById("numberOfMessagesInThisRound").innerText =
        numberOfMessagesInThisRound;
    document.getElementById("numberOfMessagesOverAll").innerText =
        numberOfMessagesOverAll;
    $('.round_logs').html(logs.slice().reverse().map((round_logs, index, array) => round_logs.map((log) => `${array.length - index - 1}: ${log}`).join('<br>') + (round_logs.length ? '<br>' : '')).join(''));
}

let chamadasHTTP = 0;
let currentRound = -1;
function getUpdatedGraph() {
    chamadasHTTP++;
    $.ajax({
        url: "update_graph/?with_logs=" + showLogs,
        type: "GET",
        success: function (data) {
            chamadasHTTP--;
            if (!data.n || !data.l) return clearInterval(interval_update);
            if (!data.r) clearInterval(interval_update);
            if (data.t < currentRound) return;
            if (data.t != currentRound) {
                highlightedLinks = [];
            }

            if (!running) {
                running = true;

                let lastts = Date.now();
                currentRound = data.t;
                nodes = data.n.map(([id, x, y, z, size, color]) => ({ id, x, y, z, size, color }));
                links = data.l.map(([source, target, bidirectional]) => ({
                    source,
                    target,
                    bidirectional,
                }));
                if (showLogs) logs[data.t] = data.logs.reverse();
                renderGraph();
                console.log("Tempo gasto pra renderizar", Date.now() - lastts, "ms");
                updateGUIInfo(data.t, data.msg_r, data.msg_a);

                running = false;
            } else console.warn(running);
        },
    });
}

function intervalUpdate() {
    if (interval_update) clearInterval(interval_update);

    interval_update = setInterval(() => {
        if (chamadasHTTP < 2) getUpdatedGraph();
    }, 1000 / getSelectedGUIRefreshRate());
}

function showArrows() {
    arrows = true;
    getUpdatedGraph();
}

function hideArrows() {
    arrows = false;
    getUpdatedGraph();
}

function showNodesIds() {
    showIds = true;
    getUpdatedGraph();
}

function hideNodesIds() {
    showIds = false;
    getUpdatedGraph();
}

function showNode2vecIds() {
    node2vecIds = true;
    if (node2vecData.vectors[0]?.length <= 2)
        plot_node2vec_2d(node2vecData.vectors[0]?.length === 1);
    else plot_node2vec_3d(node2vecData.vectors[0]?.length > 3);
}

function hideNode2vecIds() {
    node2vecIds = false;
    if (node2vecData.vectors[0]?.length <= 2)
        plot_node2vec_2d(node2vecData.vectors[0]?.length === 1);
    else plot_node2vec_3d(node2vecData.vectors[0]?.length > 3);
}

function toggleConfigurations() {
    $("#options-form").toggle();
}

function toggleAddNodesForm() {
    $("#add-nodes-form").toggle();
}

function calculateDistanceBetweenTwoNodes() {
    const node1Id = $("#two-nodes-algorithms-node-1").val();
    const node2Id = $("#two-nodes-algorithms-node-2").val();

    $.ajax({
        method: 'GET',
        url: 'calculate_distance/?node1=' + node1Id + '&node2=' + node2Id,
        success: function (data) {
            $("#two-nodes-algorithms-result").val(data.distance);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}

async function onReady() {
    intervalUpdate();

    $.ajax({
        url: "projects_names/",
        type: "GET",
        success: function (data) { },
        error: function (xhr, status, error) {
            console.error(error);
        },
    });

    initForm();

    // Adicionar evento de clique com botão direito
    const plotElement = document.getElementById("graph");
    plotElement.addEventListener("contextmenu", function (event) {
        // Prevenir o menu padrão do botão direito
        event.preventDefault();

        // Usar plotly_click para identificar o ponto
        plotElement.on("plotly_relayout", function (data) {
            if (data.points.length > 0) {
                const point = data.points[0];
                const x = point.x;
                const y = point.y;

                alert(`Você clicou com o botão direito no ponto: (x=${x}, y=${y})`);
            }
        });
    });

    $(".confirmation-check").hide();
    toggleConfigurations();
    toggleAddNodesForm();
}

function getSelectedProject() {
    const select = document.querySelector("#project");
    const option = select.children[select.selectedIndex];

    return option.textContent;
}

function getSelectedGUIRefreshRate() {
    const select = document.querySelector("#GUI_refresh_rate");
    const option = select.children[select.selectedIndex];

    return Number(option.value);
}

function clearLogs() {
    $(".round_logs").text("");
    logs = [];
}

function initForm() {
    const project = getSelectedProject();

    $.ajax({
        url: "get_config/?project=" + project,
        type: "GET",
        success: function (data) {
            console.log(data);
            populateForm(data, 'options-form');
            populateForm(data, 'add-nodes-form');
        },
        error: function (xhr, status, error) {
            console.error(error);
        },
    });
}

$(document).ready(onReady);

function initSimulation() {
    $.ajax({
        url: "init_simulation/?project=" + getSelectedProject(),
        type: "GET",
        success: function () {
            $("#initialized").show();
            setTimeout(() => {
                $("#initialized").hide();
            }, 2000);
            currentRound = -1;
            clearLogs();
            getUpdatedGraph();
        },
        error: function (xhr, status, error) {
            alert("Erro");
            console.error(error);
        },
    });
}

function runSimulation() {
    const rounds = document.querySelector("#simulation_rounds").value;
    let refreshRate = document.querySelector("#simulation_refresh_rate").value;

    if (!rounds) return alert('Preencha o campo "rodadas"');

    if (!refreshRate) refreshRate = 0;

    $.ajax({
        url: "run_simulation/?rounds=" + rounds + "&refresh_rate=" + refreshRate,
        type: "GET",
        success: function () {
            intervalUpdate();
        },
        error: function (xhr, status, error) {
            console.error(error);
        },
    });
}

function stopSimulation() {
    $.ajax({
        url: "stop_simulation/",
        type: "GET",
        success: function () { },
        error: function (xhr, status, error) {
            console.error(error);
        },
    });
}

function changeProject(e) {
    initForm();
}

function changeGUIRefreshRate(e) {
    intervalUpdate();
}

function listenForm(formId) {
    // Função que será executada quando o formulário for submetido
    document
        .getElementById(formId)
        .addEventListener("submit", function (event) {
            // Impede o envio do formulário para poder processar os dados com JS
            event.preventDefault();

            // Serializa os dados do formulário
            const formData = $(this).serialize();

            $.ajax({
                url: $(this).attr("action"), // URL definida no atributo 'action' do formulário
                type: "POST", // Método HTTP
                data: formData, // Dados do formulário
                headers: {
                    "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val(), // Adiciona o CSRF token
                },
                success: function (response) {
                    $(formId === 'add-nodes-form' ? '#submitted-add-nodes' : "#submitted").show();
                    if (formId === 'add-nodes-form')
                        getUpdatedGraph()
                    setTimeout(() => {
                        $(formId === 'add-nodes-form' ? '#submitted-add-nodes' : "#submitted").hide();
                    }, 2000);
                },
                error: function (xhr, status, error) {
                    console.error("Erro ao enviar o formulário:", error);
                    alert("Erro ao enviar o formulário.");
                },
            });
        });
}

listenForm("options-form")
listenForm("add-nodes-form")

/**
     * Preenche o formulário com os valores do arquivo JSON.
     * @param {Object} jsonData - Dados do JSON a serem aplicados ao formulário.
     */
function populateForm(jsonData, formId) {
    const form = document.getElementById(formId);

    Object.entries(jsonData).forEach(([key, value]) => {
        // Verifica se o valor é um objeto aninhado
        if (
            typeof value === "object" &&
            !Array.isArray(value) &&
            value !== null
        ) {
            Object.entries(value).forEach(([subKey, subValue]) => {
                const field = form.querySelector(`[name="${key}[${subKey}]"]`);
                if (field) {
                    setFieldValue(field, subValue);
                }
            });
        } else {
            // Atualiza valores simples
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                setFieldValue(field, value);
            }
        }
    });

    const field = document.querySelector(`[name="simulation_rounds"]`);

    setFieldValue(field, jsonData.simulation_rounds);
}

/**
 * Define o valor de um campo do formulário com base no tipo do campo.
 * @param {HTMLElement} field - Campo do formulário.
 * @param {any} value - Valor a ser aplicado ao campo.
 */
function setFieldValue(field, value) {
    if (field.type === "checkbox") {
        field.checked = Boolean(value);
    } else if (field.type === "radio") {
        const radio = document.querySelector(
            `[name="${field.name}"][value="${value}"]`
        );
        if (radio) radio.checked = true;
    } else {
        field.value = value;
    }
}

function node2vecAlgorithm() {
    $.ajax({
        url: "node2vec_algorithm/?dimensions=" + $("#node2vec-dimensions").val(),
        type: "GET",
        success: function (data) {
            node2vecData = data;

            if (data.vectors[0].length <= 2)
                return plot_node2vec_2d(data.vectors[0].length === 1);
            else
                return plot_node2vec_3d(data.vectors[0].length > 3);
        },
        error: function (xhr, status, error) {
            console.error(error);
        },
    });
}



function plot_node2vec_2d(unidimensional) {
    const { words, vectors } = node2vecData;

    let x = vectors.map(v => v[0]);
    let y = vectors.map(v => unidimensional ? 0 : v[1]);

    // Encontrar os maiores valores absolutos para ajustar os eixos simetricamente
    let maxAbs = Math.max(
        Math.max(...x.map(Math.abs)),
        Math.max(...y.map(Math.abs))
    );

    let trace = {
        x: x,
        y: y,
        text: words, // Rótulos nos pontos
        mode: node2vecIds ? "markers+text" : "markers",
        textposition: "top center",
        marker: { size: 10, color: "black" }
    };

    let layout = {
        title: "Node2Vec Embeddings (2D)",
        xaxis: { title: "Dimension 1", range: [-maxAbs * 1.1, maxAbs * 1.1] },
        yaxis: { title: "Dimension 2", range: [-maxAbs * 1.1, maxAbs * 1.1] },
        showlegend: false
    };

    Plotly.newPlot("node2vec-graph", [trace], layout);
}

function plot_node2vec_3d(fourthDimension) {
    const { words, vectors } = node2vecData;

    let x = vectors.map(v => v[0]);
    let y = vectors.map(v => v[1]);
    let z = vectors.map(v => v[2]);
    let w = fourthDimension ? vectors.map(v => v[3]) : null;

    // Encontrar o maior valor absoluto para eixos simétricos
    let maxAbs = Math.max(
        Math.max(...x.map(Math.abs)),
        Math.max(...y.map(Math.abs)),
        Math.max(...z.map(Math.abs))
    );

    let trace = {
        x: x,
        y: y,
        z: z, // Adicionando terceira dimensão
        text: words,
        mode: node2vecIds ? "markers+text" : "markers",
        textposition: "top center",
        marker: { size: 6, color: fourthDimension ? w : "black", colorscale: "Viridis" }, // Cor baseada em W
        type: "scatter3d"
    };

    let layout = {
        title: "Node2Vec Embeddings (3D)",
        scene: {
            xaxis: { title: "Dimension 1", range: [-maxAbs * 1.1, maxAbs * 1.1] },
            yaxis: { title: "Dimension 2", range: [-maxAbs * 1.1, maxAbs * 1.1] },
            zaxis: { title: "Dimension 3", range: [-maxAbs * 1.1, maxAbs * 1.1] }
        },
        showlegend: false
    };

    Plotly.newPlot("node2vec-graph", [trace], layout);
}

function download_graph(graphId) {
    Plotly.toImage(graphId, { format: 'svg', width: 1000, height: 1000 }).then(function (dataUrl) {
        let link = document.createElement('a');
        link.href = dataUrl;
        link.download = 'grafico.svg';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}

$('#show-logs').change(function () {
    if (this.checked) {
        $('.round_logs').show();
        showLogs = true;
    } else {
        $('.round_logs').hide();
        showLogs = false;
    }
});

