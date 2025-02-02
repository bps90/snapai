function calculateDegree() {
    $.ajax({
        url: "calculate_degree/?node_id=" + $("#degree-algorithm-node").val(),
        type: "GET",
        success: function (data) {

            $("#degree-result").val(data.degree);
        },
        error: function (xhr, status, error) {
            console.error(error, xhr?.responseJSON?.message);
            $("#degree-result").attr("title", xhr?.responseJSON?.message || "Erro ao calcular grau");
            $("#degree-result").val(xhr?.responseJSON?.message || "Erro ao calcular grau");
        },
    })
}

function calculateDiameter() {
    $.ajax({
        url: "calculate_diameter/",
        type: "GET",
        success: function (data) {

            $("#diameter-result").val(data.diameter);
        },
        error: function (xhr, status, error) {
            console.error(error, xhr?.responseJSON?.message);
            $("#diameter-result").attr("title", xhr?.responseJSON?.message || "Erro ao calcular diametro");
            $("#diameter-result").val(xhr?.responseJSON?.message || "Erro ao calcular diametro");
        },
    });
}

function calculateEccentricity() {
    const nodeId = $("#eccentricity-algorithm-node").val();

    $.ajax({
        url: "calculate_eccentricity/?node_id=" + nodeId,
        type: "GET",
        success: function (data) {
            $("#eccentricity-result").val(data.eccentricity);
        },
        error: function (xhr, status, error) {
            console.error(error, xhr?.responseJSON?.message);
            $("#eccentricity-result").attr("title", xhr?.responseJSON?.message || "Erro ao calcular excentricidade");
            $("#eccentricity-result").val(xhr?.responseJSON?.message || "Erro ao calcular excentricidade");
        },
    });
}

function calculateShortestPathBetweenTwoNodes() {
    const node1Id = $("#two-nodes-algorithms-node-1").val();
    const node2Id = $("#two-nodes-algorithms-node-2").val();

    $.ajax({
        url: "calculate_shortest_path_between_two_nodes/?node1_id=" + node1Id + "&node2_id=" + node2Id,
        type: "GET",
        success: function (data) {
            ''
            $("#two-nodes-algorithms-result").val(data.shortest_path);
            highlightedLinks = [];
            data.shortest_path.reduce((prev, curr) => {
                const link = {
                    source: prev,
                    target: curr,
                    bidirectional: 0,
                };
                highlightedLinks.push(link);
                return curr;
            });
            getUpdatedGraph();
        },
        error: function (xhr, status, error) {
            console.error(error, xhr?.responseJSON?.message);
            $("#two-nodes-algorithms-result").attr("title", xhr?.responseJSON?.message || "Erro ao calcular caminho mais curto");
            $("#two-nodes-algorithms-result").val(xhr?.responseJSON?.message || "Erro ao calcular caminho mais curto");
        },
    });
}